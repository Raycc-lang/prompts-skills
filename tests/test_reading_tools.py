import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import daily
import prep
import smd
import pick


class ReadingToolTests(unittest.TestCase):
    def test_only_read_starts_browser_workflow(self):
        with patch.object(sys, "argv", ["daily.py", "--only-read"]), patch.object(
            daily.socket.socket, "connect_ex", return_value=1
        ), patch.object(daily, "run", return_value=0) as run:
            daily.main()
        command = run.call_args.args[0]
        self.assertEqual(command[-1], str(TOOLS / "pick.py"))

    def test_batch_main_returns_failure_when_runner_reports_failed_tasks(self):
        class FakeRunner:
            def __init__(self, *args):
                pass

            def start(self):
                pass

            def batch(self, path):
                return False

        with patch.object(sys, "argv", ["smd.py", "-f", "batch.txt"]), patch.object(
            smd, "Runner", FakeRunner
        ), self.assertRaises(SystemExit) as raised:
            smd.main()
        self.assertEqual(raised.exception.code, 1)

    def test_worker_records_unexpected_exception(self):
        class BrokenClient:
            def chat(self, *args, **kwargs):
                raise ValueError("bad response")

        runner = smd.Runner(1, tempfile.mkdtemp(), "unused", False, False)
        runner._process(BrokenClient(), ("word", "", ""))
        self.assertEqual(runner.stats["failed"], 1)
        self.assertEqual(runner.results[0][1], "failed")

    def test_rate_limit_log_is_english_and_retries_until_success(self):
        class LimitedClient:
            def __init__(self):
                self.calls = 0

            def chat(self, *args, **kwargs):
                self.calls += 1
                if self.calls < 3:
                    raise RuntimeError(
                        "Rate limited (HTTP 429); approximate quota reset: unknown"
                    )
                return "reply", "conversation"

        runner = smd.Runner(1, tempfile.mkdtemp(), "unused", False, False)
        client = LimitedClient()
        with patch.object(runner, "_set_cooldown",
                          return_value=(0.0, "2026-08-18 22:00:00")), patch.object(
            runner, "_wait_for_cooldown"
        ), patch("sys.stdout", new_callable=io.StringIO) as output:
            runner._process(client, ("word", "", ""))
        self.assertEqual(client.calls, 3)
        self.assertEqual(runner.stats["done"], 1)
        self.assertEqual(runner.stats["failed"], 0)
        self.assertIn("[RATE LIMITED]", output.getvalue())
        self.assertNotIn("触发限流", output.getvalue())

    def test_progressive_cooldown_starts_at_ten_minutes(self):
        with patch.object(smd.random, "uniform", return_value=0), patch.object(
            smd.time, "time", return_value=1000
        ):
            self.assertEqual(smd.Runner._reset_wait("HTTP 429", 1), 600)
            self.assertEqual(smd.Runner._reset_wait("HTTP 429", 2), 1200)
            self.assertEqual(smd.Runner._reset_wait("HTTP 429", 4), 3600)

    def test_detached_launch_configuration(self):
        config = pick.detached_popen_kwargs()
        if os.name == "nt":
            expected = (pick.subprocess.CREATE_NEW_PROCESS_GROUP |
                        pick.subprocess.DETACHED_PROCESS)
            self.assertEqual(config["creationflags"], expected)
        else:
            self.assertTrue(config["start_new_session"])

    def test_detached_command_forces_utf8_and_writes_state(self):
        with tempfile.TemporaryDirectory() as day, patch.object(
            pick.subprocess, "Popen"
        ) as popen:
            popen.return_value.pid = 321
            server = pick.PickServer("page", day, True, 2)
            server.submit([{"word": "alpha", "sentence": "An alpha."}])
            command = popen.call_args.args[0]
            kwargs = popen.call_args.kwargs
            state = json.loads(Path(day, pick.JOB_STATE_NAME).read_text(
                encoding="utf-8"
            ))
        self.assertEqual(command[1:3], ["-X", "utf8"])
        self.assertIs(kwargs["stdin"], pick.subprocess.DEVNULL)
        self.assertIs(kwargs["stderr"], pick.subprocess.STDOUT)
        self.assertIsNone(state["pid"])
        self.assertEqual(state["status"], "starting")
        self.assertEqual(state["tasks"][0]["word"], "alpha")

    def test_reload_switches_all_day_scoped_paths(self):
        with tempfile.TemporaryDirectory() as root, patch.object(
            pick, "READING_DIR", root
        ):
            old_day = Path(root, "2026-08-18")
            new_day = Path(root, "2026-08-19")
            old_day.mkdir()
            new_day.mkdir()
            Path(new_day, "article.txt").write_text(
                "New article", encoding="utf-8")
            server = pick.PickServer("old page", str(old_day), True, 2)
            ok, day = server.reload("2026-08-19")
        self.assertTrue(ok)
        self.assertEqual(day, "2026-08-19")
        self.assertEqual(server.day_dir, str(new_day.resolve()))
        self.assertEqual(server.state_path, str(new_day / pick.JOB_STATE_NAME))
        self.assertEqual(server.log_path, str(new_day / pick.SMD_LOG_NAME))
        self.assertIn("New article", server.page_html)

    def test_atomic_state_writes_use_distinct_temporary_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory, "state.json"))
            sources = []

            def record_replace(source, target):
                sources.append(source)
                Path(target).write_bytes(Path(source).read_bytes())
                Path(source).unlink()

            with patch.object(pick.os, "replace", side_effect=record_replace):
                pick.atomic_write_json(path, {"writer": 1})
                pick.atomic_write_json(path, {"writer": 2})
            self.assertEqual(len(set(sources)), 2)
            self.assertTrue(all(Path(source).parent == Path(directory)
                                for source in sources))
            self.assertEqual(json.loads(Path(path).read_text(encoding="utf-8")),
                             {"writer": 2})

    def test_pick_server_restores_saved_job(self):
        with tempfile.TemporaryDirectory() as day:
            state = {
                "status": "done", "pid": None, "total": 2,
                "tasks": [{"word": "alpha", "status": "done"},
                          {"word": "beta", "status": "done"}],
            }
            Path(day, pick.JOB_STATE_NAME).write_text(
                json.dumps(state), encoding="utf-8"
            )
            server = pick.PickServer("page", day, True, 2)
            payload = server.status_payload()
        self.assertEqual(server.selected_words, ["alpha", "beta"])
        self.assertEqual(payload["status"], "done")
        self.assertEqual(payload["total"], 2)

    def test_active_saved_job_prevents_duplicate_submission(self):
        with tempfile.TemporaryDirectory() as day, patch.object(
            pick, "process_is_running", return_value=True
        ):
            Path(day, pick.JOB_STATE_NAME).write_text(json.dumps({
                "status": "running", "pid": 123,
                "tasks": [{"word": "alpha", "status": "running"}],
            }), encoding="utf-8")
            server = pick.PickServer("page", day, True, 2)
            with self.assertRaises(pick.SubmissionInProgressError):
                server.submit([{"word": "beta"}])

    def test_result_names_do_not_collide(self):
        with tempfile.TemporaryDirectory() as output:
            with patch.object(smd.time, "time_ns", side_effect=[100, 200]):
                first = smd.save_result(output, "word", "", "", "one", 0.1, "a", "test")
                second = smd.save_result(output, "word", "", "", "two", 0.1, "b", "test")
            self.assertNotEqual(first, second)
            self.assertEqual(Path(first).read_text(encoding="utf-8").count("one"), 1)
            self.assertEqual(Path(second).read_text(encoding="utf-8").count("two"), 1)

    def test_pdf_checkpoint_is_not_saved_when_article_write_fails(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as pdf:
            state = {"pdf": {}}
            with patch.object(prep, "load_state", return_value=state), patch.object(
                prep, "pdftotext_all", return_value="page one\fpage two"
            ), patch.object(prep, "write_article", side_effect=OSError("disk full")), patch.object(
                prep, "save_state"
            ) as save_state:
                with self.assertRaises(OSError):
                    prep.prep_pdf(pdf.name, 1)
            save_state.assert_not_called()
            self.assertEqual(state["pdf"], {})


if __name__ == "__main__":
    unittest.main()

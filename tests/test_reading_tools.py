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


class ReadingToolTests(unittest.TestCase):
    def test_only_read_starts_browser_workflow(self):
        with patch.object(sys, "argv", ["daily.py", "--only-read"]), patch.object(
            daily, "run", return_value=0
        ) as run:
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

#!/usr/bin/env python3
"""Build self-contained plugin packages from the canonical skill directories."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
REPOSITORY = "https://github.com/Raycc-lang/prompts-skills"
PLUGINS = {
    "ray-prompt-wording": {
        "display_name": "Ray's Prompt Wording",
        "description": "Refine prompt wording, clarify agent objectives and completion, and diagnose failures.",
        "prompts": [
            "Make this prompt clearer and more concise while preserving my meaning.",
            "Help define the objective and completion criteria for this agent prompt.",
        ],
    },
    "focused-teaching": {
        "display_name": "Focused Teaching",
        "description": "Learn through clear explanations, worked contrasts, and practice adapted to your understanding.",
        "prompts": [
            "Explain the distinction I am missing, building on what I already understand.",
            "Teach me this concept with worked examples, then guide me through practice.",
        ],
    },
    "jiangou-learning-analysis": {
        "display_name": "Jiangou Learning Analysis",
        "description": "Break down a chosen learning direction into abilities, suitable practice, and progress checks.",
        "prompts": [
            "I have chosen what to learn. Break it into sub-skills and a practical learning sequence.",
            "Analyze this learning difficulty and propose targeted practice and checks.",
        ],
    },
}


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def plugin_files(name: str, config: dict) -> dict[Path, bytes]:
    source = ROOT / "skills" / name
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"Missing canonical skill: {source}")
    files = {}
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Package sources must be regular files: {path}")
        if path.is_file():
            files[Path("skills") / name / path.relative_to(source)] = path.read_bytes()
    interface = {
        "displayName": config["display_name"],
        "shortDescription": config["description"],
        "longDescription": config["description"],
        "developerName": "Ray",
        "category": "Productivity",
        "defaultPrompt": config["prompts"],
        "composerIcon": "./assets/icon.svg",
        "logo": "./assets/icon.svg",
    }
    identity = {
        "name": name,
        "version": VERSION,
        "description": config["description"],
        "author": {"name": "Ray", "url": "https://github.com/Raycc-lang"},
        "repository": REPOSITORY,
    }
    files[Path("plugin.json")] = encoded({
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        **identity,
        "extensions": {"com.openai": {"interface": interface}},
    })
    files[Path(".codex-plugin/plugin.json")] = encoded({
        **identity, "skills": "./skills/", "interface": interface,
    })
    files[Path("assets/icon.svg")] = (source / "assets/icon.svg").read_bytes()
    return files


def expected_files() -> dict[Path, bytes]:
    files = {}
    for name, config in PLUGINS.items():
        files.update({Path("plugins") / name / path: data
                      for path, data in plugin_files(name, config).items()})
    files[Path(".agents/plugins/marketplace.json")] = encoded({
        "name": "ray-prompts-skills",
        "interface": {"displayName": "Ray's Prompt and Learning Skills"},
        "plugins": [
            {
                "name": name,
                "source": {"source": "local", "path": f"./plugins/{name}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }
            for name in PLUGINS
        ],
    })
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated packages without writing")
    args = parser.parse_args()
    expected = expected_files()
    stale = [str(path) for path, data in expected.items()
             if not (ROOT / path).is_file() or (ROOT / path).read_bytes() != data]
    extra = []
    for name in PLUGINS:
        directory = ROOT / "plugins" / name
        if directory.exists():
            extra.extend(str(p.relative_to(ROOT)) for p in directory.rglob("*")
                         if p.is_file() and p.relative_to(ROOT) not in expected)
    if args.check:
        if stale or extra:
            for path in stale: print(f"Missing or stale: {path}", file=sys.stderr)
            for path in extra: print(f"Unexpected: {path}", file=sys.stderr)
            return 1
        print(f"Verified {len(PLUGINS)} plugins: packaged skills match canonical sources.")
        return 0
    # The three plugin directories contain generated files only; remove stale files.
    for relative in extra:
        (ROOT / relative).unlink()
    for relative, data in expected.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f"Built {len(PLUGINS)} plugins and the repository marketplace.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

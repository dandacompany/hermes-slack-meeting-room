#!/usr/bin/env python3
"""Validate the hermes-slack-meeting-room skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


REQUIRED_FILES = [
    "SKILL.md",
    "assets/hermes-meeting/SKILL.md",
    "assets/templates/profile-config-snippets.yaml",
    "assets/templates/channel-prompts.yaml",
    "assets/templates/tts-options.yaml",
    "references/distribution.md",
    "references/plugin-boundary.md",
    "references/slack-checklist.md",
    "references/troubleshooting.md",
    "scripts/validate_setup.py",
]

SECRET_PATTERNS = [
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"xapp-[A-Za-z0-9-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{24,}"),
]


def check_frontmatter(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return [f"{path}: missing YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return [f"{path}: unterminated YAML frontmatter"]
    if yaml is None:
        return []
    data = yaml.safe_load(text[4:end]) or {}
    errors = []
    for key in ("name", "description"):
        if not data.get(key):
            errors.append(f"{path}: missing frontmatter key '{key}'")
    return errors


def check_yaml(path: Path) -> list[str]:
    if yaml is None:
        return []
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: YAML parse error: {exc}"]
    return []


def scan_secrets(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    errors = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path}: possible secret detected")
            break
    return errors


def main() -> int:
    root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path.cwd()
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    if (root / "SKILL.md").exists():
        errors.extend(check_frontmatter(root / "SKILL.md"))
    if (root / "assets/hermes-meeting/SKILL.md").exists():
        errors.extend(check_frontmatter(root / "assets/hermes-meeting/SKILL.md"))

    for yaml_file in (root / "assets/templates").glob("*.yaml"):
        errors.extend(check_yaml(yaml_file))

    for file_path in root.rglob("*"):
        if file_path.is_file():
            errors.extend(scan_secrets(file_path))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

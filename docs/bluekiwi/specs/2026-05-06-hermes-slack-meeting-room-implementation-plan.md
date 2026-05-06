# Hermes Slack Meeting Room Skill Implementation Plan

## MVP

MVP goal: a user can install the `hermes-slack-meeting-room` skill, follow its workflow, customize three additional Hermes profiles, choose TTS options, complete Slack setup manually with guidance, and run the first `/meeting` smoke test.

## Dependency Map

```text
Package skeleton
  -> Skill instructions
  -> Reference docs + templates
  -> Validation script
  -> Local validation
  -> Install/distribution verification
  -> Final review
```

## Phase 1. Package Skeleton

Work:

- Create repository-level README.
- Create Hermes skill folder under `skills/hermes-slack-meeting-room/`.
- Create subfolders for assets, references, scripts, and docs.

Files:

- `README.md`
- `skills/hermes-slack-meeting-room/`
- `docs/bluekiwi/specs/`

Dependencies: none.

Verification:

```bash
find . -maxdepth 5 -type f | sort
```

Status: complete.

## Phase 2. Skill Instructions

Work:

- Write the main `SKILL.md`.
- Define trigger conditions, operating rules, Socratic setup workflow, TTS selection, Slack checklist handoff, template generation, validation, and smoke tests.
- Keep Slack UI work explicitly manual/guided.

Files:

- `skills/hermes-slack-meeting-room/SKILL.md`

Dependencies:

- Phase 1.

Verification:

- Frontmatter has `name` and `description`.
- No real Slack IDs, tokens, or server-specific values.
- Skill body references bundled assets and references by relative path.

Status: complete.

## Phase 3. References And Templates

Work:

- Add Slack UI checklist.
- Add troubleshooting guide.
- Add Hermes profile config snippets.
- Add channel prompt templates.
- Add TTS option template.
- Add installable `hermes-meeting` moderator skill asset.

Files:

- `skills/hermes-slack-meeting-room/references/slack-checklist.md`
- `skills/hermes-slack-meeting-room/references/troubleshooting.md`
- `skills/hermes-slack-meeting-room/assets/templates/profile-config-snippets.yaml`
- `skills/hermes-slack-meeting-room/assets/templates/channel-prompts.yaml`
- `skills/hermes-slack-meeting-room/assets/templates/tts-options.yaml`
- `skills/hermes-slack-meeting-room/assets/hermes-meeting/SKILL.md`

Dependencies:

- Phase 1.

Verification:

```bash
python3 skills/hermes-slack-meeting-room/scripts/validate_setup.py skills/hermes-slack-meeting-room
```

Status: complete.

## Phase 4. Validation Script

Work:

- Add a standard-library validation script.
- Check required files.
- Check `SKILL.md` frontmatter.
- Parse YAML when PyYAML is available.
- Scan common token/API key patterns.

Files:

- `skills/hermes-slack-meeting-room/scripts/validate_setup.py`

Dependencies:

- Phase 1.
- Phase 2.
- Phase 3.

Verification:

```bash
chmod +x skills/hermes-slack-meeting-room/scripts/validate_setup.py
python3 skills/hermes-slack-meeting-room/scripts/validate_setup.py skills/hermes-slack-meeting-room
```

Status: complete.

## Phase 5. Local Validation

Work:

- Run package validator.
- Parse YAML templates with the Hermes Python environment.
- Run grep-based secret scan.
- Run Hermes Skills Guard scan.

Files:

- All files under `skills/hermes-slack-meeting-room/`.

Dependencies:

- Phase 4.

Verification:

```bash
python3 skills/hermes-slack-meeting-room/scripts/validate_setup.py skills/hermes-slack-meeting-room
/Users/dante/.hermes/hermes-agent/venv/bin/python - <<'PY'
from pathlib import Path
import yaml
for p in Path('skills/hermes-slack-meeting-room/assets/templates').glob('*.yaml'):
    yaml.safe_load(p.read_text())
    print('ok', p)
PY
rg -n "xox[baprs]-[A-Za-z0-9-]{20,}|xapp-[A-Za-z0-9-]{20,}|sk-[A-Za-z0-9_-]{20,}" .
```

Status: complete.

## Phase 6. Install And Distribution Verification

Work:

- Verify local install instructions.
- Verify expected GitHub tap layout.
- Document direct GitHub identifier and tap install paths.
- If a remote repo is chosen later, replace `<owner>/<repo>` placeholders.

Files:

- `README.md`
- `skills/hermes-slack-meeting-room/SKILL.md`

Dependencies:

- Phase 5.

Verification:

```bash
hermes skills install <owner>/<repo>/skills/hermes-slack-meeting-room
hermes skills tap add <owner>/<repo>
hermes skills search "hermes slack meeting"
```

Status: pending remote repository decision.

## Phase 7. Coming Soon

Work:

- Add optional helper script that generates profile matrices from an answers file.
- Add optional plugin notes for Hermes-internal `/meeting` routing and TTS metadata filtering.
- Prepare a public registry submission after repeated successful installs.

Files:

- Future `scripts/generate_profile_matrix.py`
- Future `references/plugin-boundary.md`

Dependencies:

- MVP usage feedback.

Verification:

- New helper scripts must pass local validation.
- Plugin boundary notes must clearly state Slack UI steps cannot be automated by a plugin.

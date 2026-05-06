# Hermes Slack Meeting Room Skill

Hermes Slack multi-profile meeting rooms can be hard to set up because the work crosses Hermes profiles, Slack apps, slash commands, gateway services, channel prompts, and TTS settings.

This repository packages a Hermes skill that guides that setup as a workflow:

- Start after Codex and Hermes Agent are installed.
- Assume one base Hermes profile already exists.
- Create three additional meeting profiles by default.
- Let the user customize each profile's name, role, personality, Slack app display name, allowed channels, and TTS voice.
- Guide Slack UI steps that cannot be automated by a Hermes plugin.
- Generate deterministic Hermes templates and validation commands.

## Install

Direct GitHub identifier install:

```bash
hermes skills install <owner>/<repo>/skills/hermes-slack-meeting-room
```

GitHub tap install:

```bash
hermes skills tap add <owner>/<repo>
hermes skills search "hermes slack meeting"
hermes skills install <identifier-shown-by-search>
```

Local install while developing:

```bash
mkdir -p ~/.hermes/skills/hermes-slack-meeting-room
cp -R skills/hermes-slack-meeting-room/* ~/.hermes/skills/hermes-slack-meeting-room/
hermes skills check
```

## Package

```text
skills/hermes-slack-meeting-room/
  SKILL.md
  assets/
    hermes-meeting/SKILL.md
    templates/
  references/
    distribution.md
    plugin-boundary.md
    slack-checklist.md
    troubleshooting.md
  scripts/
    validate_setup.py
```

## Default Rollout

The default rollout is one base Manager profile plus three additional profiles. The three profiles are not fixed. The skill asks the user what profiles and personalities they want, then offers starter presets only when helpful.

TTS choices should include Hermes built-in providers detected in the target install and Typecast candidate voices when available. Edge TTS remains the lowest-friction default.

Do not use a raw `SKILL.md` URL for this package. Hermes raw URL installs are single-file installs; this skill needs its bundled `assets/`, `references/`, and `scripts/`.

## Validate

```bash
python3 skills/hermes-slack-meeting-room/scripts/validate_setup.py skills/hermes-slack-meeting-room
```

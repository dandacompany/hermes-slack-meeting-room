# Hermes Slack Meeting Room Skill

Hermes Slack multi-profile meeting rooms can be hard to set up because the work crosses Hermes profiles, Slack apps, slash commands, gateway services, channel prompts, and TTS settings.

This repository packages a Hermes skill that guides that setup as a workflow:

- Start after Codex and Hermes Agent are installed.
- Assume one base Hermes profile already exists.
- Create three additional meeting profiles by default.
- Let the user customize each profile's aligned Hermes profile name, Slack app display name, persona, allowed channels, and TTS voice.
- Include built-in business persona presets such as Marketer, Product, Backend, Frontend, Designer, UX, QA, Researcher, Data, Planner, Consultant, Finance, Sales, Success, Legal, Security, Ops, People, and Contents.
- Guide Slack UI steps that cannot be automated by a Hermes plugin.
- Generate deterministic Hermes templates and validation commands.

## Install

Direct GitHub identifier install:

```bash
hermes skills install dandacompany/hermes-slack-meeting-room/skills/hermes-slack-meeting-room
```

GitHub tap install:

```bash
hermes skills tap add dandacompany/hermes-slack-meeting-room
hermes skills search "hermes slack meeting"
hermes skills install hermes-slack-meeting-room
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
      business-persona-presets.yaml
  references/
    distribution.md
    plugin-boundary.md
    slack-checklist.md
    troubleshooting.md
  scripts/
    validate_setup.py
```

## Default Rollout

The default rollout is one base Manager profile plus three additional profiles. The three profiles are not fixed. The skill asks the user what profiles and personas they want, including name, job/role, personality, values, speaking style, background, decision lens, and avoided behaviors.

For business users, the skill can recommend presets from `assets/templates/business-persona-presets.yaml` based on the meeting goal and deliverable. Users can select presets as-is, mix them, or customize every persona field.

TTS choices should include Hermes built-in providers detected in the target install and Typecast candidate voices when available. Edge TTS remains the lowest-friction default.

Do not use a raw `SKILL.md` URL for this package. Hermes raw URL installs are single-file installs; this skill needs its bundled `assets/`, `references/`, and `scripts/`.

## Tutorial

- [Installation and usage guide](docs/tutorial-hermes-slack-meeting-room/tutorial-hermes-slack-meeting-room.md)
- [Static HTML tutorial](docs/tutorial-hermes-slack-meeting-room/tutorial-hermes-slack-meeting-room.html)

Regenerate the HTML tutorial after editing the source:

```bash
python3 docs/tutorial-hermes-slack-meeting-room/build_tutorial_hermes_slack_meeting_room.py
```

## Validate

```bash
python3 skills/hermes-slack-meeting-room/scripts/validate_setup.py skills/hermes-slack-meeting-room
```

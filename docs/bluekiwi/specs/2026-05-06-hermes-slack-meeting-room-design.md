# Hermes Slack Meeting Room Skill Design

## 1. Overview

This project creates a Hermes skill named `hermes-slack-meeting-room`.

The skill guides a user from a fresh Codex + Hermes Agent + Slack workspace baseline to a working Slack-Hermes multi-profile meeting room. It assumes one base Hermes profile already exists and guides the user to create three additional participant profiles by default.

The problem is not only a Hermes config problem. It crosses Slack app setup, profile-specific gateway tokens, slash commands, channel prompts, TTS provider selection, and meeting moderation rules. The skill therefore acts as a workflow coach: it asks the user for profile/personality choices, guides unavoidable Slack UI steps, and keeps deterministic setup in templates and validation scripts.

## 2. Architecture

The package is distributed as a Hermes skill folder:

```text
skills/hermes-slack-meeting-room/
  SKILL.md
  assets/
    hermes-meeting/SKILL.md
    templates/
  references/
    slack-checklist.md
    troubleshooting.md
  scripts/
    validate_setup.py
```

Main components:

- `Setup Coach`: asks for the base moderator profile and three additional profile names, roles, personalities, Slack app display names, channel policy, and TTS choices.
- `Template Builder`: converts the approved profile matrix into Hermes profile config snippets, channel prompts, and the `hermes-meeting` skill install plan.
- `Slack Checklist`: guides app creation, scopes, events, Socket Mode, slash command setup, reinstall, tokens, and channel invitation.
- `Validator`: checks required files, frontmatter, YAML templates, secret patterns, Hermes config health, and smoke-test readiness.

Data flow:

```text
user answers
-> profile matrix
-> template placeholder replacement
-> Hermes profile config and skill files
-> gateway restart
-> Slack text smoke test
-> optional TTS smoke test
```

## 3. Interfaces

User-facing trigger examples:

```text
Use the hermes-slack-meeting-room skill to set up a Slack meeting room.
Hermes Slack 회의실을 만들자.
/meeting을 쓸 수 있는 멀티프로필 Hermes Slack 회의방을 설정해줘.
```

Distribution interfaces:

```bash
hermes skills install <owner>/<repo>/skills/hermes-slack-meeting-room
hermes skills tap add <owner>/<repo>
hermes skills search "hermes slack meeting"
hermes skills install <identifier-shown-by-search>
```

Raw `SKILL.md` URL install is intentionally not used because Hermes treats bare markdown URLs as single-file skills, while this package requires bundled assets, references, and scripts.

Validation interface:

```bash
python3 ~/.hermes/skills/hermes-slack-meeting-room/scripts/validate_setup.py ~/.hermes/skills/hermes-slack-meeting-room
```

Hermes meeting interface:

```text
/meeting 테스트 회의, 3턴, text-only
/meeting 제품 전략 회의, 6턴, voice-summary
```

## 4. Error Handling

Common failures are documented in `references/troubleshooting.md`.

- Slack app did not respond: check gateway status, Socket Mode, tokens, reinstall, and logs.
- Unknown `/meeting`: register `/meeting` only on the Manager/base app and reinstall that app.
- App is DMs only: set `slack.dm_only: false` in the relevant profile.
- Bot cannot see the channel: verify invitation, scopes, events, and channel allowlist.
- Every profile answers at once: enforce Manager-led routing and participant handoff rules.
- TTS reads metadata: keep `[MEETING]`, `handoff:`, mentions, and routing metadata outside voice-facing text.

## 5. Test Strategy

Automated checks:

- Run `scripts/validate_setup.py`.
- Parse YAML templates with the Hermes Python environment.
- Run grep-based secret scan for Slack/provider token patterns.
- Run Hermes Skills Guard scan before publishing.

Hermes checks:

```bash
hermes config check
hermes doctor
hermes skills check
hermes --profile <profile> config check
```

Manual Slack smoke tests:

1. Invite Manager and all three profile apps to a test channel.
2. Mention each app directly and verify one response.
3. Run `/meeting 테스트 회의, 3턴, text-only`.
4. Confirm Manager asks setup questions before routing.
5. Confirm sequential handoff returns to Manager.
6. Run `/meeting 테스트 회의, 3턴, voice-summary`.
7. Confirm TTS speaks only meeting content and not metadata.

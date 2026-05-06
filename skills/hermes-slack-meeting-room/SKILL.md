---
name: hermes-slack-meeting-room
description: Guide users through setting up a Slack-Hermes multi-profile meeting room after Codex and Hermes Agent are installed. Use when the user wants /meeting, moderator-led multi-agent Slack meetings, profile/personality setup, Slack app checklists, Hermes profile config templates, or TTS voice selection for Hermes meetings.
version: 0.1.0
author: Dante Labs
license: MIT
platforms: [macos, linux]
prerequisites:
  commands: [hermes, python3]
metadata:
  hermes:
    tags: [Hermes, Slack, Meetings, Multi-Agent, TTS]
    requires_toolsets: [terminal]
---

# Hermes Slack Meeting Room Setup

Use this skill to guide a user from a fresh Hermes installation to a working Slack meeting room where one moderator profile coordinates several Hermes participant profiles.

## Operating Rules

- Start from this baseline: Codex is available, Hermes Agent is installed, one base Hermes profile can run, and the user has a Slack workspace.
- Do not assume any local server name, Slack channel ID, Slack user ID, token, or profile name.
- Never print full Slack, Typecast, ElevenLabs, or provider tokens. Redact secrets in reports.
- Prefer deterministic steps: copy templates, edit config files, run validation, restart services, and run smoke tests.
- Treat Slack app creation, OAuth scopes, Socket Mode, app reinstall, token generation, slash command setup, and channel invitation as guided user actions.
- Default to one base Manager profile plus three additional participant profiles, but make every profile name, role, persona, channel policy, and TTS voice user-configurable.
- Keep each Hermes profile name, Slack app display name, and human-facing persona name intentionally aligned unless the user explicitly chooses an exception.
- Edge TTS is the lowest-friction default. Also present Hermes built-in TTS providers discovered on the target install and Typecast voice candidates when available.

## Workflow

### 1. Baseline Check

Run:

```bash
hermes --version
hermes update --check
hermes config check
hermes profile list
hermes skills list
```

If Hermes is not installed or the base profile cannot run, pause and fix that before continuing.

### 2. Socratic Profile Design

Ask concise questions and build a profile matrix. Do not ask the user to edit YAML at this stage.

Required fields:

- Base moderator profile name
- Three additional profile names
- Naming convention for each profile:
  - Hermes profile id, for example `contents`
  - Slack app display name, for example `Hermes Contents`
  - Persona display name, for example `Contents`
  - Default rule: keep these names recognizably identical across Hermes config, Slack app, and meeting prompts.
- Each profile's role specialization
- Each profile's persona card:
  - Name
  - Role/job
  - Personality traits
  - Values and priorities
  - Speaking style and tone
  - Background/context
  - Decision lens
  - Avoided behaviors or forbidden style
- Meeting channel policy
- TTS provider and voice for each profile

Ask the user to customize these persona cards instead of forcing fixed presets. For business users, read `assets/templates/business-persona-presets.yaml` and offer either:

- Recommended personas based on the user's meeting goal, industry, and deliverable
- A short selectable list of built-in personas
- Fully custom personas when the user already knows what they want

Built-in business persona examples:

| Preset | Use |
| --- | --- |
| Manager | Facilitation, turn control, Socratic setup |
| Marketer | Positioning, campaign, funnel, customer message |
| Product | Product strategy, PRD, roadmap, prioritization |
| Backend | API, database, reliability, security-sensitive architecture |
| Frontend | UI implementation, state, accessibility, performance |
| Designer | Brand, visual hierarchy, presentation polish |
| UX | User flow, usability, onboarding, friction points |
| QA | Test plans, regression, reproducible failure cases |
| Researcher | Market/user research, evidence quality, assumptions |
| Data | Metrics, dashboards, experiments, analytical caveats |
| Planner | Business plans, proposals, operating plans |
| Consultant | Executive framing, options, tradeoffs, recommendations |
| Finance | Budget, ROI, valuation, downside risk, unit economics |
| Sales | Pitch, objection handling, discovery, account strategy |
| Success | Onboarding, retention, customer health, renewal |
| Legal | Compliance, privacy, contracts, claims risk |
| Security | Threat modeling, permissions, secrets, attack surface |
| Ops | Process, SOP, ownership, repeatable operations |
| People | Hiring, team health, feedback, org communication |
| Contents | YouTube, scripts, tutorials, editorial strategy |

Confirm the final matrix before file edits. The confirmation must show profile id, Slack app display name, persona name, role, speaking style, and TTS choice for every profile.

### 3. TTS Selection

Start with the user's target Hermes install. Ask Codex to inspect available Hermes voice/TTS commands or config docs when possible. Present:

- Hermes built-in/free providers available in that install
- Provider-specific requirements
- Typecast candidates if the user has a Typecast API key or voice list
- Voice mode: `text-only`, `voice-summary`, `voice-full`, or `hybrid`

Default recommendation:

```yaml
voice:
  auto_tts: false
tts:
  provider: edge
```

Use Typecast or ElevenLabs only after text meeting flow passes.

### 4. Slack Checklist

Read `references/slack-checklist.md` when Slack app setup begins.

For each profile-specific Slack app, guide the user through:

- App manifest or manual app creation
- Bot scopes
- Event subscriptions
- App Home DM enablement
- Socket Mode
- Slash command registration
- Reinstall to workspace
- Token placement in the correct profile `.env`
- App invitation to the meeting channel

Register `/meeting` only on the Manager/base app by default.

### 5. Generate Templates

Use bundled assets:

- `assets/templates/profile-config-snippets.yaml`
- `assets/templates/business-persona-presets.yaml`
- `assets/templates/channel-prompts.yaml`
- `assets/templates/tts-options.yaml`
- `assets/hermes-meeting/SKILL.md`

Replace placeholders with the confirmed profile matrix. Keep generated files in a staging folder first, then apply them to Hermes config paths only after user approval.

### 6. Install Hermes Meeting Skill

Copy or merge `assets/hermes-meeting/SKILL.md` into:

```bash
~/.hermes/skills/hermes-meeting/SKILL.md
```

For profile-isolated installs, copy it into each profile's active skills directory if that Hermes version requires per-profile skills.

### 7. Validate

Run the bundled validation script against the staged package or copied install:

```bash
python3 ~/.hermes/skills/hermes-slack-meeting-room/scripts/validate_setup.py ~/.hermes/skills/hermes-slack-meeting-room
```

Then run Hermes checks:

```bash
hermes config check
hermes doctor
hermes skills check
```

For each profile:

```bash
hermes --profile <profile> config check
```

Restart gateway services only after config validation passes.

### 8. Slack Smoke Tests

Test in a dedicated Slack channel first.

1. Invite every profile app to the test channel.
2. Send a direct mention to each app.
3. Run text-only meeting setup:

```text
/meeting 테스트 회의, 3턴, text-only
```

4. Confirm the Manager asks setup questions before mentioning participants.
5. Confirm sequential handoff works.
6. Enable voice only after the text meeting passes:

```text
/meeting 테스트 회의, 3턴, voice-summary
```

7. Confirm TTS does not speak metadata such as `[MEETING]`, `handoff:`, `round`, `next`, or participant mentions.

## Troubleshooting

Read `references/troubleshooting.md` when Slack says the app did not respond, `/meeting` is unknown, the app is configured for DMs only, a bot does not see the channel, or TTS speaks routing metadata.

Read `references/plugin-boundary.md` if the user asks whether this should be a Hermes plugin instead of a skill.

## Distribution

Read `references/distribution.md` when preparing the skill for testers, GitHub tap installation, or public registry submission.

Do not rely on a Hermes plugin as the primary onboarding path. A plugin can later automate Hermes-internal routing, TTS filtering, and smoke-test helpers, but it cannot create Slack apps, scopes, tokens, Socket Mode, workspace reinstall, or channel invitations.

# Plugin Boundary

A Hermes plugin can improve the meeting-room experience after Slack apps and profile gateways exist, but it is not the right primary onboarding mechanism.

## Good Plugin Responsibilities

- Route `/meeting` payloads into the `hermes-meeting` skill.
- Normalize meeting state blocks.
- Filter TTS metadata so only meeting content is spoken.
- Provide smoke-test commands for gateway/profile health.
- Generate or update channel prompts from a confirmed profile matrix.
- Expose a dashboard view of meeting participants, channel allowlists, and voice modes.

## Not Plugin Responsibilities

These require Slack UI or workspace permissions and should remain checklist-guided:

- Creating Slack apps.
- Granting OAuth scopes.
- Enabling Socket Mode.
- Creating app-level tokens.
- Reinstalling apps to a workspace.
- Inviting bot users to channels.
- Approving workspace-level app permissions.

## Recommended Path

Use this skill first. Once a team has repeated the setup successfully, consider a plugin for Hermes-internal automation and maintenance.


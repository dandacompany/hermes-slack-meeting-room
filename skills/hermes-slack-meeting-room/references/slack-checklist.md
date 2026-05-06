# Slack Checklist

Use this checklist for each Hermes profile Slack app.

## App Creation

- Create one Slack app per Hermes profile.
- Keep app display names aligned with profile names.
- Use one visible naming convention across all surfaces:
  - Hermes profile id: `contents`
  - Slack app display name: `Hermes Contents`
  - Persona display name in prompts: `Contents`
- Do not create a Slack app display name that hides which Hermes profile it belongs to. Meeting debugging depends on matching Slack messages back to profile config quickly.
- Use Socket Mode unless the user has a public HTTPS endpoint.
- Reinstall the app after every scope, event, or slash command change.

## Required Bot Scopes

Minimum public-channel setup:

```text
app_mentions:read
channels:history
channels:read
chat:write
commands
im:history
im:read
im:write
users:read
```

Private-channel setup also needs:

```text
groups:history
groups:read
```

If the app uploads audio files or voice artifacts, add the file scopes required by the active Hermes voice implementation.

## Event Subscriptions

Enable:

```text
app_mention
message.channels
message.im
```

For private channels:

```text
message.groups
```

## App Home

Turn on App Home messages and allow users to send messages to the app. This is required for DMs.

## Slash Commands

Register `/meeting` only on the Manager/base app by default.

```text
Command: /meeting
Description: Start a Hermes multi-profile meeting
Usage hint: topic, 6 turns, voice-summary
```

If the workspace requires a request URL even with Socket Mode, use the URL format expected by the installed Hermes Slack gateway docs or manifest generator.

## Tokens

Place tokens only in profile-specific `.env` files. Never paste tokens into chat, docs, GitHub, or screenshots.

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_ALLOWED_USERS=<SLACK_USER_ID_1>,<SLACK_USER_ID_2>
SLACK_HOME_CHANNEL=<OPTIONAL_HOME_CHANNEL_ID>
```

## Channel Setup

In the Slack meeting test channel:

```text
/invite @Hermes Manager
/invite @<Profile 1 App>
/invite @<Profile 2 App>
/invite @<Profile 3 App>
```

Confirm that every app is visibly a channel member before testing `/meeting`.

# Troubleshooting

## Slack says the app did not respond

Check:

```bash
hermes gateway status
hermes logs errors --since 30m
hermes config check
```

Likely causes:

- Gateway process is stopped or restarting.
- Socket Mode is off.
- App token is missing or belongs to another app.
- Bot token is missing or belongs to another app.
- Slash command was added but the app was not reinstalled.

## Unknown command `/meeting`

Likely causes:

- `/meeting` was registered on a different Slack app.
- Manager app was not reinstalled after command registration.
- The user is invoking `/meeting` in a workspace where that command is owned by another app.

Default fix: register `/meeting` only on the Manager/base app and reinstall it.

## App is configured for DMs only

Check the profile config:

```yaml
slack:
  dm_only: false
  require_mention: true
  strict_mention: true
```

Restart the gateway after changing config.

## Bot does not see channel messages

Check:

- App is invited to the channel.
- Public channel events include `message.channels`.
- Private channel events include `message.groups`.
- Scopes include `channels:history` or `groups:history`.
- The meeting channel is in the profile's allowlist or free-response channel list.

## Every profile answers at once

Use Manager-led routing:

- Participants answer only when directly mentioned by the Manager.
- Participants do not mention each other.
- Participants return to the Manager with `handoff: <@MANAGER_USER_ID>` in sequential mode.
- Free-response channels should be limited to trusted test/meeting channels.

## TTS reads metadata

Spoken content must exclude:

```text
[MEETING]
round:
speaker_done:
next:
handoff:
participant mentions
[PARALLEL-DONE]
```

Prefer `voice-summary` and ask participants to put only the spoken line after `음성 요약:`. If the gateway supports `[TTS]...[/TTS]`, wrap only speakable content in that block.

## Typecast or ElevenLabs does not speak

Check:

- API key exists in the right profile `.env`.
- Provider name matches the installed Hermes version.
- Voice ID belongs to the same account.
- Text meeting flow works before enabling voice.
- Gateway logs show no provider authentication or quota errors.

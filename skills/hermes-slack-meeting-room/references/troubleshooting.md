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
- Moderator app was not reinstalled after command registration.
- The user is invoking `/meeting` in a workspace where that command is owned by another app.

Default fix: register `/meeting` only on the moderator app and reinstall it.

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

## `/meeting` forgets context after the setup draft

Likely causes:

- The `/meeting` setup response was delivered as a Slack ephemeral slash-command reply.
- Slack is configured with `require_mention: true` and `strict_mention: true`.
- The user typed bare `시작` in the channel, so the bot ignored it or treated the next mention as a new top-level session.

Fix:

- In the moderator prompt, ask for `@<moderator> 시작` in the same channel/thread.
- Prefer a gateway `/meeting` approval bridge that remembers the same `(channel_id, user_id)` for a short TTL and accepts bare `시작`, `start`, `go`, `진행`, or `승인` as continuation.
- If no bridge exists, do not tell the user that plain `시작` is sufficient in strict-mention rooms.

## Every profile answers at once

Use moderator-led routing:

- Participants answer only when directly mentioned by the moderator.
- Participants do not mention each other.
- Participants return to the moderator with `handoff: <@MODERATOR_USER_ID>` in sequential mode.
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

## Slack uploads OGG instead of MP3

Likely cause: the TTS provider is configured with `voice_compatible: true`, which can convert generated MP3 into Opus/OGG for voice-bubble compatibility.

Fix for Slack meeting rooms:

- Set command-provider `output_format: mp3`.
- Set command-provider `voice_compatible: false` unless the platform explicitly requires Opus/OGG.
- Restart the gateway and run one `text_to_speech_tool` smoke test to confirm the returned file path ends in `.mp3`.

## Typecast or ElevenLabs does not speak

Check:

- API key exists in the right profile `.env`.
- Provider name matches the installed Hermes version.
- Voice ID belongs to the same account.
- Text meeting flow works before enabling voice.
- Gateway logs show no provider authentication or quota errors.

Do not paste provider keys into chat. Open the profile `.env` file and let the user edit it directly:

```bash
touch <PROFILE_ENV_FILE>
chmod 600 <PROFILE_ENV_FILE>
"${VISUAL:-${EDITOR:-nano}}" <PROFILE_ENV_FILE>
```

Confirm only that key names are present:

```bash
grep -E '^(TYPECAST_API_KEY|ELEVENLABS_API_KEY)=' <PROFILE_ENV_FILE> | sed 's/=.*/=<set>/'
```

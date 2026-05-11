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
- `/meeting` was implemented as a normal message bridge instead of a dedicated meeting session router.
- The user tried to continue the meeting through `@<moderator> ...`, which belongs to the normal Slack mention session.

Fix:

- Prefer the Block Kit `/meeting` UI described in `block-kit-meeting-ui.md`.
- Store meeting records separately from normal Slack sessions and route UI actions to a session key such as `meeting:<channel_id>:<meeting_id>`.
- Use the UI `시작`, `이어쓰기`, and `종료` actions for meeting continuation. Do not rely on normal `@<moderator> ...` messages to preserve meeting context.

## Every profile answers at once

Use moderator-led routing:

- Participants answer only when directly mentioned by the moderator.
- Participants do not mention each other.
- Participants return to the moderator with `handoff: @<MODERATOR_NAME>` in sequential mode, replacing `<MODERATOR_NAME>` with the moderator configured for that meeting.
- Free-response channels should be limited to trusted test/meeting channels.

## Participants do not answer moderator mentions

Likely causes:

- Participant profile `.env` allows only the human user's Slack id.
- `SLACK_ALLOW_BOTS` is missing or set to `none`.
- The moderator mentions the participant app, but Slack marks the sender as the moderator bot user.

Fix:

- Add every meeting bot user id to every profile's `SLACK_ALLOWED_USERS`.
- Set `SLACK_ALLOW_BOTS=mentions`, not `all`.
- Keep `SLACK_REQUIRE_MENTION=true` and `SLACK_STRICT_MENTION=true` so participants only answer explicit moderator mentions.
- Restart every profile gateway after changing `.env`.

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

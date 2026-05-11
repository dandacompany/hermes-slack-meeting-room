# Block Kit Meeting UI

Use this reference when `/meeting` should act like a Slack control surface instead of a plain text command.

## Goal

`/meeting` opens an ephemeral Block Kit meeting room for the invoking user. The UI controls all meeting lifecycle actions:

- Create a new meeting
- List existing meetings
- Start a setup-stage meeting
- Continue a meeting with a follow-up message
- Select the next speaker in manual routing mode
- End a meeting

Normal Slack mentions remain normal conversations. They do not continue meeting sessions.

## Session Model

Persist meeting metadata outside normal Slack message sessions:

```json
{
  "version": 1,
  "meetings": {
    "mtg-0511-101500": {
      "id": "mtg-0511-101500",
      "channel_id": "C...",
      "user_id": "U...",
      "title": "YouTube planning",
      "participants": ["<PARTICIPANT_NAME_1>", "<PARTICIPANT_NAME_2>"],
      "turns": "4",
      "mode": "mixed",
      "routing_mode": "auto",
      "voice_mode": "voice-summary",
      "status": "setup",
      "session_thread_id": "meeting:C...:mtg-0511-101500"
    }
  },
  "current": {
    "C...:U...": "mtg-0511-101500"
  }
}
```

The `session_thread_id` must be passed to the Hermes gateway source as the thread id. This keeps meeting context separate from normal `@moderator` Slack sessions.

## UI Flow

`/meeting` should render:

- Header: `Hermes Meeting Room`
- Explanation: meeting sessions are controlled by this UI and separated from normal mentions
- Primary button: `새 회의 시작`
- Refresh button: `새로고침`
- Existing meeting rows with status, title, participants, and actions

New meeting modal fields:

- Topic and goal
- Participants as a multi-select
- Turn count
- Mode: `mixed`, `sequential`, `parallel`, `directed`
- Routing control: `auto` immediately routes the next profile; `manual` waits for a user-selected next-speaker button
- Voice mode: `voice-summary`, `text-only`, `voice-full`, `hybrid`

Existing meeting actions:

- `시작`: send `시작` to the dedicated meeting session
- `이어쓰기`: open a modal and send the submitted message to the dedicated meeting session
- `다음: <profile>`: in manual routing mode, ask the moderator in the dedicated meeting session to route one turn to that profile
- `종료`: send a finalization request and mark the meeting ended

## Prompt Contract

When the UI creates a meeting, dispatch a command-style event to Hermes:

```text
/meeting <topic>

참석자: <PARTICIPANT_NAME_1>, <PARTICIPANT_NAME_2>
턴수: 4턴
진행: mixed
진행 제어: auto
음성: voice-summary
세션: 이 회의는 Slack Block Kit `/meeting` UI에서 생성된 전용 meeting 세션입니다. 일반 @멘션 대화와 분리해서 진행하고, 시작/이어쓰기/종료/다음 발언자 선택은 `/meeting` UI 액션으로만 받습니다. 먼저 setup 초안을 보여주고 참가자를 멘션하지 마세요.
```

The moderator must not instruct the user to continue via normal `@moderator` messages when the UI is installed.
In auto routing, the moderator must immediately call exactly one next participant. In manual routing, the moderator must wait for the UI next-speaker action and must not auto-route participants.

## Slack Requirements

The moderator Slack app must have:

- Slash command `/meeting`
- Interactivity enabled
- Socket Mode enabled
- Bot scopes for channel messages and file uploads
- Channel membership in the meeting channel

Block Kit button and modal callbacks should use action ids and callback ids prefixed with `hermes_meeting_`.

## Bot-To-Bot Routing

Multi-profile meetings require bot-to-bot messages only for explicit moderator routing. Configure every profile environment with:

```bash
SLACK_ALLOWED_USERS=<HUMAN_USER_ID>,<MODERATOR_BOT_USER_ID>,<PARTICIPANT_BOT_USER_ID_1>,<PARTICIPANT_BOT_USER_ID_2>
SLACK_ALLOW_BOTS=mentions
SLACK_REQUIRE_MENTION=true
SLACK_STRICT_MENTION=true
SLACK_INJECT_BOT_MENTION_CONTEXT=true
```

Rules:

- Include every profile app's Slack bot user id, not just the human user's id.
- Keep `SLACK_ALLOW_BOTS=mentions`; do not use `all` for meeting rooms unless you intentionally want broad bot-message ingestion.
- Participants still answer only when the moderator explicitly mentions them.
- If a moderator writes `<PARTICIPANT_NAME> 1턴입니다.`, the gateway may rewrite that single routed line to the real Slack mention before sending.
- Do not print Slack user IDs or mention maps in user-visible warnings or setup messages.
- Profiles should receive recent meeting context on top-level bot-to-bot mentions so they can answer from the actual conversation, not only from the latest prompt.
- Normal unmentioned bot chatter remains ignored.

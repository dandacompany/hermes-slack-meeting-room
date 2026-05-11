# Block Kit Meeting UI

Use this reference when `/meeting` should act like a Slack control surface instead of a plain text command.

## Goal

`/meeting` opens an ephemeral Block Kit meeting room for the invoking user. The UI controls all meeting lifecycle actions:

- Create a new meeting
- List existing meetings
- Start a setup-stage meeting
- Continue a meeting with a follow-up message
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
      "participants": ["Grace", "Mike", "Sunny"],
      "turns": "4",
      "mode": "mixed",
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
- Voice mode: `voice-summary`, `text-only`, `voice-full`, `hybrid`

Existing meeting actions:

- `시작`: send `시작` to the dedicated meeting session
- `이어쓰기`: open a modal and send the submitted message to the dedicated meeting session
- `종료`: send a finalization request and mark the meeting ended

## Prompt Contract

When the UI creates a meeting, dispatch a command-style event to Hermes:

```text
/meeting <topic>

참석자: Grace, Mike, Sunny
턴수: 4턴
진행: mixed
음성: voice-summary
세션: 이 회의는 Slack Block Kit `/meeting` UI에서 생성된 전용 meeting 세션입니다. 일반 @멘션 대화와 분리해서 진행하고, 시작/이어쓰기/종료는 `/meeting` UI 액션으로만 받습니다. 먼저 setup 초안을 보여주고 참가자를 멘션하지 마세요.
```

The moderator must not instruct the user to continue via normal `@moderator` messages when the UI is installed.

## Slack Requirements

The moderator Slack app must have:

- Slash command `/meeting`
- Interactivity enabled
- Socket Mode enabled
- Bot scopes for channel messages and file uploads
- Channel membership in the meeting channel

Block Kit button and modal callbacks should use action ids and callback ids prefixed with `hermes_meeting_`.

---
name: hermes-meeting
description: Socratic moderator workflow for Hermes multi-profile Slack meetings. Use when /meeting is invoked or a user wants a structured multi-agent meeting.
---

# Hermes Meeting Moderator

The profile that receives `/meeting` is the meeting entrypoint. By default, the base Manager profile moderates the meeting.

## Setup First

Do not start by mentioning participants. First confirm:

- Meeting title
- Goal and expected output
- Participants
- Total speaking turns
- Mode: sequential, parallel, directed, or mixed
- Voice mode: text-only, voice-summary, voice-full, or hybrid
- User intervention rule
- Anti-convergence rule

Use:

```text
회의 설정 초안
제목: ...
목표/산출물: ...
참여자: ...
턴수: ...
진행: ...
음성: ...
개입: ...
합의 품질: ...

이 설정으로 시작할까요?
```

Only start when the user clearly approves.

## Routing

Sequential mode:

- Mention exactly one participant.
- Participant substantive replies count as turns.
- Moderator routing messages do not count as turns.
- Participants hand back with `handoff: <@MANAGER_USER_ID>`.

Parallel mode:

- Mention multiple participants once.
- Include: `병렬 응답: 서로를 멘션하지 말고, 끝에 handoff를 쓰지 말고, [PARALLEL-DONE]으로 끝내세요.`
- Summarize only after all expected participants respond or the user asks to summarize.

Directed mode:

- Use for a single targeted question to one profile.
- Return to the previous flow after that turn.

## Anti-Convergence

At halfway and before the final decision, ask for one of:

- Counterargument
- Failure scenario
- Missing stakeholder
- Weak assumption
- Metric or verification signal

If all participants converge too quickly, assign contrasting frames to the next turns.

## User Intervention

If the user speaks mid-meeting:

1. Pause routing.
2. Summarize the changed constraint in one sentence.
3. Revise the next speaker or mode.
4. Continue only after the change is reflected.

## Voice Modes

- `text-only`: no voice-specific formatting.
- `voice-summary`: participant adds one final `음성 요약:` sentence.
- `voice-full`: participant writes 2-4 natural spoken Korean sentences.
- `hybrid`: moderator states which turns are spoken.

TTS must speak only meeting content. Do not speak:

```text
[MEETING]
round:
speaker_done:
next:
handoff:
participant mentions
[PARALLEL-DONE]
```

If precise spoken content matters, wrap only that content:

```text
[TTS]
...
[/TTS]
```

## Ending

At the final turn, mention no participant. End with:

- Decision or synthesis
- Open questions
- Next actions
- `회의 종료`

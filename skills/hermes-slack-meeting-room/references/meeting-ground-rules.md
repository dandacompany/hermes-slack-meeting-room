# Meeting Ground Rules

Use these rules for every Hermes Slack multi-profile meeting room.

## Roles

- Manager/moderator owns the meeting state, speaker selection, mode changes, synthesis, and ending.
- Participants answer only when the Manager assigns them the floor.
- The user can override the meeting at any time.
- Participants do not coordinate directly with each other unless the Manager explicitly switches to a special mode that allows it.

## Setup Gate

The Manager must not mention participants until the user approves the setup draft.

Required setup fields:

```text
title:
goal:
expected_output:
participants:
total_turns:
mode: sequential | parallel | directed | mixed
voice_mode: text-only | voice-summary | voice-full | hybrid
user_intervention_rule:
anti_convergence_rule:
finish_condition:
```

If any required field is missing, ask one short clarifying question instead of starting the meeting.

## State Block

The Manager must maintain a compact state block on every routing, pause, resume, synthesis, or decision message.

```text
[MEETING]
id: <short-id>
status: setup | active | paused | waiting | ended
mode: sequential | parallel | directed | mixed
phase: framing | divergence | critique | synthesis | decision
turns: <counted>/<total>
current_speaker: <profile-or-none>
pending: <profiles-or-none>
completed: <profiles-or-none>
next: <profile-or-action>
last_event: <brief>
[/MEETING]
```

Routing and metadata do not count as meeting turns. Only substantive participant replies and final Manager synthesis count.

## Message Types

- `setup`: Manager asks for meeting configuration.
- `route`: Manager assigns the next speaker or group.
- `participant_turn`: A participant gives one substantive answer.
- `handoff`: A participant returns control to the Manager.
- `user_intervention`: The user changes topic, constraints, participants, mode, turn count, or asks to pause/stop.
- `synthesis`: Manager summarizes, compares, or updates the plan.
- `final`: Manager ends the meeting.
- `off_protocol`: Duplicate, late, cross-mention, or unassigned participant response.

## Mention Rules

- Only the Manager assigns speaking turns.
- In sequential and directed mode, the Manager mentions exactly one participant.
- In parallel mode, the Manager mentions the selected participants once in the same message.
- Participants never mention other participant apps.
- Participants mention only the Manager in `handoff`, and only when sequential or directed mode requires it.
- If a participant sees another participant's answer, it must not reply to that participant unless the Manager explicitly asked for cross-examination.
- If the user speaks, all participants remain silent until the Manager re-routes.

## Sequential Mode

Use sequential mode as the default.

1. Manager selects one participant.
2. Manager asks one bounded question.
3. The selected participant answers once.
4. The participant ends with `handoff: <@MANAGER_USER_ID>`.
5. Manager updates state and chooses the next action.

Do not assign the next participant until the expected participant has answered, the user intervenes, or the timeout policy is triggered.

## Parallel Mode

Use parallel mode only when the meeting needs divergent ideas or independent estimates.

Manager route message must include:

```text
병렬 응답: 서로를 멘션하지 말고, 끝에 handoff를 쓰지 말고, [PARALLEL-DONE]으로 끝내세요.
```

Manager waits until all expected participants respond, the user asks to continue, or the timeout policy triggers. Missing participants are listed as missing; their silence is not invented.

## Directed Mode

Use directed mode for one targeted question to one participant. Return to the previous mode after the answer unless the user or Manager explicitly changes the plan.

## Mixed Mode

Mixed mode must be declared with a short phase plan, for example:

```text
framing: Manager
divergence: parallel Marketer/Data/Researcher
critique: sequential QA/Security
synthesis: Manager
```

## Timeout And Duplicate Handling

If a participant does not answer in the expected window:

1. Manager marks the participant as `pending`.
2. Manager may retry once with a shorter prompt.
3. If still missing, Manager continues and records `missing: <profile>`.

If a participant answers twice for the same route, count only the first substantive answer. Treat the second as `off_protocol` unless the Manager asked for a revision.

If a late answer arrives after synthesis moved on, Manager can either ignore it or add a one-line correction. Do not reopen the meeting automatically.

## User Intervention

Classify user messages before continuing:

- `pause`: stop routing and wait.
- `stop`: end the meeting with current state.
- `revise`: change title, goal, participants, mode, voice mode, turn count, or constraints.
- `answer`: user provides missing information.
- `comment`: user adds context without changing the plan.
- `direct`: user asks a specific participant or the Manager a targeted question.

After any intervention:

1. Manager pauses routing.
2. Manager states the interpreted change in one sentence.
3. Manager updates the state block.
4. Manager continues only after the next action is clear.

## Anti-Convergence

Do not let the meeting collapse into agreement too early.

- At halfway, require one dissent checkpoint.
- Before final synthesis, require one risk or verification checkpoint.
- If all participants agree, the Manager assigns contrasting frames such as customer risk, technical risk, financial risk, legal risk, operational risk, or failure scenario.
- Participants must add at least one new reason, counterexample, condition, metric, or execution risk.

## Thread And Channel Behavior

- Follow the configured Slack surface. If the meeting started in a thread, stay in that thread. If it started in the channel root, keep routing in the channel root.
- Do not split one meeting across multiple channels or DMs.
- If a profile is not a channel member, stop and ask the user to invite it instead of continuing with a hidden participant.

## TTS Rules

TTS may speak only meeting content.

Never speak:

```text
[MEETING]
[/MEETING]
round:
speaker_done:
next:
handoff:
participant mentions
[PARALLEL-DONE]
```

If the gateway supports it, wrap the exact spoken content:

```text
[TTS]
...
[/TTS]
```

## Ending

The Manager ends the meeting when:

- Turn count is complete, or
- The user stops the meeting, or
- The finish condition is satisfied.

Final response format:

```text
결정/종합:
남은 질문:
다음 행동:
회의 종료
```

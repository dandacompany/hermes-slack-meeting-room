# Meeting Ground Rules

Use these rules for every Hermes Slack multi-profile meeting room.

## Roles

- Moderator owns the meeting state, speaker selection, mode changes, synthesis, and ending.
- Participants answer only when the moderator assigns them the floor.
- The user can override the meeting at any time.
- Participants do not coordinate directly with each other unless the moderator explicitly switches to a special mode that allows it.

## Setup Gate

The moderator must not mention participants until the user approves the setup draft.
In Slack workspaces with the Block Kit meeting UI, meeting setup and follow-up should be controlled by `/meeting` UI actions:

- `/meeting` opens a meeting room UI with new meeting, meeting list, start, continue, and end actions.
- New meeting, start, continue, and end actions must route to a dedicated meeting session key such as `meeting:<channel_id>:<meeting_id>`.
- Normal `@<moderator> ...` messages are ordinary Slack conversations and must not be treated as meeting continuation.
- Do not route participants until this approval is received.

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

The moderator must maintain a compact state block on every routing, pause, resume, synthesis, or decision message.

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

Routing and metadata do not count as meeting turns. Only substantive participant replies and final moderator synthesis count.

## Message Types

- `setup`: moderator asks for meeting configuration.
- `route`: moderator assigns the next speaker or group.
- `participant_turn`: A participant gives one substantive answer.
- `handoff`: A participant returns control to the moderator.
- `user_intervention`: The user changes topic, constraints, participants, mode, turn count, or asks to pause/stop.
- `synthesis`: moderator summarizes, compares, or updates the plan.
- `final`: moderator ends the meeting.
- `off_protocol`: Duplicate, late, cross-mention, or unassigned participant response.

## Mention Rules

- Only the moderator assigns speaking turns.
- In sequential and directed mode, the moderator mentions exactly one participant.
- In this Slack meeting-room setup, prefer one routed participant per message. Avoid parallel mode unless the gateway explicitly supports safe fan-out.
- In auto routing, the moderator immediately posts the next participant mention after the current turn is ready.
- In manual routing, the moderator waits for the `/meeting` UI next-speaker button and does not auto-mention participants.
- A participant route should use the visible profile name, for example `<PARTICIPANT_NAME> 1턴입니다.` The gateway may convert that single routing line to the real Slack mention internally.
- Do not ask the user for Slack user IDs and do not print mention maps or ID examples in warnings, explanations, code blocks, or checklists.
- Each participant route must include enough context to answer: current `[MEETING]` state, prior key points or decisions, and the specific question for that profile.
- Participants never mention other participant apps.
- Participants mention only the moderator in `handoff`, and only when sequential or directed mode requires it.
- If a participant sees another participant's answer, it must not reply to that participant unless the moderator explicitly asked for cross-examination.
- If the user speaks, all participants remain silent until the moderator re-routes.

## Sequential Mode

Use sequential mode as the default.

1. moderator selects one participant.
2. moderator asks one bounded question.
3. The selected participant answers once.
4. The participant ends with `handoff: @<MODERATOR_NAME>`.
5. moderator updates state and chooses the next action.

Do not assign the next participant until the expected participant has answered, the user intervenes, or the timeout policy is triggered.

## Parallel Mode

Use parallel mode only when the meeting needs divergent ideas or independent estimates.

moderator route message must include:

```text
병렬 응답: 서로를 멘션하지 말고, 끝에 handoff를 쓰지 말고, [PARALLEL-DONE]으로 끝내세요.
```

moderator waits until all expected participants respond, the user asks to continue, or the timeout policy triggers. Missing participants are listed as missing; their silence is not invented.

## Directed Mode

Use directed mode for one targeted question to one participant. Return to the previous mode after the answer unless the user or moderator explicitly changes the plan.

## Mixed Mode

Mixed mode must be declared with a short phase plan, for example:

```text
framing: moderator
divergence: parallel Marketer/Data/Researcher
critique: sequential QA/Security
synthesis: moderator
```

## Timeout And Duplicate Handling

If a participant does not answer in the expected window:

1. moderator marks the participant as `pending`.
2. moderator may retry once with a shorter prompt.
3. If still missing, moderator continues and records `missing: <profile>`.

If a participant answers twice for the same route, count only the first substantive answer. Treat the second as `off_protocol` unless the moderator asked for a revision.

If a late answer arrives after synthesis moved on, moderator can either ignore it or add a one-line correction. Do not reopen the meeting automatically.

## User Intervention

Classify user messages before continuing:

- `pause`: stop routing and wait.
- `stop`: end the meeting with current state.
- `revise`: change title, goal, participants, mode, voice mode, turn count, or constraints.
- `answer`: user provides missing information.
- `comment`: user adds context without changing the plan.
- `direct`: user asks a specific participant or the moderator a targeted question.

After any intervention:

1. moderator pauses routing.
2. moderator states the interpreted change in one sentence.
3. moderator updates the state block.
4. moderator continues only after the next action is clear.

## Anti-Convergence

Do not let the meeting collapse into agreement too early.

- At halfway, require one dissent checkpoint.
- Before final synthesis, require one risk or verification checkpoint.
- If all participants agree, the moderator assigns contrasting frames such as customer risk, technical risk, financial risk, legal risk, operational risk, or failure scenario.
- Participants must add at least one new reason, counterexample, condition, metric, or execution risk.

## Thread And Channel Behavior

- Follow the configured Slack surface. If the meeting started in a thread, stay in that thread. If it started in the channel root, keep routing in the channel root.
- Do not split one meeting across multiple channels or DMs.
- If a profile is not a channel member, stop and ask the user to invite it instead of continuing with a hidden participant.
- Slash-command setup replies may be ephemeral. If the Block Kit meeting UI is installed, the gateway must preserve durable meeting records and route UI actions to the dedicated meeting session, not to normal Slack mention sessions.

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

For Slack, MP3 should be the default uploaded audio format. Do not set command-provider `voice_compatible: true` for Slack unless the user explicitly wants an Opus/OGG voice-bubble workflow; that flag can convert MP3 into OGG.

## Ending

The moderator ends the meeting when:

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

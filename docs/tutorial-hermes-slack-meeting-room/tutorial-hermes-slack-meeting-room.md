# Hermes Slack Meeting Room Skill 설치와 사용법

이 튜토리얼은 `hermes-slack-meeting-room` skill을 설치하고, Hermes Agent에서 Slack 멀티프로필 회의실 설정 가이드로 사용하는 과정을 다룹니다.

## 1. 무엇을 설치하는가

`hermes-slack-meeting-room`은 Hermes skill입니다. 직접 Slack 앱을 대신 만들어 주는 플러그인이 아니라, 사용자가 꼭 Slack UI에서 해야 하는 작업은 체크리스트로 안내하고, Hermes 쪽 설정은 템플릿과 검증 명령으로 정리해 주는 설치 가이드형 skill입니다.

이 skill 자체가 회의실 런타임 기능을 제공하는 것이 아닙니다. 목적은 Hermes Agent와 사용자가 함께 Slack 앱, Hermes profile, channel prompt, `/meeting` 등록 규칙, persona matrix, TTS 정책, 회의 운영 ground rules를 단계적으로 만들도록 돕는 것입니다.

실제 회의 동작은 설정이 끝난 뒤의 Hermes profile, Slack gateway, 채널 프롬프트, slash command, 그리고 필요하면 설치되는 `hermes-meeting` moderator instruction이 담당합니다.

기본 목표는 기존 Hermes 기본 프로필 1개에 회의 참여 프로필 3개를 추가하고, 각 프로필의 이름 체계, 페르소나, 허용 채널, TTS provider와 voice를 문답으로 정하는 것입니다.

## 2. 설치 전 확인

먼저 Hermes가 정상 동작하는지 확인합니다.

```bash
hermes --version
hermes update --check
hermes config check
hermes profile list
hermes skills list
```

`hermes config check`가 실패하면 skill 설치보다 Hermes 기본 설정을 먼저 고칩니다.

## 3. 설치 방법

이 skill은 `assets/`, `references/`, `scripts/`를 함께 쓰는 multi-file skill입니다. raw `SKILL.md` URL로 설치하면 본문 하나만 설치되고 부속 파일이 빠지므로 사용하지 않습니다.

GitHub에 공개한 뒤에는 GitHub identifier 방식으로 설치합니다.

```bash
hermes skills install dandacompany/hermes-slack-meeting-room/skills/hermes-slack-meeting-room
```

같은 저장소에서 여러 skill을 배포할 계획이면 tap 방식이 좋습니다.

```bash
hermes skills tap add dandacompany/hermes-slack-meeting-room
hermes skills search "hermes slack meeting"
hermes skills install hermes-slack-meeting-room
```

개발 중인 로컬 복사본을 바로 설치할 때는 아래처럼 복사합니다.

```bash
mkdir -p ~/.hermes/skills/hermes-slack-meeting-room
cp -R skills/hermes-slack-meeting-room/* ~/.hermes/skills/hermes-slack-meeting-room/
hermes skills check
```

## 4. 설치 확인

설치 후 Hermes가 skill을 인식하는지 확인합니다.

```bash
hermes skills list
hermes skills check
```

패키지 자체도 한 번 검증합니다.

```bash
python3 ~/.hermes/skills/hermes-slack-meeting-room/scripts/validate_setup.py ~/.hermes/skills/hermes-slack-meeting-room
```

성공하면 다음과 비슷하게 나옵니다.

```text
Validation passed: /home/you/.hermes/skills/hermes-slack-meeting-room
```

## 5. 사용 시작

Hermes에게 이 skill을 사용해 Slack 회의실 설정을 진행해 달라고 요청합니다.

```bash
hermes -s hermes-slack-meeting-room
```

대화 안에서는 이렇게 요청합니다.

```text
hermes-slack-meeting-room skill을 사용해서 Slack 멀티프로필 회의실을 설정해줘.
기본 프로필 하나는 이미 있고, 회의 참여 프로필 3개를 추가하고 싶어.
```

Hermes는 바로 YAML 편집을 요구하지 않고 먼저 문답으로 profile matrix를 만듭니다.

## 6. 문답에서 정하는 것

스킬은 다음 정보를 하나씩 확인합니다.

| 항목 | 예시 |
| --- | --- |
| base moderator profile | manager |
| 추가 profile 1 | contents |
| 추가 profile 2 | critic |
| 추가 profile 3 | operator |
| Hermes profile id | contents |
| Slack app display name | Hermes Contents |
| persona display name | Contents |
| naming rule | Hermes 설정, Slack 앱, 회의 프롬프트에서 같은 이름을 알아볼 수 있게 맞춤 |
| persona name | 콘텐츠 전략가 |
| role/job | 유튜브 콘텐츠 기획자 |
| personality traits | 차분함, 구조화, 청중 감각 |
| values/priorities | 명확성, 실용성, 시청 지속률 |
| speaking style | 짧고 구체적인 한국어, 제목/훅 중심 |
| background/context | 교육 콘텐츠와 자동화 워크플로를 자주 다룸 |
| decision lens | 시청자가 바로 이해하고 실행할 수 있는가 |
| avoided behaviors | 근거 없는 낙관, 장황한 설명, 빠른 합의 |
| 허용 채널 | 테스트 회의 채널 1개부터 |
| TTS provider | Edge TTS, Hermes built-in provider, Typecast |
| voice mode | text-only, voice-summary, voice-full, hybrid |

기본 규칙은 `contents` profile이면 Slack 앱은 `Hermes Contents`, 회의 프롬프트의 persona name은 `Contents`처럼 맞추는 것입니다. 예외가 필요하면 문답에서 이유를 확인하고 명시적으로 기록합니다.

비즈니스 회의에서는 처음부터 빈칸으로 설계하지 않아도 됩니다. 스킬은 `assets/templates/business-persona-presets.yaml`의 built-in persona catalog를 보여주고, 회의 목적과 산출물에 맞춰 추천할 수 있습니다.

| 프리셋 | 적합한 회의 |
| --- | --- |
| Moderator | 진행, 턴 제어, 소크라테스식 설정 |
| Marketer | 포지셔닝, 캠페인, 퍼널, 고객 메시지 |
| Product | PRD, 로드맵, MVP, 우선순위 |
| Backend | API, 데이터베이스, 안정성, 보안성 있는 아키텍처 |
| Frontend | UI 구현, 상태, 접근성, 성능 |
| Designer | 브랜드, 시각 위계, 발표자료, 폴리시 |
| UX | 사용자 흐름, 온보딩, 마찰 지점, 사용성 |
| QA | 테스트 계획, 회귀, 재현 가능한 실패 케이스 |
| Researcher | 시장/사용자 리서치, 근거 품질, 가설 검증 |
| Data | KPI, 대시보드, 실험, 분석 주의점 |
| Planner | 사업계획, 제안서, 운영계획 |
| Consultant | 경영진용 프레이밍, 선택지, 트레이드오프 |
| Finance | 예산, ROI, 밸류에이션, 하방 리스크 |
| Sales | 피치, 반론 대응, 디스커버리, 계정 전략 |
| Success | 온보딩, 리텐션, 고객 건강도, 갱신 |
| Legal | 컴플라이언스, 개인정보, 계약, 주장 리스크 |
| Security | 위협 모델링, 권한, 시크릿, 공격 표면 |
| Ops | 프로세스, SOP, 소유권, 반복 운영 |
| People | 채용, 팀 건강, 피드백, 조직 커뮤니케이션 |
| Contents | 유튜브, 스크립트, 튜토리얼, 편집 전략 |

처음에는 `text-only` 또는 `voice-summary`가 안정적입니다. Typecast나 ElevenLabs 같은 유료/외부 provider는 텍스트 회의 흐름이 통과한 뒤 켭니다.

## 7. Slack에서 직접 해야 하는 일

Slack 앱 생성과 권한 부여는 skill이나 plugin이 대신 끝낼 수 없습니다. 스킬은 `references/slack-checklist.md`를 기준으로 사용자가 해야 할 작업을 안내합니다.

최소 확인 항목은 아래와 같습니다.

```text
Socket Mode: On
App Home Messages: On
Bot scopes: chat:write, commands, app_mentions:read, channels:history, channels:read, im:history, im:write
Events: app_mention, message.channels, message.im
Reinstall to Workspace: scope/event/command 변경 뒤 반드시 실행
Channel invite: 회의 채널에 모든 Hermes app 초대
```

`/meeting` slash command는 기본적으로 진행자 앱 하나에만 등록합니다. 여러 앱에 같은 command를 중복 등록하면 어떤 앱이 받는지 헷갈리고, workspace 설정에 따라 충돌처럼 보일 수 있습니다.

## 8. Hermes 설정 적용

문답이 끝나면 skill은 아래 템플릿을 사용해 설정 초안을 만듭니다.

```text
assets/templates/profile-config-snippets.yaml
assets/templates/channel-prompts.yaml
assets/templates/tts-options.yaml
assets/hermes-meeting/SKILL.md
```

적용 전에는 `<MEETING_CHANNEL_ID>`, `<@MODERATOR_USER_ID>`, `<ROLE_SPECIALIZATION>`, `<TYPECAST_VOICE_ID>` 같은 placeholder가 남아 있지 않은지 확인합니다.

프로필별 기본 검증은 아래처럼 합니다.

```bash
hermes config check
hermes --profile <profile-1> config check
hermes --profile <profile-2> config check
hermes --profile <profile-3> config check
```

검증이 통과한 뒤에 gateway를 재시작합니다.

## 9. 회의 운영 ground rules

`/meeting`은 단순히 여러 봇을 동시에 부르는 기능이 아니라, 진행자 프로필이 회의 상태와 발언권을 관리하는 workflow입니다. 세부 규칙은 설치된 skill의 `references/meeting-ground-rules.md`에 들어 있습니다.

핵심 규칙은 아래와 같습니다.

| 영역 | 규칙 |
| --- | --- |
| setup gate | 사용자가 회의 설정을 승인하기 전에는 참여자를 멘션하지 않음 |
| state block | routing, pause, resume, synthesis, decision마다 `[MEETING]` 상태 갱신 |
| 발언권 | 진행자만 발언권을 배정하고 participant는 직접 다른 앱을 멘션하지 않음 |
| sequential | 한 번에 한 명만 호출하고, 답변 후 `handoff`로 진행자에게 반환 |
| parallel | 여러 명을 한 번에 호출하되 서로 멘션하지 않고 `[PARALLEL-DONE]`으로 종료 |
| 사용자 개입 | pause, stop, revise, answer, comment, direct로 분류한 뒤 라우팅 재설계 |
| timeout/duplicate | 누락은 pending/missing으로 기록하고, 중복 답변은 첫 답변만 카운트 |
| anti-convergence | 중간과 최종 전 dissent/risk/verification checkpoint를 강제 |
| TTS | 메타데이터와 멘션은 읽지 않고 회의 본문만 음성화 |

운영 규칙을 직접 확인하려면 아래 파일을 엽니다.

```bash
sed -n '1,260p' ~/.hermes/skills/hermes-slack-meeting-room/references/meeting-ground-rules.md
```

## 10. 첫 Slack smoke test

처음에는 테스트 채널 하나에서 text-only로 확인합니다.

```text
/invite @Hermes@<MODERATOR_APP_NAME>
/invite @Hermes Contents
/invite @Hermes Critic
/invite @Hermes Operator
```

그 다음 `/meeting`을 실행합니다.

```text
/meeting 테스트 회의, 3턴, text-only
```

성공 기준은 여섯 가지입니다.

```text
1. 진행자가 먼저 회의 설정을 확인한다.
2. 사용자가 시작을 승인하기 전에는 참여자를 호출하지 않는다.
3. sequential 모드에서 한 번에 한 프로필만 발언한다.
4. participant는 발언 후@<MODERATOR_APP_NAME>에게 handoff한다.
5. 사용자가 중간에 개입하면 routing을 멈추고 상태를 갱신한다.
6. 중복/지연 답변이 와도 완료된 턴을 자동으로 다시 열지 않는다.
```

텍스트 흐름이 통과하면 voice-summary를 테스트합니다.

```text
/meeting 테스트 회의, 3턴, voice-summary
```

이때 TTS가 `[MEETING]`, `handoff:`, `round`, `next`, Slack mention 같은 메타정보를 읽으면 안 됩니다.

## 11. 자주 나는 오류

| 증상 | 먼저 볼 것 |
| --- | --- |
| Slackbot이 앱이 반응하지 않는다고 함 | gateway 상태, Socket Mode, app token, reinstall |
| `Unknown command /meeting` | `/meeting`이 진행자 app에 등록됐는지 확인 |
| DMs only라고 뜸 | profile config의 `slack.dm_only: false` |
| 봇이 채널 메시지를 못 봄 | 채널 초대, `message.channels`, `channels:history` |
| 모든 프로필이 동시에 답함 | free-response 채널 정책과 participant prompt |
| 중복/지연 답변으로 회의가 꼬임 | `meeting-ground-rules.md`의 timeout/duplicate handling |
| TTS가 메타정보를 읽음 | `voice-summary`와 TTS 필터 규칙 |

문제가 생기면 설치된 skill의 troubleshooting 문서를 먼저 엽니다.

```bash
sed -n '1,220p' ~/.hermes/skills/hermes-slack-meeting-room/references/troubleshooting.md
```

## 12. 다음 단계

첫 테스트가 통과하면 아래 순서로 확장합니다.

```text
1. 프로필 personality를 실제 회의 목적에 맞게 조정
2. 테스트 채널 외 허용 채널 추가
3. voice-summary에서 Typecast 또는 다른 provider로 교체
4. parallel 또는 mixed meeting mode 실험
5. 공개 GitHub repo로 배포하고 tap 설치 검증
```

안정화 전에는 Slack 채널 allowlist를 넓히지 않습니다. 멀티프로필 회의실은 한 채널에서 확실히 통과한 뒤 확장하는 방식이 가장 안전합니다.

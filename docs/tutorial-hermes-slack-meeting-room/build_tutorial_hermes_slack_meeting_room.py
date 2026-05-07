#!/usr/bin/env python3
from __future__ import annotations

import html
import pathlib
import re

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "tutorial-hermes-slack-meeting-room.html"

MASK_PATTERNS = [
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"), "xoxb-<SLACK_TOKEN>"),
    (re.compile(r"xapp-[A-Za-z0-9-]{20,}"), "xapp-<SLACK_APP_TOKEN>"),
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "sk-<API_KEY>"),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def mask(text: str) -> str:
    for pattern, repl in MASK_PATTERNS:
        text = pattern.sub(repl, text)
    return text


def code_block(label: str, text: str, lang: str = "") -> str:
    return f"""
    <div class="code-block">
      <div class="code-header">
        <span class="dots"><i></i><i></i><i></i></span>
        <span>{esc(label)}</span>
      </div>
      <pre><code class="language-{esc(lang)}">{esc(mask(text.strip()))}</code></pre>
    </div>
    """


def note_block(label: str, text: str) -> str:
    return f"""
    <aside class="note-block">
      <div class="block-label">{esc(label)}</div>
      <p>{text}</p>
    </aside>
    """


def design_block(label: str, goal: str, principles: list[str], components: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f"<li><span>{idx:02d}</span><p>{esc(item)}</p></li>"
        for idx, item in enumerate(principles, 1)
    )
    cards = "\n".join(
        f"<article><strong>{esc(name)}</strong><p>{esc(desc)}</p></article>"
        for name, desc in components
    )
    return f"""
    <section class="design-block">
      <div class="block-label">{esc(label)}</div>
      <p class="goal">{esc(goal)}</p>
      <ol class="principles">{items}</ol>
      <div class="component-grid">{cards}</div>
    </section>
    """


def table(rows: list[tuple[str, str]], headers: tuple[str, str] = ("항목", "내용")) -> str:
    body = "\n".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in rows)
    return f"""
    <table>
      <thead><tr><th>{esc(headers[0])}</th><th>{esc(headers[1])}</th></tr></thead>
      <tbody>{body}</tbody>
    </table>
    """


SECTIONS = [
    {
        "num": "01",
        "title": "무엇을 설치하는가",
        "lede": "이 skill은 Slack 앱을 대신 만드는 플러그인이나 회의실 런타임이 아니라, 사용자가 해야 할 Slack UI 작업과 Codex가 처리할 Hermes 설정 작업을 분리하는 setup guide입니다.",
        "blocks": [
            design_block(
                "01-1. 구조",
                "기본 프로필 하나에서 시작해 참여 프로필 3개를 추가할 수 있도록 설정, 컨벤션, 프롬프트, 검증 절차를 단계적으로 만든다.",
                [
                    "Slack 앱 생성과 권한 부여는 체크리스트로 안내한다.",
                    "Hermes 설정은 템플릿과 검증 명령으로 결정론적으로 처리한다.",
                    "회의 동작은 설정된 Hermes profile, Slack gateway, channel prompt, moderator instruction이 담당한다.",
                    "TTS는 text-only 통과 후 voice-summary부터 확장한다.",
                ],
                [
                    ("Setup Coach", "프로필/Slack 앱 이름 체계, persona card, voice를 문답으로 확정"),
                    ("Template Builder", "profile config, channel prompt, meeting skill 템플릿 적용"),
                    ("Validator", "placeholder, YAML, token pattern, Hermes config 상태 점검"),
                ],
            )
        ],
    },
    {
        "num": "02",
        "title": "설치 전 상태 확인",
        "lede": "Hermes 기본 설치가 흔들리면 Slack 회의실 설정도 같이 흔들립니다. skill 설치 전에 기본 상태부터 확인합니다.",
        "blocks": [
            code_block(
                "02-1. Hermes baseline check",
                """
hermes --version
hermes update --check
hermes config check
hermes profile list
hermes skills list
                """,
                "bash",
            ),
            note_block(
                "02-2. 판단 기준",
                "`hermes config check`가 실패하면 profile이나 Slack 설정을 시작하지 말고 Hermes 기본 설정을 먼저 고칩니다.",
            ),
        ],
    },
    {
        "num": "03",
        "title": "skill 설치",
        "lede": "이 패키지는 multi-file skill입니다. raw SKILL.md URL 설치는 부속 파일을 가져오지 못하므로 GitHub identifier 또는 tap 방식으로 설치합니다.",
        "blocks": [
            code_block(
                "03-1. GitHub identifier",
                "hermes skills install dandacompany/hermes-slack-meeting-room/skills/hermes-slack-meeting-room",
                "bash",
            ),
            code_block(
                "03-2. GitHub tap",
                """
hermes skills tap add dandacompany/hermes-slack-meeting-room
hermes skills search "hermes slack meeting"
hermes skills install hermes-slack-meeting-room
                """,
                "bash",
            ),
            code_block(
                "03-3. Local development",
                """
mkdir -p ~/.hermes/skills/hermes-slack-meeting-room
cp -R skills/hermes-slack-meeting-room/* ~/.hermes/skills/hermes-slack-meeting-room/
hermes skills check
                """,
                "bash",
            ),
        ],
    },
    {
        "num": "04",
        "title": "설치 확인",
        "lede": "Hermes가 skill을 읽는지 확인하고, 패키지 내부 파일과 템플릿이 빠지지 않았는지 검증합니다.",
        "blocks": [
            code_block(
                "04-1. Hermes skill check",
                """
hermes skills list
hermes skills check
                """,
                "bash",
            ),
            code_block(
                "04-2. Package validator",
                "python3 ~/.hermes/skills/hermes-slack-meeting-room/scripts/validate_setup.py ~/.hermes/skills/hermes-slack-meeting-room",
                "bash",
            ),
            code_block(
                "04-3. Expected output",
                "Validation passed: /home/you/.hermes/skills/hermes-slack-meeting-room",
                "text",
            ),
        ],
    },
    {
        "num": "05",
        "title": "사용 시작",
        "lede": "Hermes 대화에서 skill을 명시적으로 불러 setup workflow를 시작합니다. 이 단계에서는 YAML을 먼저 편집하지 않고 profile matrix를 만듭니다.",
        "blocks": [
            code_block("05-1. Start Hermes with the skill", "hermes -s hermes-slack-meeting-room", "bash"),
            code_block(
                "05-2. User prompt",
                """
hermes-slack-meeting-room skill을 사용해서 Slack 멀티프로필 회의실을 설정해줘.
기본 프로필 하나는 이미 있고, 회의 참여 프로필 3개를 추가하고 싶어.
                """,
                "text",
            ),
            table(
                [
                    ("Moderator", "기존 base profile 또는 진행자 profile"),
                    ("Participants", "기본 3개, profile id와 Slack 앱명을 일원화하고 persona는 사용자 문답으로 결정"),
                    ("Hermes profile id", "`contents`, `critic`, `operator`처럼 config에서 쓰는 짧은 id"),
                    ("Slack app display name", "`Hermes Contents`처럼 profile id를 바로 알아볼 수 있는 앱 이름"),
                    ("Persona display name", "`Contents`처럼 회의 프롬프트에서 부를 이름"),
                    ("Naming rule", "Hermes 설정, Slack 앱, 회의 프롬프트에서 같은 프로필임을 바로 알아볼 수 있게 맞춤"),
                    ("Persona card", "이름, 직업/역할, 성격, 가치관, 말투, 배경, 판단 기준, 피해야 할 방식"),
                    ("TTS", "Edge TTS 기본, Hermes built-in provider, Typecast, ElevenLabs 후보 선택 가능"),
                    ("Channel policy", "처음에는 테스트 채널 1개만 허용"),
                ],
                ("결정 항목", "권장 시작점"),
            ),
            note_block(
                "05-3. Business persona catalog",
                "`assets/templates/business-persona-presets.yaml`에는 비즈니스 회의용 built-in persona가 들어 있습니다. 사용자는 목록에서 고르거나, 회의 목적과 산출물을 말해 추천을 받을 수 있습니다.",
            ),
            table(
                [
                    ("Moderator", "진행, 턴 제어, 소크라테스식 설정"),
                    ("Marketer", "포지셔닝, 캠페인, 퍼널, 고객 메시지"),
                    ("Product", "PRD, 로드맵, MVP, 우선순위"),
                    ("Backend", "API, 데이터베이스, 안정성, 보안성 있는 아키텍처"),
                    ("Frontend", "UI 구현, 상태, 접근성, 성능"),
                    ("Designer", "브랜드, 시각 위계, 발표자료, 폴리시"),
                    ("UX", "사용자 흐름, 온보딩, 마찰 지점, 사용성"),
                    ("QA", "테스트 계획, 회귀, 재현 가능한 실패 케이스"),
                    ("Researcher", "시장/사용자 리서치, 근거 품질, 가설 검증"),
                    ("Data", "KPI, 대시보드, 실험, 분석 주의점"),
                    ("Planner", "사업계획, 제안서, 운영계획"),
                    ("Consultant", "경영진용 프레이밍, 선택지, 트레이드오프"),
                    ("Finance", "예산, ROI, 밸류에이션, 하방 리스크"),
                    ("Sales", "피치, 반론 대응, 디스커버리, 계정 전략"),
                    ("Success", "온보딩, 리텐션, 고객 건강도, 갱신"),
                    ("Legal", "컴플라이언스, 개인정보, 계약, 주장 리스크"),
                    ("Security", "위협 모델링, 권한, 시크릿, 공격 표면"),
                    ("Ops", "프로세스, SOP, 소유권, 반복 운영"),
                    ("People", "채용, 팀 건강, 피드백, 조직 커뮤니케이션"),
                    ("Contents", "유튜브, 스크립트, 튜토리얼, 편집 전략"),
                ],
                ("프리셋", "적합한 회의"),
            ),
        ],
    },
    {
        "num": "06",
        "title": "Slack에서 해야 할 일",
        "lede": "Slack 앱 생성, scope, Socket Mode, reinstall, 채널 초대는 plugin으로 대신 끝낼 수 없습니다. skill은 이 부분을 체크리스트로 안내합니다.",
        "blocks": [
            code_block(
                "06-1. Minimum Slack setup",
                """
Socket Mode: On
App Home Messages: On
Bot scopes: chat:write, commands, app_mentions:read, channels:history, channels:read, im:history, im:write
Events: app_mention, message.channels, message.im
Reinstall to Workspace: scope/event/command 변경 뒤 반드시 실행
Channel invite: 회의 채널에 모든 Hermes app 초대
                """,
                "text",
            ),
            note_block(
                "06-2. /meeting command",
                "`/meeting`은 진행자 앱 하나에만 등록합니다. 여러 앱에 같은 slash command를 등록하면 어느 앱이 받는지 불명확해집니다.",
            ),
            code_block(
                "06-3. Secret input",
                """
touch <PROFILE_ENV_FILE>
chmod 600 <PROFILE_ENV_FILE>
"${VISUAL:-${EDITOR:-nano}}" <PROFILE_ENV_FILE>

# 필요한 값만 파일에 저장합니다.
TYPECAST_API_KEY=<TYPECAST_API_KEY>
ELEVENLABS_API_KEY=<ELEVENLABS_API_KEY>
                """,
                "bash",
            ),
            code_block(
                "06-4. Secret check",
                """
grep -E '^(TYPECAST_API_KEY|ELEVENLABS_API_KEY|SLACK_BOT_TOKEN|SLACK_APP_TOKEN)=' <PROFILE_ENV_FILE> \\
  | sed 's/=.*/=<set>/'
                """,
                "bash",
            ),
        ],
    },
    {
        "num": "07",
        "title": "Hermes 설정 적용",
        "lede": "문답이 끝나면 skill은 bundled template을 사용해 profile config, channel prompt, meeting skill 설치 계획을 만듭니다.",
        "blocks": [
            code_block(
                "07-1. Bundled templates",
                """
assets/templates/profile-config-snippets.yaml
assets/templates/channel-prompts.yaml
assets/templates/tts-options.yaml
assets/hermes-meeting/SKILL.md
                """,
                "text",
            ),
            code_block(
                "07-2. Profile checks",
                """
hermes config check
hermes --profile <profile-1> config check
hermes --profile <profile-2> config check
hermes --profile <profile-3> config check
                """,
                "bash",
            ),
            note_block(
                "07-3. Placeholder rule",
                "`<MEETING_CHANNEL_ID>`, `<@MODERATOR_USER_ID>`, `<ROLE_SPECIALIZATION>`, `<TYPECAST_VOICE_ID>`, `<ELEVENLABS_VOICE_ID>` 같은 placeholder가 남아 있으면 gateway를 재시작하지 않습니다.",
            ),
        ],
    },
    {
        "num": "08",
        "title": "회의 운영 ground rules",
        "lede": "`/meeting`은 여러 봇을 동시에 부르는 기능이 아니라, 진행자 프로필이 상태와 발언권을 관리하는 workflow입니다.",
        "blocks": [
            table(
                [
                    ("setup gate", "사용자가 회의 설정을 승인하기 전에는 참여자를 멘션하지 않음"),
                    ("state block", "routing, pause, resume, synthesis, decision마다 [MEETING] 상태 갱신"),
                    ("발언권", "진행자만 발언권을 배정하고 participant는 직접 다른 앱을 멘션하지 않음"),
                    ("sequential", "한 번에 한 명만 호출하고, 답변 후 handoff로 진행자에게 반환"),
                    ("parallel", "여러 명을 한 번에 호출하되 서로 멘션하지 않고 [PARALLEL-DONE]으로 종료"),
                    ("사용자 개입", "pause, stop, revise, answer, comment, direct로 분류한 뒤 라우팅 재설계"),
                    ("timeout/duplicate", "누락은 pending/missing으로 기록하고, 중복 답변은 첫 답변만 카운트"),
                    ("anti-convergence", "중간과 최종 전 dissent/risk/verification checkpoint를 강제"),
                    ("TTS", "메타데이터와 멘션은 읽지 않고 회의 본문만 음성화"),
                ],
                ("영역", "규칙"),
            ),
            code_block(
                "08-1. Ground rules reference",
                "sed -n '1,260p' ~/.hermes/skills/hermes-slack-meeting-room/references/meeting-ground-rules.md",
                "bash",
            ),
        ],
    },
    {
        "num": "09",
        "title": "첫 Slack smoke test",
        "lede": "처음에는 text-only로 meeting flow만 확인합니다. TTS는 routing이 안정화된 뒤 켭니다.",
        "blocks": [
            code_block(
                "09-1. Invite apps",
                """
/invite @<MODERATOR_APP_NAME>
/invite @Hermes Contents
/invite @Hermes Critic
/invite @Hermes Operator
                """,
                "text",
            ),
            code_block("09-2. Text meeting", "/meeting 테스트 회의, 3턴, text-only", "text"),
            code_block("09-3. Voice summary meeting", "/meeting 테스트 회의, 3턴, voice-summary", "text"),
            table(
                [
                    ("설정 확인", "진행자가 먼저 회의 설정을 묻는다"),
                    ("승인 전 대기", "사용자가 시작하기 전에는 참여자를 호출하지 않는다"),
                    ("순차 발언", "한 번에 한 프로필만 발언한다"),
                    ("사용자 개입", "중간 개입 시 routing을 멈추고 상태를 갱신한다"),
                    ("중복/지연 답변", "완료된 턴을 자동으로 다시 열지 않는다"),
                    ("TTS 필터", "[MEETING], handoff, mention을 읽지 않는다"),
                ],
                ("성공 기준", "확인 내용"),
            ),
        ],
    },
    {
        "num": "10",
        "title": "오류가 날 때",
        "lede": "대부분의 실패는 Slack app 설정, gateway 상태, command 등록 위치, TTS metadata 분리 중 하나에서 생깁니다.",
        "blocks": [
            table(
                [
                    ("앱이 반응하지 않음", "gateway 상태, Socket Mode, app token, reinstall"),
                    ("Unknown command", "`/meeting`이 진행자 app에 등록됐는지 확인"),
                    ("DMs only", "`slack.dm_only: false` 확인"),
                    ("채널 메시지를 못 봄", "채널 초대, events, history scopes 확인"),
                    ("모든 프로필 동시 응답", "free-response channel과 participant prompt 확인"),
                    ("중복/지연 답변으로 회의가 꼬임", "`meeting-ground-rules.md`의 timeout/duplicate handling 확인"),
                    ("TTS가 metadata를 읽음", "`voice-summary`와 TTS 필터 규칙 확인"),
                ],
                ("증상", "먼저 볼 곳"),
            ),
            code_block(
                "10-1. Troubleshooting reference",
                "sed -n '1,220p' ~/.hermes/skills/hermes-slack-meeting-room/references/troubleshooting.md",
                "bash",
            ),
        ],
    },
]


HEAD = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hermes Slack Meeting Room Skill 설치와 사용법</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --stone-900:#111111; --stone-700:#2a2a2a; --stone-500:#555555;
      --stone-400:#777777; --stone-200:#c8c4bc;
      --sand-50:#f5f2ec; --sand-100:#ebe5d8; --sand-200:#e0d8c8;
      --moss:#1e3f3f; --moss-light:#2d5555; --cream:#faf7f0;
      --red-soft:#b84a2c; --green-soft:#3a6c49; --terra:#7a5a10;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--sand-50);
      color: var(--stone-700);
      font-family: 'Noto Sans KR', system-ui, sans-serif;
      line-height: 1.75;
    }
    .hero {
      padding: 88px 32px 72px;
      background: linear-gradient(135deg, var(--sand-100), var(--sand-200));
      border-bottom: 1px solid var(--stone-200);
    }
    .hero-inner, .container { max-width: 820px; margin: 0 auto; }
    .eyebrow, .section-num, .block-label, .code-header, th {
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: .04em;
      text-transform: uppercase;
    }
    .eyebrow {
      display: inline-block;
      margin-bottom: 18px;
      color: var(--moss);
      font-size: 12px;
      font-weight: 500;
    }
    h1, h2 {
      font-family: 'Noto Serif KR', serif;
      color: var(--stone-900);
      line-height: 1.2;
      letter-spacing: 0;
    }
    h1 {
      max-width: 780px;
      margin: 0;
      font-size: clamp(34px, 5vw, 52px);
      font-weight: 900;
    }
    .hero p {
      max-width: 720px;
      margin: 24px 0 0;
      color: var(--stone-500);
      font-size: 17px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 34px;
    }
    .meta-grid div {
      background: rgba(250, 247, 240, .62);
      border: 1px solid rgba(200, 196, 188, .85);
      border-radius: 16px;
      padding: 16px;
    }
    .meta-grid dt {
      margin: 0 0 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--stone-400);
    }
    .meta-grid dd { margin: 0; color: var(--stone-700); font-weight: 600; }
    section.step {
      padding: 68px 0;
      border-top: 1px solid var(--stone-200);
    }
    .section-num {
      color: var(--stone-400);
      font-size: 11px;
      letter-spacing: .35em;
    }
    h2 {
      margin: 10px 0 14px;
      font-size: clamp(24px, 3vw, 32px);
      font-weight: 700;
    }
    .lede { margin: 0 0 28px; color: var(--stone-500); font-size: 16px; }
    .code-block, .note-block, .design-block {
      margin: 22px 0;
      border: 1px solid var(--stone-200);
      border-radius: 18px;
      overflow: hidden;
      background: var(--cream);
      box-shadow: 0 18px 50px rgba(17, 17, 17, .05);
    }
    .code-block { background: #111111; border-color: #272727; }
    .code-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 13px 16px;
      border-bottom: 1px solid #272727;
      color: #c8c4bc;
      font-size: 12px;
    }
    .dots { display: flex; gap: 7px; }
    .dots i { width: 11px; height: 11px; border-radius: 999px; display: block; }
    .dots i:nth-child(1) { background: #ff5f57; }
    .dots i:nth-child(2) { background: #ffbd2e; }
    .dots i:nth-child(3) { background: #28c840; }
    pre {
      margin: 0;
      padding: 18px 20px;
      overflow-x: auto;
      white-space: pre;
    }
    code {
      color: #f5f2ec;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      line-height: 1.85;
    }
    .note-block {
      padding: 20px 22px;
      border-left: 5px solid var(--moss);
    }
    .block-label {
      margin-bottom: 10px;
      color: var(--terra);
      font-size: 12px;
      font-weight: 500;
    }
    .note-block p, .design-block p { margin: 0; }
    .design-block { padding: 24px; }
    .goal {
      color: var(--stone-900);
      font-family: 'Noto Serif KR', serif;
      font-size: 20px;
      font-weight: 700;
    }
    .principles {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 22px 0;
      padding: 0;
      list-style: none;
    }
    .principles li {
      padding: 16px;
      border: 1px solid var(--stone-200);
      border-radius: 14px;
      background: rgba(245, 242, 236, .65);
    }
    .principles span {
      display: block;
      margin-bottom: 8px;
      color: var(--moss);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
    }
    .principles p { color: var(--stone-700); font-size: 14px; }
    .component-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }
    .component-grid article {
      padding: 16px;
      border-radius: 14px;
      background: var(--sand-50);
      border: 1px solid var(--stone-200);
    }
    .component-grid strong { color: var(--stone-900); }
    .component-grid p { margin-top: 8px; color: var(--stone-500); font-size: 14px; }
    table {
      width: 100%;
      margin: 22px 0;
      border-collapse: collapse;
      overflow: hidden;
      border: 1px solid var(--stone-200);
      border-radius: 16px;
      background: var(--cream);
      display: table;
    }
    th, td { padding: 14px 16px; border-bottom: 1px solid var(--stone-200); vertical-align: top; }
    th { color: var(--moss); font-size: 12px; text-align: left; background: var(--sand-100); }
    td { font-size: 14px; color: var(--stone-700); }
    tr:last-child td { border-bottom: 0; }
    footer {
      padding: 50px 32px 70px;
      border-top: 1px solid var(--stone-200);
      color: var(--stone-500);
      text-align: center;
    }
    @media (max-width: 720px) {
      .hero { padding: 58px 22px 48px; }
      .container { padding: 0 22px; }
      .meta-grid, .principles, .component-grid { grid-template-columns: 1fr; }
      section.step { padding: 50px 0; }
      pre { padding: 16px; }
    }
  </style>
</head>
"""


def render_step(section: dict) -> str:
    blocks = "\n".join(section["blocks"])
    return f"""
    <section class="step" id="step-{esc(section['num'])}">
      <div class="section-num">STEP {esc(section['num'])}</div>
      <h2>{esc(section['title'])}</h2>
      <p class="lede">{esc(section['lede'])}</p>
      {blocks}
    </section>
    """


def body() -> str:
    rendered = "\n".join(render_step(section) for section in SECTIONS)
    return f"""
<body>
  <header class="hero">
    <div class="hero-inner">
      <span class="eyebrow">Hermes Skill Tutorial</span>
      <h1>Hermes Slack Meeting Room Skill 설치와 사용법</h1>
      <p>Slack 앱 설정과 Hermes 프로필 설정이 뒤섞이지 않도록, skill 설치부터 첫 `/meeting` smoke test까지 한 번에 따라가는 운영 가이드입니다.</p>
      <dl class="meta-grid">
        <div><dt>대상</dt><dd>Hermes 운영자</dd></div>
        <div><dt>기준</dt><dd>기본 프로필 설치 직후</dd></div>
        <div><dt>기본 TTS</dt><dd>Edge TTS</dd></div>
      </dl>
    </div>
  </header>
  <main class="container">
    {rendered}
  </main>
  <footer>
    <p>Raw SKILL.md URL은 단일 파일 설치용입니다. 이 패키지는 GitHub identifier 또는 tap 방식으로 설치합니다.</p>
  </footer>
</body>
</html>
"""


def main() -> None:
    html_text = HEAD + body()
    html_text = "\n".join(line.rstrip() for line in html_text.splitlines()) + "\n"
    OUT.write_text(html_text, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

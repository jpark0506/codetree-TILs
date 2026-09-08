#!/usr/bin/env python3
"""`.review/today.json` 을 읽어 Discord 웹훅으로 복습 카드를 보낸다.

hyper-whale-tracker 의 internal/notify/discord.go 를 파이썬으로 옮긴 것이다.
같은 규약을 따른다: username 배지, 임베드 timestamp, 링크 버튼,
429 는 본문의 retry_after 를 헤더보다 우선해 3회까지 재시도, 5xx 는 1초 뒤 한 번 더,
그 밖의 4xx 는 재시도해도 나아지지 않으므로 즉시 실패.

웹훅 URL 은 절대 커밋하지 않는다. 환경변수 DISCORD_TIL_WEBHOOK 로만 받는다.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY_PATH = os.path.join(REPO, ".review", "today.json")
ENV_PATH = os.path.join(REPO, ".env")

# Discord 제한
DESC_LIMIT = 4096
TITLE_LIMIT = 256
FIELD_NAME_LIMIT = 256
FIELD_VALUE_LIMIT = 1024

# 색은 hyper-whale-tracker notify/format.go 팔레트를 따른다.
COLOR_NOTE = 0x3498DB  # 파랑: 분석/설명
COLOR_ALGO = 0x2ECC71  # 초록: 풀이
COLOR_OPT = 0xE67E22  # 주황: 개선 제안

# 링크 버튼 컴포넌트 상수 (웹훅은 link 스타일 버튼만 실을 수 있다)
COMPONENT_ACTION_ROW = 1
COMPONENT_BUTTON = 2
BUTTON_STYLE_LINK = 5

MAX_ATTEMPTS = 3

# 개선 판정별 제목 이모지
VERDICT_EMOJI = {
    "개선 여지 있음": "⚡",
    "상수만 개선": "🔧",
    "이미 최적": "✅",
}


def load_dotenv(path=ENV_PATH):
    """.env 를 읽어 아직 없는 키만 환경변수에 채운다. 이미 있는 값이 우선."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def username():
    """운영 환경이 아니면 배지를 붙인다. WHALE [DEV] 와 같은 규약."""
    env = os.environ.get("APP_ENVIRONMENT", "").strip().lower()
    if env in ("", "production", "prod"):
        return "복습"
    return f"복습 [{env.upper()}]"


def clip(text, limit):
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def spoiler(text):
    """Discord 스포일러. 전체를 한 덩어리로 감싼다.

    줄 단위로 감싸면 스포일러 블록이 여러 개가 되어 정답을 보려고 여러 번 눌러야 한다.
    Discord 는 여러 줄 스포일러를 지원하므로 한 번에 열리게 통째로 감싼다.
    본문에 `||` 가 섞여 있으면 조기 종료되므로 먼저 없앤다.
    """
    text = (text or "").strip().replace("||", "")
    if not text:
        return ""
    return f"||{text}||"


def join(*parts):
    return "\n\n".join(p for p in (p.strip() if p else "" for p in parts) if p)


def field(name, value, inline=False):
    """값이 있을 때만 필드를 만든다. 없으면 None 을 돌려 걸러지게 한다."""
    value = (value or "").strip()
    if not value:
        return None
    return {
        "name": clip(name, FIELD_NAME_LIMIT),
        "value": clip(value, FIELD_VALUE_LIMIT),
        "inline": inline,
    }


def fields(*items):
    return [f for f in items if f]


def build_messages(data):
    """카드를 메시지 단위로 나눈다.

    임베드 하나에 총 6000자 제한이 있어 카드마다 따로 보낸다.
    본문을 description 에 몰지 않고 필드로 쪼갠다. 필드는 값이 1024자에서 잘리고
    제목이 따로 굵게 렌더링되므로, 휴대폰에서 훑어 읽기가 훨씬 낫다.
    """
    syntax = data.get("syntax", {})
    algo = data.get("algo", {})
    opt = data.get("optimized") or {}
    day = data.get("date", "")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    messages = []

    # ── 1. C++ 문법 ──────────────────────────────────────────────
    messages.append(
        {
            "username": username(),
            "embeds": [
                {
                    "title": clip(f"📘 {syntax.get('topic', '오늘의 문법')}", TITLE_LIMIT),
                    "description": clip(syntax.get("headline", ""), DESC_LIMIT),
                    "color": COLOR_NOTE,
                    "timestamp": stamp,
                    "fields": fields(
                        field("💡 왜 그런가", syntax.get("body")),
                        field("💻 코드", syntax.get("code")),
                        field("🧩 확인 퀴즈", syntax.get("quiz")),
                        field("🔑 정답", spoiler(syntax.get("answer"))),
                    ),
                    "footer": {"text": f"아침 복습 · {day}"},
                }
            ],
        }
    )

    # ── 2. 알고리즘 ──────────────────────────────────────────────
    link = (algo.get("link") or "").strip()
    algo_embed = {
        "title": clip(f"🧠 {algo.get('title', '알고리즘 복습')}", TITLE_LIMIT),
        "description": clip(algo.get("summary", ""), DESC_LIMIT),
        "color": COLOR_ALGO,
        "timestamp": stamp,
        "fields": fields(
            field("📂 분류", algo.get("tag"), inline=True),
            field("📄 내 풀이", f"`{algo.get('path', '')}`", inline=True),
            field("🤔 생각해보기", algo.get("question")),
            field("🔑 핵심 아이디어", spoiler(algo.get("answer"))),
            field("🔍 내 코드", algo.get("code_review")),
        ),
        "footer": {"text": "정답은 가려져 있다. 먼저 생각해보고 눌러볼 것."},
    }
    if link.startswith("http"):
        algo_embed["url"] = link

    algo_msg = {"username": username(), "embeds": [algo_embed]}
    if link.startswith("http"):
        algo_msg["components"] = [
            {
                "type": COMPONENT_ACTION_ROW,
                "components": [
                    {
                        "type": COMPONENT_BUTTON,
                        "style": BUTTON_STYLE_LINK,
                        "label": "문제 보러 가기",
                        "url": link,
                        "emoji": {"name": "🌳"},
                    }
                ],
            }
        ]
    messages.append(algo_msg)

    # ── 3. 더 나은 풀이 (있을 때만) ───────────────────────────────
    if opt.get("idea") or opt.get("code"):
        verdict = (opt.get("verdict") or "").strip()
        emoji = VERDICT_EMOJI.get(verdict, "⚡")
        messages.append(
            {
                "username": username(),
                "embeds": [
                    {
                        "title": clip(f"{emoji} 더 나은 풀이 — {verdict or '검토'}", TITLE_LIMIT),
                        "description": clip(opt.get("gain", ""), DESC_LIMIT),
                        "color": COLOR_OPT,
                        "timestamp": stamp,
                        "fields": fields(
                            field("💡 아이디어", opt.get("idea")),
                            field("💻 코드", opt.get("code")),
                        ),
                        "footer": {"text": f"{algo.get('title', '')} 개선안"},
                    }
                ],
            }
        )

    return messages


def retry_after(headers, body):
    """429 대기 시간. 본문의 retry_after 가 소수점까지 있어 헤더보다 정확하다."""
    try:
        value = float(json.loads(body).get("retry_after", 0))
        if value > 0:
            return value
    except (ValueError, TypeError, AttributeError):
        pass
    header = headers.get("Retry-After", "") if headers else ""
    try:
        value = float(header)
        if value > 0:
            return value
    except ValueError:
        pass
    return 2.0


def post(url, payload):
    """웹훅 전송. 성공하면 조용히 돌아오고, 실패하면 SystemExit 를 던진다."""
    body = json.dumps(payload).encode("utf-8")
    last_err = "원인 미상"

    for attempt in range(MAX_ATTEMPTS):
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "codetree-daily-review/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                if res.status < 300:
                    return
                last_err = f"예상 밖 상태 코드 {res.status}"
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            if e.code == 429:
                wait = min(retry_after(e.headers, detail), 30.0)
                last_err = f"레이트리밋(429), {wait:.1f}초 대기"
                time.sleep(wait)
                continue
            if e.code >= 500:
                last_err = f"Discord 서버 오류 {e.code}: {detail}"
                time.sleep(1)
                continue
            # 429 가 아닌 4xx 는 재시도해도 나아지지 않는다.
            raise SystemExit(f"Discord 전송 실패 (HTTP {e.code}): {detail}")
        except urllib.error.URLError as e:
            last_err = f"연결 실패: {e.reason}"
            time.sleep(1)

    raise SystemExit(f"Discord 전송 실패 ({MAX_ATTEMPTS}회 시도): {last_err}")


def main():
    load_dotenv()
    dry_run = bool(os.environ.get("DRY_RUN"))
    url = os.environ.get("DISCORD_TIL_WEBHOOK", "").strip()
    if not url and not dry_run:
        raise SystemExit("DISCORD_TIL_WEBHOOK 이 비어 있다. GitHub Secrets 또는 .env 를 확인할 것.")

    if not os.path.exists(TODAY_PATH):
        raise SystemExit(f"{TODAY_PATH} 가 없다. 카드 생성 단계가 실패했을 가능성이 높다.")

    with open(TODAY_PATH, encoding="utf-8") as f:
        data = json.load(f)

    messages = build_messages(data)

    if dry_run:
        for msg in messages:
            embed = msg["embeds"][0]
            print(f"╔══ {embed['title']}")
            if embed.get("description"):
                print(f"║  {embed['description']}")
            for f in embed.get("fields", []):
                mark = "▸" if f["inline"] else "▪"
                print(f"╟─ {mark} {f['name']}  ({len(f['value'])}자)")
                for line in f["value"].split("\n"):
                    print(f"║  {line}")
            if msg.get("components"):
                print(f"╟─ [버튼] {msg['components'][0]['components'][0]['url']}")
            print("╚" + "═" * 60)
            print()
        return 0

    for i, msg in enumerate(messages):
        post(url, msg)
        if i < len(messages) - 1:
            time.sleep(1)  # 웹훅 레이트리밋 여유
    print(f"Discord 전송 완료 ({len(messages)}건)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

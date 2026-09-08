#!/usr/bin/env python3
"""생성된 `.review/today.json` 을 정리하고 검증한다.

hyper-whale-tracker 의 interpret.parseCLIOutput 과 같은 복구 전략을 쓴다.
모델이 지시를 어기고 코드펜스를 두르거나 앞뒤에 산문을 붙이는 경우가 있어,
펜스를 벗기고 첫 '{' 부터 마지막 '}' 까지를 잘라내 파싱을 시도한다.
복구에 성공하면 정리된 JSON 으로 파일을 덮어써 다음 단계가 깨끗한 입력을 받게 한다.

`claude -p --output-format json` 의 봉투를 --envelope 로 함께 넘기면
is_error 여부도 확인한다.
"""

import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY_PATH = os.path.join(REPO, ".review", "today.json")

REQUIRED = {
    "syntax": ("topic", "headline", "body", "code", "quiz", "answer"),
    "algo": ("title", "tag", "summary", "question", "answer", "code_review"),
    "optimized": ("verdict", "idea", "code", "gain"),
}

# Discord 임베드 필드 값은 1024자에서 잘린다. 넘으면 경고만 하고 진행한다
# (post_discord.py 가 말줄임표로 자른다).
FIELD_LIMIT = 1024


def recover(raw):
    """코드펜스와 앞뒤 산문을 걷어내고 JSON 객체만 남긴다."""
    text = raw.strip()
    for fence in ("```json", "```"):
        if text.startswith(fence):
            text = text[len(fence) :]
            break
    text = text.removesuffix("```").strip()

    start = text.find("{")
    end = text.rfind("}")
    if start > 0 and end > start:
        text = text[start : end + 1]
    return text


def check_envelope(path):
    """claude -p --output-format json 봉투에서 실패를 잡아낸다."""
    with open(path, encoding="utf-8") as f:
        raw = f.read().strip()
    if not raw:
        raise SystemExit("claude 가 아무것도 출력하지 않았다.")
    try:
        env = json.loads(raw)
    except json.JSONDecodeError:
        # 봉투가 깨졌어도 today.json 만 멀쩡하면 진행할 수 있다.
        print("경고: claude 출력 봉투를 파싱하지 못했다. today.json 으로 판단한다.", file=sys.stderr)
        return
    if env.get("is_error"):
        raise SystemExit(f"claude 실행 실패: {str(env.get('result', ''))[:300]}")
    if env.get("subtype") and env["subtype"] != "success":
        print(f"경고: claude subtype={env['subtype']}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--envelope", help="claude -p --output-format json 출력 파일")
    args = parser.parse_args()

    if args.envelope and os.path.exists(args.envelope):
        check_envelope(args.envelope)

    if not os.path.exists(TODAY_PATH):
        raise SystemExit(f"{TODAY_PATH} 가 없다. 카드 생성이 실패했다.")

    with open(TODAY_PATH, encoding="utf-8") as f:
        raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as first:
        try:
            data = json.loads(recover(raw))
        except json.JSONDecodeError:
            raise SystemExit(f"today.json 을 파싱할 수 없다: {first}") from first
        with open(TODAY_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("today.json 을 복구했다 (코드펜스/산문 제거).")

    missing = [
        f"{section}.{key}"
        for section, keys in REQUIRED.items()
        for key in keys
        if not str(data.get(section, {}).get(key, "")).strip()
    ]
    if missing:
        raise SystemExit("필수 항목이 비어 있다: " + ", ".join(missing))

    overflow = [
        f"{section}.{key} {len(str(data[section][key]))}자"
        for section, keys in REQUIRED.items()
        for key in keys
        if len(str(data.get(section, {}).get(key, ""))) > FIELD_LIMIT
    ]
    if overflow:
        print("경고: 필드가 1024자를 넘어 잘린다 — " + ", ".join(overflow), file=sys.stderr)

    print(f"today.json 검증 통과 (문법: {data['syntax']['topic'][:40]} / 문제: {data['algo']['title']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

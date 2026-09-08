#!/usr/bin/env python3
"""오늘의 복습 소재를 고르고 Claude Code 에 넘길 프롬프트를 만든다.

- C++ 문법 주제: syntax_topics.TOPICS 를 커서로 순환 (매일 다른 주제 보장)
- 알고리즘 소재: 레포의 풀이 파일 중 가장 오래 안 나온 것 (간격 반복)

상태는 .review/state.json 에 남기고 워크플로가 커밋한다.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from syntax_topics import TOPICS

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(REPO, ".review", "state.json")
PROMPT_PATH = os.path.join(REPO, ".review", "prompt.md")
OUT_PATH = os.path.join(REPO, ".review", "today.json")

KST = timezone(timedelta(hours=9))
SOLUTION_EXTS = (".cpp", ".py", ".c", ".cc", ".java", ".js")
SKIP_DIRS = {".git", ".github", ".review", "scripts"}

# 방금 푼 문제를 몇 시간 동안 출제 대상에서 뺄지. 0 이면 전부 포함한다.
# 워크플로는 실행 시점에 체크아웃하므로, 새벽에 풀어 push 한 문제도 그날 아침 후보가 된다.
# 그런 문제는 "미출제" 라서 1순위로 뽑히는데, 푼 지 몇 시간 만에 복습하는 건
# 간격 반복의 취지와 어긋난다. 하루쯤 묵히고 싶으면 24 정도를 넣는다.
MIN_AGE_HOURS = int(os.environ.get("REVIEW_MIN_AGE_HOURS", "0"))


def find_solutions():
    """레포를 훑어 풀이 파일 목록을 만든다.

    각 항목은 (풀이경로, README경로|None, PROBLEM경로|None).
    CodeTree 플러그인이 만드는 README 에는 제목·링크·난이도만 있고 문제 본문이 없다.
    같은 폴더에 PROBLEM.md 를 직접 넣어두면 그걸 문제 본문으로 쓴다.
    """
    found = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel_root = os.path.relpath(root, REPO)
        for name in sorted(files):
            if not name.endswith(SOLUTION_EXTS):
                continue

            def sibling(filename):
                rel = os.path.normpath(os.path.join(rel_root, filename))
                return rel if os.path.exists(os.path.join(REPO, rel)) else None

            found.append(
                (
                    os.path.normpath(os.path.join(rel_root, name)),
                    sibling("README.md"),
                    sibling("PROBLEM.md"),
                )
            )
    return found


def added_at(path):
    """git 이력에서 파일이 처음 추가된 시각을 읽는다. 알 수 없으면 None."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%at", "-1", "--", path],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    stamp = out.stdout.strip()
    if not stamp.isdigit():
        return None
    return datetime.fromtimestamp(int(stamp), tz=timezone.utc)


def drop_too_fresh(solutions, now):
    """푼 지 얼마 안 된 풀이를 후보에서 뺀다. 전부 빠지면 원본을 그대로 쓴다."""
    if MIN_AGE_HOURS <= 0:
        return solutions
    cutoff = now - timedelta(hours=MIN_AGE_HOURS)
    kept = [s for s in solutions if (added_at(s[0]) or datetime.min.replace(tzinfo=timezone.utc)) < cutoff]
    if not kept:
        print(f"경고: {MIN_AGE_HOURS}시간 기준으로 남는 후보가 없어 전체를 대상으로 한다.", file=sys.stderr)
        return solutions
    if len(kept) < len(solutions):
        print(f"최근 {MIN_AGE_HOURS}시간 내 추가된 풀이 {len(solutions) - len(kept)}개는 다음 기회로 미룬다.")
    return kept


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"syntax_cursor": 0, "items": {}}


def pick_algo(solutions, state):
    """한 번도 안 나온 것 우선, 그다음 마지막 출제일이 가장 오래된 것."""
    items = state.setdefault("items", {})

    def sort_key(entry):
        rec = items.get(entry[0])
        if rec is None:
            return (0, "", entry[0])
        return (1, rec.get("last_shown", ""), entry[0])

    return sorted(solutions, key=sort_key)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--provider",
        default=os.environ.get("REVIEW_PROVIDER", "codex"),
        choices=("codex", "claude"),
        help="카드를 만들 CLI. 출력 방식이 달라 프롬프트 끝부분이 바뀐다.",
    )
    args = parser.parse_args()

    today = datetime.now(KST).date()
    solutions = find_solutions()
    if not solutions:
        print("풀이 파일을 찾지 못했다.", file=sys.stderr)
        return 1

    solutions = drop_too_fresh(solutions, datetime.now(timezone.utc))

    state = load_state()
    topic = TOPICS[state.get("syntax_cursor", 0) % len(TOPICS)]
    algo_path, algo_readme, algo_problem = pick_algo(solutions, state)

    prompt = build_prompt(topic, algo_path, algo_readme, algo_problem, today, args.provider)
    os.makedirs(os.path.dirname(PROMPT_PATH), exist_ok=True)
    with open(PROMPT_PATH, "w", encoding="utf-8") as f:
        f.write(prompt)

    state["syntax_cursor"] = (state.get("syntax_cursor", 0) + 1) % len(TOPICS)
    rec = state["items"].setdefault(algo_path, {"count": 0})
    rec["last_shown"] = today.isoformat()
    rec["count"] = rec.get("count", 0) + 1
    state["last_run"] = today.isoformat()
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"문법 주제: {topic}")
    print(f"알고리즘 소재: {algo_path} (누적 {rec['count']}회)")
    print(f"문제 본문: {algo_problem or '없음 — 코드에서 역추론한다'}")
    print(f"생성기: {args.provider}")
    return 0


def build_prompt(topic, algo_path, algo_readme, algo_problem, today, provider="codex"):
    if algo_problem:
        source_block = f"""- 문제 본문: `{algo_problem}` ← **이 파일이 문제의 정답 출처다.**
- 메타데이터 README: `{algo_readme}`""" if algo_readme else f"- 문제 본문: `{algo_problem}` ← **이 파일이 문제의 정답 출처다.**"
        knowledge_rule = """이 문제는 본문이 레포에 있다. 제약조건과 입력 형식을 본문에서 확인하고 쓴다.
본문에 없는 수치는 지어내지 않는다."""
    else:
        source_block = (
            f"- 메타데이터 README: `{algo_readme}`" if algo_readme else "- README 없음. 파일 경로에서 문제를 유추할 것."
        )
        knowledge_rule = """**중요 — 너는 이 문제의 본문을 모른다.**
CodeTree 플러그인이 만든 README 에는 제목·링크·유형·난이도만 있고 문제 설명, 입력 형식,
제약조건(n 의 범위, 값의 범위)이 전혀 없다. 문제 페이지는 로그인이 필요해 가져올 수도 없다.
그러니 네가 가진 것은 제목과 유형, 그리고 주인이 쓴 코드뿐이다. 아래를 지킨다.

- 문제 요약은 **코드에서 역추론한 것**임을 밝힌다. 확정된 사실처럼 쓰지 않는다.
- 제약조건을 아는 척하지 않는다. `n=100 이면 9만 번` 처럼 근거 없는 수치를 사실로 쓰지 말고,
  꼭 필요하면 `n 이 100 정도라고 가정하면` 처럼 가정임을 드러낸다.
- 복잡도는 n, k 같은 기호로 말한다. 기호로 말하는 데는 제약이 필요 없다.
- 코드가 특정 값을 가정하고 있다면(예: `== 1` 비교), 그것을 단정적으로 버그라고 부르지 않는다.
  "값이 0/1 이 아닌 문제였다면 여기가 먼저 깨진다. 원래 제약이 무엇이었나?" 처럼
  주인에게 되묻는 형태로 쓴다. 주인은 이 문제를 풀어봤으니 답을 안다 — 그게 좋은 복습이다.
- 질문 하나는 반드시 원래 제약조건을 떠올리게 하는 것으로 만든다."""

    if provider == "codex":
        task_line = """아래 스키마에 맞는 JSON 객체 하나를 **최종 응답으로** 낸다.
파일을 쓰지 않는다. 레포 파일은 읽기만 한다. 설명이나 인사말을 덧붙이지 않는다."""
        output_line = "최종 응답은 아래 스키마를 따르는 JSON 객체 하나다. 응답 형태는 스키마로 강제된다."
    else:
        task_line = """`.review/today.json` 파일 하나를 쓴다. 그게 전부다. 다른 파일은 건드리지 않는다."""
        output_line = "`.review/today.json` 에 아래 스키마로 정확히 쓴다."

    return f"""오늘은 {today.isoformat()}. 이 레포 주인이 출근길 지하철에서 읽을 복습 카드를 만든다.
주인은 C++ 를 한동안 안 써서 문법 감이 무뎌졌고, 예전에 푼 알고리즘 문제를 머릿속으로 다시 굴려보고 싶어 한다.

## 해야 할 일

{task_line}

### 1. C++ 문법 노트

오늘 주제: **{topic}**

- `headline` 은 이 주제를 한 문장으로 압축한 결론이다. 카드를 열자마자 보이는 줄이라 여기서 승부가 난다.
- `body` 는 왜 그런지를 짧게 푼다. 불릿 2~3개로 쪼갠다. 산문 문단을 쓰지 않는다.
- `code` 는 코드블록 하나다. 틀리기 쉬운 예와 고친 예를 위아래로 놓고 주석으로 가리킨다.
  `// 이렇게 쓰기 쉽다` 와 `// 이렇게 고친다` 처럼 한국어 주석을 붙인다.
  `#if 0` / `#else` 같은 전처리기로 두 버전을 가르지 않는다. 읽기 어렵다.
  줄 수는 15줄 안쪽. `#include` 와 `int main()` 은 꼭 필요할 때만 넣는다.
- `quiz` 는 한 문제만. 답은 `answer` 에 담는다 (Discord 스포일러로 가려진다).
- 가능하면 이 레포의 실제 `.cpp` 코드에서 해당 문법이 쓰인 자리를 찾아 인용한다.

### 2. 알고리즘 복습

오늘 소재:
- 풀이 파일: `{algo_path}`
{source_block}

{knowledge_rule}

파일을 먼저 읽는다. 그리고:

- `summary` 는 문제가 무엇을 요구하는지 두세 줄. 정답 알고리즘을 미리 말하지 않는다.
  본문 없이 코드에서 역추론했다면 첫머리에 `(코드에서 역추론)` 을 붙인다.
- `tag` 는 README 의 유형과 난이도를 그대로 옮긴 짧은 한 줄이다. 예: `Simulation · 격자 완전탐색 · 쉬움`
- 지하철에서 눈 감고 굴려볼 만한 질문을 하나 던진다. "어떻게 접근하지?" 수준이 아니라
  "왜 이 접근이 되는가", "복잡도가 왜 이렇게 나오는가", "입력이 10배 커지면 무엇이 먼저 터지는가"
  처럼 사고를 요구하는 질문이어야 한다.
- 그 답과 핵심 아이디어, 시간/공간 복잡도를 별도 필드에 쓴다 (스포일러로 가려진다).
- `code_review` 는 번호 매긴 지적 1~3개다. 각 항목은 두 줄을 넘기지 않는다.
  근거 없는 트집이 아니라 진짜 문제(불필요한 복사, 초기화 실수, signed/unsigned 비교,
  자료구조 선택, 가독성)만 짚는다.

### 3. 더 나은 풀이

같은 문제를 더 잘 푸는 방법이 있는지 정직하게 판정한다.

- 판정은 셋 중 하나다: `개선 여지 있음` / `상수만 개선` / `이미 최적`.
- **개선 여지 있음** — 시간이나 공간 복잡도가 실제로 내려가는 경우다. 무엇을 미리 계산해두면
  무엇이 사라지는지, 어떤 자료구조로 바꾸면 어떤 연산이 O(1) 이 되는지를 말한다.
- **상수만 개선** — 복잡도는 같지만 캐시 지역성, 불필요한 복사 제거, 조기 종료 등으로 빨라지는 경우다.
- **이미 최적** — 억지로 다른 풀이를 지어내지 않는다. 대신 **왜** 이 이상 줄일 수 없는지를 설명한다.
  (입력을 전부 읽어야 하므로 O(n) 하한이다, 정렬이 병목인데 비교 기반이라 O(n log n) 이 하한이다 등)
- 판정 근거에 입력 크기가 필요한데 제약을 모른다면, 그 사실을 적고 기호로만 비교한다.
  모르는 제약을 가정해 "이 정도면 충분하다" 같은 결론을 내리지 않는다.
- `idea` 는 무엇을 바꾸는지, 왜 되는지. 불릿 2~3개로 쪼갠다.
- `code` 는 C++ 코드블록 하나. 전체를 다시 쓰지 말고 핵심만 20줄 안쪽으로.
  `이미 최적` 이면 원래 풀이를 C++ 로 옮긴 관용적인 형태를 보여준다.
- `gain` 은 무엇이 얼마나 좋아지는지 한 줄로 못박는다. (예: `O(n²k²) → O(n²), k 가 식에서 사라진다`)

## 한국어 문장 규칙

읽는 곳은 지하철에서 보는 휴대폰 화면이다. 길면 안 읽는다.

- **한 문단은 세 줄을 넘기지 않는다.** 넘으면 불릿으로 쪼갠다.
- 불릿 하나는 한두 줄. 불릿 안에서 다시 문단을 만들지 않는다.
- 굵게(`**`)는 한 덩어리에 한 번만. 다 굵으면 아무것도 안 굵은 것과 같다.
- 만연체를 쓰지 않는다. `~하게 되는 것이다` → `~한다`. `~라고 할 수 있다` → `~다`.
- 번역투를 피한다. `~에 대해`, `~를 통해`, `~하는 것을 통해`, `~에 있어서` 대신
  `~을`, `~로`, `~하면` 을 쓴다.
- **영어를 원형으로 두는 건 코드에 실제로 나오는 이름뿐이다.** `vector`, `sync_with_stdio`,
  `iterator`, `unordered_map` 처럼 타이핑하는 식별자만 그렇다.
  일반 명사는 한국어로 쓴다. buffering→버퍼링, stream→스트림, list→리스트,
  prompt→프롬프트, ring buffer→링 버퍼. 한 문장에 영어 단어가 셋 이상이면 다시 쓴다.
- 숫자와 기호는 붙여 쓴다. `O(n²)`, `3×3`, `k×k`.
- 설명하다 말고 결론을 뒤로 미루지 않는다. 결론을 먼저 쓰고 이유를 뒤에 붙인다.

## 출력 형식

{output_line} 모든 값은 한국어.
Discord 마크다운을 쓴다 (`**굵게**`, 인라인 코드는 백틱, 코드블록은 백틱 3개 + `cpp`).

```json
{{
  "date": "{today.isoformat()}",
  "syntax": {{
    "topic": "주제 이름. 50자 이내.",
    "headline": "한 문장 결론. 80자 이내.",
    "body": "왜 그런지. 불릿 2~3개. 380자 이내.",
    "code": "코드블록 하나. 15줄, 600자 이내.",
    "quiz": "확인 퀴즈 한 문제. 200자 이내.",
    "answer": "정답과 이유. 세 문장 이내, 380자 이내."
  }},
  "algo": {{
    "title": "문제 제목",
    "link": "README 에 있던 문제 URL. 없으면 빈 문자열.",
    "path": "{algo_path}",
    "tag": "유형 · 세부분류 · 난이도. 60자 이내.",
    "summary": "문제 요약. 300자 이내.",
    "question": "생각해볼 질문. 250자 이내.",
    "answer": "핵심 아이디어 + 복잡도. 세 문장 이내, 550자 이내.",
    "code_review": "번호 매긴 지적 1~3개. 항목당 두 줄. 480자 이내."
  }},
  "optimized": {{
    "verdict": "개선 여지 있음 | 상수만 개선 | 이미 최적",
    "idea": "무엇을 바꾸고 왜 되는가. 불릿 2~3개. 380자 이내.",
    "code": "C++ 코드블록 하나. 20줄, 600자 이내.",
    "gain": "무엇이 얼마나 좋아지는가 한 줄. 120자 이내."
  }}
}}
```

**글자 수 상한을 반드시 지킨다.** Discord 임베드 필드는 1024자에서 잘린다.
상한은 넉넉히 잡은 게 아니라 잘리지 않는 한계선이다. 짧게 쓰는 쪽이 항상 낫다.

`syntax.answer` 와 `algo.answer` 는 스포일러(`||...||`)로 **통째로** 감싸져 전송된다.
한 번 누르면 전부 열린다.

- 이 두 필드에는 코드블록을 쓰지 않는다. 스포일러 안에서 깨진다. 짧은 인라인 코드만 쓴다.
- 이 두 필드에 `||` 를 직접 쓰지 않는다. 스포일러가 거기서 끊긴다.
- 세 문장을 넘기지 않는다. 결론 한 문장, 이유 한두 문장이면 충분하다.

`code`, `body`, `code_review`, `idea` 에는 코드블록을 써도 된다.

JSON 은 유효해야 한다. 코드블록 안의 줄바꿈은 `\\n` 으로 이스케이프한다.
"""


if __name__ == "__main__":
    raise SystemExit(main())

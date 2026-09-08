#!/usr/bin/env bash
# 복습 카드를 생성한다. 어떤 CLI 를 쓸지는 REVIEW_PROVIDER 가 정한다.
#
#   codex  (기본) — codex exec. --output-schema 로 응답 형태를 강제하므로
#                    모델이 스키마를 벗어날 여지가 거의 없다.
#   claude         — claude -p. 에이전트가 Write 툴로 파일을 만든다.
#
# 두 경로 모두 .review/today.json 을 남기고 같은 검증을 통과해야 한다.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

PROVIDER="${REVIEW_PROVIDER:-codex}"
PROMPT_PATH=".review/prompt.md"
OUT_PATH=".review/today.json"
SCHEMA_PATH="scripts/today.schema.json"
ENVELOPE_PATH=".review/cli-output.json"
LOG_PATH=".review/cli-output.log"

if [[ ! -f "$PROMPT_PATH" ]]; then
  echo "$PROMPT_PATH 가 없다. 먼저 scripts/pick_topic.py 를 돌린다." >&2
  exit 1
fi

rm -f "$OUT_PATH" "$ENVELOPE_PATH" "$LOG_PATH"

case "$PROVIDER" in
  codex)
    MODEL="${CODEX_MODEL:-gpt-5.6-sol}"
    echo "생성기: codex exec (모델 $MODEL)"
    # read-only 샌드박스면 충분하다. 카드는 최종 응답으로 돌아오고,
    # -o 가 그 응답을 파일로 떨어뜨린다. 모델이 파일을 쓸 필요가 없다.
    codex exec \
      --model "$MODEL" \
      --sandbox read-only \
      --cd "$REPO" \
      --output-schema "$SCHEMA_PATH" \
      --output-last-message "$OUT_PATH" \
      "$(cat "$PROMPT_PATH")" > "$LOG_PATH"
    # codex 는 최종 JSON 을 stdout 에도 그대로 뱉는다. 카드 전문이 CI 로그에
    # 남을 이유가 없으므로 파일로 돌린다. 실패하면 아래 검증이 잡는다.
    python3 scripts/validate_today.py
    ;;

  claude)
    MODEL="${CLAUDE_MODEL:-fable}"
    echo "생성기: claude -p (모델 $MODEL)"
    claude -p "$(cat "$PROMPT_PATH")" \
      --model "$MODEL" \
      --restricted \
      --allowedTools "Read,Write,Glob,Grep" \
      --permission-mode acceptEdits \
      --output-format json > "$ENVELOPE_PATH"
    python3 scripts/validate_today.py --envelope "$ENVELOPE_PATH"
    ;;

  *)
    echo "REVIEW_PROVIDER 는 codex 또는 claude 여야 한다 (받은 값: $PROVIDER)" >&2
    exit 1
    ;;
esac

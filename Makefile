.PHONY: pick generate dry send review clean

# 카드를 만들 CLI. codex 또는 claude.
#   make review REVIEW_PROVIDER=claude  처럼 한 번만 바꿔 쓸 수 있다.
REVIEW_PROVIDER ?= codex

# 각 CLI 가 쓸 모델. 해당 provider 일 때만 의미가 있다.
CODEX_MODEL  ?= gpt-5.6-sol
CLAUDE_MODEL ?= fable

export REVIEW_PROVIDER CODEX_MODEL CLAUDE_MODEL

# 오늘 소재를 고르고 프롬프트를 만든다 (.review/state.json 이 갱신된다)
pick:
	python3 scripts/pick_topic.py --provider $(REVIEW_PROVIDER)

# 복습 카드를 생성하고 검증한다
generate:
	bash scripts/generate.sh

# 전송 없이 화면으로만 확인
dry:
	DRY_RUN=1 python3 scripts/post_discord.py

# 실제 Discord 전송 (.env 의 DISCORD_TIL_WEBHOOK 사용)
send:
	python3 scripts/post_discord.py

# 한 바퀴 전부 (선정 → 생성 → 전송)
review: pick generate send

# 중간 산출물 정리. state.json 과 archive 는 건드리지 않는다
clean:
	rm -f .review/prompt.md .review/today.json .review/cli-output.json .review/cli-output.log

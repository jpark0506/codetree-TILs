# 아침 복습 자동화

매일 아침 Discord 로 복습 카드 두 장을 보낸다.

- **📘 C++ 문법** — 한 줄 결론 → 왜 그런가 → 코드 → 확인 퀴즈 → 정답(스포일러)
- **🧠 알고리즘** — 문제 요약 → 분류 → 생각해보기 → 핵심 아이디어(스포일러) → 내 코드 지적. 문제 링크는 버튼.
- **⚡ 더 나은 풀이** — `개선 여지 있음` / `상수만 개선` / `이미 최적` 판정 → 아이디어 → C++ 코드

**가독성이 이 자동화의 최우선 기준이다.** 지하철에서 휴대폰으로 읽는 글이라 길면 안 읽힌다.

- 본문을 임베드 `description` 에 몰지 않고 **필드로 쪼갠다.** 필드는 제목이 따로 렌더링되고
  값이 1024자에서 잘리므로, 훑어 읽기 좋고 모델이 늘어놓는 것도 막힌다.
- 필드 이름에 이모지를 일관되게 붙여 눈이 걸리게 한다 (💡 왜 그런가 · 💻 코드 · 🔑 정답 · 🤔 생각해보기).
- **스포일러는 통째로 한 덩어리다.** 줄 단위로 감싸면 정답을 보려고 여러 번 눌러야 한다.
- 프롬프트에 한국어 문장 규칙을 넣었다. 문단 3줄 제한, 만연체·번역투 금지, 결론 먼저,
  그리고 **영어 원형은 코드에 실제 나오는 식별자만** (buffering→버퍼링, ring buffer→링 버퍼).
- 코드 예시는 전처리기 분기(`#if 0`) 없이 `// 이렇게 쓰기 쉽다` / `// 이렇게 고친다` 로 위아래 대조한다.

구조와 규약은 `hyper-whale-tracker` 를 따랐다. Discord 전송은 `internal/notify/discord.go`,
Claude Code 헤드리스 호출과 출력 복구는 `internal/interpret/claude.go` 를 파이썬으로 옮긴 것이다.

## 동작 방식

```
.github/workflows/daily-review.yml   매일 07:45 KST 실행 (cron: 45 22 * * * UTC)
scripts/syntax_topics.py             C++ 문법 커리큘럼 40개
scripts/pick_topic.py                오늘 소재 선정 → .review/prompt.md 생성
scripts/generate.sh                  provider 에 따라 codex 또는 claude 로 카드 생성
scripts/today.schema.json            카드 JSON Schema (codex 가 응답 형태 강제에 쓴다)
.review/today.json                   생성된 복습 카드
scripts/validate_today.py            필수 항목 검사 + 코드펜스/산문 복구 (+ claude 봉투 is_error)
scripts/post_discord.py              Discord 임베드 3장 전송
.review/state.json                   출제 이력 (커밋됨)
.review/archive/YYYY-MM-DD.json      지난 카드 보관 (커밋됨)
```

## 생성기 두 가지

`REVIEW_PROVIDER` 로 고른다. **기본은 codex.**

| | codex (기본) | claude |
|---|---|---|
| 명령 | `codex exec` | `claude -p` |
| 출력 방식 | 최종 응답이 곧 카드. `--output-schema` 로 형태를 강제하고 `-o` 로 파일에 받는다 | 에이전트가 Write 툴로 `.review/today.json` 을 만든다 |
| 샌드박스 | `read-only` | `--restricted` + `Read,Write,Glob,Grep` |
| 모델 | `CODEX_MODEL` (기본 `gpt-5.6-sol`) | `CLAUDE_MODEL` (기본 `fable`) |
| CI 인증 | `CODEX_AUTH_JSON` 시크릿 (아래 참고) | `CLAUDE_CODE_OAUTH_TOKEN` 시크릿 |

codex 쪽이 JSON Schema 로 응답 형태를 강제하므로 파싱이 거의 안 깨진다.
claude 쪽은 인증이 단순하다(장수명 토큰 하나). 한쪽이 막히면 변수 하나로 갈아탄다.

```bash
gh variable set REVIEW_PROVIDER --body claude   # 다음 실행부터 claude
gh workflow run daily-review.yml -f provider=claude   # 이번 한 번만 claude
```

## 문제 본문에 관한 한계

CodeTree 플러그인이 만드는 각 폴더의 `README.md` 에는 **제목·링크·유형·난이도만 있고
문제 설명, 입력 형식, 제약조건이 없다.** 문제 페이지는 로그인이 필요한 SPA 라 가져올 수도 없다.

그래서 기본 상태에서 카드 생성기가 아는 것은 **제목과 유형, 그리고 내가 쓴 코드**뿐이고,
문제는 코드에서 역추론한다. 이 사실은 감추지 않는다.

- 요약 첫머리에 `(코드에서 역추론)` 을 붙인다.
- 제약을 모르므로 `n=100 이면 9만 번` 같은 구체적 수치를 지어내지 않고 `Θ(n²)` 처럼 기호로만 말한다.
- `== 1` 비교처럼 코드가 특정 값을 가정하는 자리는 버그로 단정하지 않고
  "원래 제약이 무엇이었나?" 로 되묻는다. 문제를 풀어본 사람은 나이므로, 되묻는 편이 복습이 된다.

**문제 본문을 넣어두면 더 정확해진다.** 풀이 파일과 같은 폴더에 `PROBLEM.md` 를 만들고
문제 설명과 제약조건을 붙여넣으면, 그때부터 그 파일을 정답 출처로 삼고 추론 모드를 끈다.

```
240215/최고의 33위치/
├── README.md              (플러그인 생성 — 메타데이터만)
├── PROBLEM.md             (직접 붙여넣기 — 있으면 이걸 쓴다)
└── best-place-of-33.py
```

전부 채울 필요는 없다. 카드에 나온 문제부터 하나씩 채워도 다음 순번에 반영된다.

**소재 선정 규칙**

- 문법 주제는 커리큘럼 40개를 커서로 하나씩 순환한다. 40일이면 한 바퀴.
- 알고리즘은 아직 안 나온 풀이 파일이 우선이고, 다 돌면 마지막 출제일이 가장 오래된 것부터 다시 나온다.
- 워크플로는 **실행 시점에 체크아웃**한다. 새벽에 풀어 push 한 문제도 그날 아침 후보에 들어간다.
  그런 문제는 미출제라 1순위로 뽑히는데, 푼 지 몇 시간 만에 복습하는 게 싫으면
  `REVIEW_MIN_AGE_HOURS=24` 를 주면 하루 묵힌 것만 대상이 된다 (기본값 0 = 전부 포함).
  기준을 세게 잡아 후보가 하나도 안 남으면 경고를 찍고 전체를 대상으로 되돌린다.

**전송 규약** (hyper-whale-tracker 와 동일)

- 429 는 응답 본문의 `retry_after` 를 헤더보다 우선해 최대 3회까지 재시도한다.
- 5xx 는 1초 뒤 한 번 더 시도하고, 그 밖의 4xx 는 재시도해도 나아지지 않으므로 즉시 실패한다.
- `APP_ENVIRONMENT` 가 production 이 아니면 사용자명에 배지가 붙는다 (`복습 [DEV]`).

## 최초 설정

### 1. Discord 웹훅

```bash
gh secret set DISCORD_TIL_WEBHOOK
```

> 이 레포는 **공개 레포**다. 웹훅 URL 과 토큰은 절대 파일에 적어 커밋하지 않는다.
> 웹훅 URL 을 아는 사람은 누구나 그 채널에 글을 쓸 수 있다.

### 2-A. codex 인증 (기본 경로)

로컬에서 `codex login` 이 끝나 있고 `~/.codex/auth.json` 이 `auth_mode: "chatgpt"` 면 그 파일을 그대로 올린다.

```bash
gh secret set CODEX_AUTH_JSON < ~/.codex/auth.json
```

이 방식은 OpenAI 가 문서화한 [CI/CD 인증 유지](https://learn.chatgpt.com/docs/auth/ci-cd-auth) 절차를 따른다.
`auth.json` 안의 refresh token 으로 Codex 가 알아서 토큰을 갱신한다
(`last_refresh` 가 8일쯤 지나면 실행 전에 갱신하고, 401 을 받아도 갱신 후 재시도한다).

**갱신분을 보존하는 게 핵심이다.** 러너는 매번 사라지므로, 워크플로가 실행 뒤
바뀐 `auth.json` 을 시크릿에 되쓴다. 이걸 하려면 시크릿 쓰기 권한이 있는 토큰이 하나 더 필요하다.

```bash
# github.com/settings/personal-access-tokens 에서 fine-grained 토큰 발급
#   Repository access : jpark0506/codetree-TILs
#   Permissions       : Secrets = Read and write
gh secret set GH_SECRETS_TOKEN
```

`GH_SECRETS_TOKEN` 이 없으면 워크플로는 경고만 남기고 계속 돈다. 대신 토큰이 만료되면
`codex login` 을 다시 하고 `CODEX_AUTH_JSON` 을 갈아끼워야 한다.

> **캐시(`actions/cache`)를 쓰지 않는 이유.** 이 레포는 공개다. 포크에서 올라온 PR 워크플로가
> base 브랜치 캐시를 복원할 수 있어, 캐시에 자격증명을 두면 새어나갈 수 있다.
> 시크릿은 포크 PR 에 전달되지 않으므로 시크릿 되쓰기만 쓴다.

### 2-B. claude 인증 (대체 경로)

```bash
claude setup-token                      # 구독으로 인증되는 장수명 토큰
gh secret set CLAUDE_CODE_OAUTH_TOKEN
```

Claude 구독(Pro/Max)으로 동작하며 **API 별도 과금이 없다.**

### 3. 수동 실행으로 확인

```bash
gh workflow run daily-review.yml
gh run watch
```

## 로컬에서 돌리기

`.env.example` 을 `.env` 로 복사해 값을 채운다 (`.env` 는 gitignore 된다).

```bash
make pick        # 소재 선정 → 프롬프트 생성
make generate    # 카드 생성 + 검증
make dry         # 전송 없이 화면 출력
make send        # 실제 Discord 전송
make review      # 위 세 단계 한 번에 (pick → generate → send)
make clean       # 중간 산출물 정리

make review REVIEW_PROVIDER=claude   # 이번만 claude 로
```

로컬에서는 `codex login` / `claude` 로그인이 돼 있으면 시크릿 설정 없이 그냥 돈다.

로컬 실행도 `.review/state.json` 을 실제로 바꾼다. 되돌리려면 `git checkout .review/state.json`.

## 알아둘 것

- GitHub Actions 의 스케줄은 정각에 부하가 몰려 수십 분 늦을 수 있다. 그래서 07:45 로 잡아 08:00 근처에 도착하게 했다.
- 레포에 60일간 활동이 없으면 GitHub 이 스케줄 워크플로를 자동으로 끈다. 이 워크플로가 매일 상태를 커밋하므로 보통은 문제없다.
- 문법 주제를 바꾸거나 추가하려면 `scripts/syntax_topics.py` 의 `TOPICS` 를 고친다.
- 출제 간격이나 선정 규칙은 `scripts/pick_topic.py` 의 `pick_algo` 에 있다.
- 임베드 설명은 4096자, 메시지 하나에 총 6000자가 한계라 카드를 두 번에 나눠 보낸다.

# Superpowers Integration

이 문서는 Superpowers를 설치한 에이전트 환경에서 ragSystem_codex 하네스와 함께 쓰는 방법을 정리한다.

## Sources

- Repository: https://github.com/obra/superpowers
- Codex guide: https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/docs/README.codex.md

## Priority

우선순위는 아래 순서다.

1. 사용자 명시 지시
2. 이 리포지터리의 `AGENTS.md`
3. `docs/` 하네스 문서
4. 설치된 Superpowers skill
5. 기본 에이전트 동작

Superpowers skill이 더 강한 절차를 요구하더라도 사용자 승인, 브랜치 생성, PR/merge, 문서 위치 규칙은 이 리포지터리 규칙을 따른다.

## Skill Mapping

| Superpowers skill | Harness location | Use |
| --- | --- | --- |
| `brainstorming` | `docs/product-specs/`, `docs/design-docs/`, `docs/references/` | 요구사항, eval 기준, 설계 승인 정리 |
| `writing-plans` | `docs/exec-plans/active/` | 실행 가능한 작업 계획 작성 |
| `using-git-worktrees` | `.worktrees/`, 작업 브랜치 | 승인된 구현 작업 격리 |
| `test-driven-development` | 테스트 코드, eval case, `docs/QUALITY_SCORE.md` | 실패 테스트 또는 재현 eval 우선 구현 |
| `systematic-debugging` | `docs/RELIABILITY.md`, active plan | 원인 조사 후 수정 |
| `requesting-code-review` | PR 전 또는 task 완료 후 | 요구사항 충족과 코드 품질 검토 |
| `verification-before-completion` | active plan `Validation Result` | 완료 선언 전 증거 확인 |
| `finishing-a-development-branch` | `docs/HANDOFF.md`, completed plan | 검증, merge/PR 판단, 인계 갱신 |

## Operating Profile

1. 새 기능, prompt, retrieval, eval, deployment 변경은 요구사항과 성공 기준을 먼저 정리한다.
2. 승인된 설계는 제품 명세, 설계 문서, reference report, active exec plan 중 적절한 위치에 남긴다.
3. 구현 계획은 작은 checkbox task로 나누고 파일 경로, 테스트/eval 명령, 기대 결과를 포함한다.
4. 사용자 승인 후 작업 브랜치 또는 격리 worktree에서 구현한다.
5. 기능과 버그 수정은 가능한 한 RED-GREEN-REFACTOR 또는 eval-first 순서로 진행한다.
6. RAG 품질 변경은 관련 eval subset, source drift, trace, latency 증거 중 적절한 검증을 남긴다.
7. task 완료 시 요구사항 충족 리뷰와 코드 품질 리뷰를 분리한다.
8. 완료 전 실제 검증 결과를 active plan에 기록한다.
9. 완료된 계획은 `docs/exec-plans/completed/`로 이동하고 `docs/index.md`와 `docs/HANDOFF.md`를 갱신한다.
10. PR 생성 또는 갱신 시 title/body/요약 설명은 `AGENTS.md` 규칙에 따라 한글로 작성한다.

## Installation Note

Codex에서 수동 설치하는 경우 일반 흐름은 아래와 같다.

```bash
git clone https://github.com/obra/superpowers.git ~/.codex/superpowers
mkdir -p ~/.agents/skills
ln -s ~/.codex/superpowers/skills/<skill> ~/.agents/skills/superpowers-<skill>
```

설치 후 Codex를 재시작해야 새 skill 목록이 발견된다. subagent 기반 workflow는 Codex의 multi-agent 기능이 켜져 있어야 한다.

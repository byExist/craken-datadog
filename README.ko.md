<h1 align="center">Datadog</h1>

<p align="center">
  <a href="https://github.com/byExist/craken-datadog/actions/workflows/ci.yml"><img src="https://github.com/byExist/craken-datadog/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/byExist/craken"><img src="https://img.shields.io/badge/Claude_Code-plugin-da7756" alt="Claude Code plugin"></a>
  <img src="https://img.shields.io/badge/python-3.13+-3776AB?logo=python&logoColor=white" alt="Python 3.13+">
</p>

<p align="center">
  Claude에서 Datadog — 로그·APM 트레이스·메트릭·모니터·인시던트 등을 공식 API 위에서, 읽기 전용으로.
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

---

## 왜 datadog인가?

Datadog API는 표면이 넓습니다 — 로그, RUM 이벤트, APM 트레이스, 메트릭, 모니터, 이벤트, 인시던트, SLO, 다운타임, 대시보드, 신서틱, 호스트, 컨테이너, 프로세스, 서비스 카탈로그. 이 플러그인은 v1/v2 REST API를 [`httpx`](https://www.python-httpx.org/)로 직접 호출합니다 — 30 MB짜리 생성 SDK 없이 — 그리고 모든 응답을 compact한 typed 모델로 투영합니다: None 필드는 덜어내고, 깊고 변동 잦은 구조는 보존하되 타입은 생략해, 조사 결과가 엔벨로프 더미가 아니라 신호로 돌아옵니다.

**설계상 읽기 전용입니다.** 모든 도구는 목록·조회·검색·집계만 합니다 — 쓰기 표면도 설정 토글도 없어, 활성화해도 모니터·인시던트·대시보드를 읽을 뿐 바꾸지 않습니다. 닿을 수 있는 범위는 **application key의 권한**이 결정하며, 거부된 호출은 (키에 권한이 없다는 안내와 함께) actionable한 에러로 돌아옵니다 — 조용한 빈 결과가 아니라.

## 설치

datadog은 MCP 서버를 [uv](https://docs.astral.sh/uv/)로 실행하므로 uv가 `PATH`에 있어야 합니다:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux — Windows는 uv 문서 참고
```

```bash
/plugin marketplace add byExist/craken
/plugin install datadog@craken
```

**비활성 상태로 설치됩니다** — Datadog 조직에 연결되므로, 활성화(`/plugin` 메뉴 또는 `claude plugin enable datadog`)로 직접 opt-in 하면 아래 설정을 묻습니다. 키는 `settings.json`이 아니라 OS 키체인에 저장되고, `/plugin config datadog`로 언제든 다시 설정할 수 있습니다.

| 설정 | 설명 |
| --- | --- |
| Datadog API key | 조직을 식별. Organization Settings → API Keys에서 생성. |
| Datadog application key | 사용자를 식별하고 읽기 / 쿼리 엔드포인트를 인가. Organization Settings → Application Keys에서 생성. |
| Datadog site | 로그인 후 URL에서 보이는 리전. 기본값 `datadoghq.com`(US1); `us3`/`us5`/`datadoghq.eu`/`ap1`/`ddog-gov.com`이면 설정. |

## 도구

도구는 `datadog` MCP 서버 아래 bare 이름으로 노출됩니다(예: `search_logs`). 로그·스팬 검색은 Datadog [쿼리 문자열](https://docs.datadoghq.com/logs/explorer/search_syntax/)을 받고, 메트릭 쿼리는 v2 formula API를 씁니다. 시간 범위는 `now-15m` 같은 상대값(로그 / 스팬 / 이벤트) 또는 epoch 밀리초(메트릭)를 받습니다.

| 영역 | 도구 |
| --- | --- |
| 로그 | `search_logs` · `aggregate_logs` |
| RUM | `search_rum_events` · `aggregate_rum_events` |
| 스팬 | `search_spans` · `aggregate_spans` |
| 트레이스 | `get_trace` · `get_pruned_trace` (preview) |
| 메트릭 | `query_timeseries` · `query_scalar` · `list_metrics` |
| 모니터 | `list_monitors` · `get_monitor` · `search_monitors` |
| 이벤트 | `list_events` · `get_event` |
| 인시던트 | `list_incidents` · `get_incident` · `search_incidents` |
| SLO | `list_slos` · `get_slo` · `get_slo_status` (preview) |
| 다운타임 | `list_downtimes` · `get_downtime` |
| 대시보드 | `list_dashboards` · `get_dashboard` |
| 서비스 카탈로그 | `list_catalog_entities` · `get_service_definition` |
| 신서틱 | `list_synthetic_tests` · `get_api_test_results` · `get_browser_test_results` |
| 호스트 | `list_hosts` · `get_host_totals` |
| 컨테이너 | `list_containers` |
| 프로세스 | `list_processes` |

## 개발

```bash
uv sync
uv run pytest
uv run pyright
```

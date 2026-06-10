<h1 align="center">Datadog</h1>

<p align="center">
  <a href="https://github.com/byExist/craken-datadog/actions/workflows/ci.yml"><img src="https://github.com/byExist/craken-datadog/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/byExist/craken"><img src="https://img.shields.io/badge/Claude_Code-plugin-da7756" alt="Claude Code plugin"></a>
  <img src="https://img.shields.io/badge/python-3.13+-3776AB?logo=python&logoColor=white" alt="Python 3.13+">
</p>

<p align="center">
  Datadog in Claude — logs, APM traces, metrics, monitors, incidents, and more, read-only over the official API.
</p>

<p align="center">
  <a href="README.ko.md">한국어</a>
</p>

---

## Why datadog?

Datadog's API is a sprawling surface — logs, RUM events, APM traces, metrics, monitors, events, incidents, SLOs, downtimes, dashboards, synthetics, hosts, containers, processes, and the service catalog. This plugin talks to the v1/v2 REST API directly over [`httpx`](https://www.python-httpx.org/) — no 30 MB generated SDK — and projects every response into compact typed models: null fields are dropped and deep, volatile structures are kept but left untyped, so an investigation comes back as signal rather than pages of envelope.

It is **read-only by design**. Every tool lists, gets, searches, or aggregates; there is no write surface and no config toggle, so enabling it can read your monitors, incidents, and dashboards but never change them. What you can reach is bounded by your **application key's permissions** — a denied call returns an actionable error (with a note that the key lacks the permission), not a silent empty.

## Installation

datadog runs its MCP server through [uv](https://docs.astral.sh/uv/), so uv must be on your `PATH`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux — see the uv docs for Windows
```

```bash
/plugin marketplace add byExist/craken
/plugin install datadog@craken
```

**Installed disabled** — it connects to your Datadog organization, so you opt in by enabling it (`/plugin` menu, or `claude plugin enable datadog`), which prompts for the settings below. Keys are stored in your OS keychain, not `settings.json`; reconfigure anytime with `/plugin config datadog`.

| Setting | Description |
| --- | --- |
| Datadog API key | Identifies your organization. Create one at Organization Settings → API Keys. |
| Datadog application key | Identifies you and authorizes read / query endpoints. Create one at Organization Settings → Application Keys. |
| Datadog site | Your Datadog region, taken from the URL after you log in. Defaults to `datadoghq.com` (US1); set it for `us3`/`us5`/`datadoghq.eu`/`ap1`/`ddog-gov.com`. |

## Tools

Tools are exposed under the `datadog` MCP server by their bare names (e.g. `search_logs`). Log and span searches take a Datadog [query string](https://docs.datadoghq.com/logs/explorer/search_syntax/); metric queries use the v2 formula API. Time ranges accept relative values like `now-15m` (logs / spans / events) or epoch milliseconds (metrics).

| Domain | Tools |
| --- | --- |
| Logs | `search_logs` · `aggregate_logs` |
| RUM | `search_rum_events` · `aggregate_rum_events` |
| Spans | `search_spans` · `aggregate_spans` |
| Traces | `get_trace` · `get_pruned_trace` (preview) |
| Metrics | `query_timeseries` · `query_scalar` · `list_metrics` |
| Monitors | `list_monitors` · `get_monitor` · `search_monitors` |
| Events | `list_events` · `get_event` |
| Incidents | `list_incidents` · `get_incident` · `search_incidents` |
| SLOs | `list_slos` · `get_slo` · `get_slo_status` (preview) |
| Downtimes | `list_downtimes` · `get_downtime` |
| Dashboards | `list_dashboards` · `get_dashboard` |
| Service catalog | `list_catalog_entities` · `get_service_definition` |
| Synthetics | `list_synthetic_tests` · `get_api_test_results` · `get_browser_test_results` |
| Hosts | `list_hosts` · `get_host_totals` |
| Containers | `list_containers` |
| Processes | `list_processes` |

## Development

```bash
uv sync
uv run pytest
uv run pyright
```

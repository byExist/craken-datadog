"""Register Datadog MCP tools.

Read-only: every tool lists, gets, searches, or aggregates Datadog data. There
is no write surface and no config gate — the application key's permissions are
the only limit, and a 403 surfaces as an actionable ``DatadogError``.
"""

from collections.abc import Callable
from typing import Any

from mcp.server.fastmcp import FastMCP

from datadog_mcp import tools

mcp = FastMCP(
    "datadog",
    instructions=(
        "Read-only Datadog access: logs, RUM (real user monitoring) events, spans, "
        "full and pruned APM traces, metrics, monitors, events, incidents, SLOs (with "
        "live status), downtimes, dashboards, synthetics, hosts, and the service "
        "catalog. Search and aggregate logs, RUM, and spans with Datadog query "
        "syntax; fetch a whole trace by ID (use the pruned tree for a compact view); "
        "query metrics with the v2 formula API; list live containers and processes "
        "for infrastructure beneath hosts. Time ranges accept relative values like "
        "'now-15m' (logs/spans/events) or epoch milliseconds (metrics)."
    ),
)


def _register(fns: list[Callable[..., Any]]) -> None:
    for fn in fns:
        mcp.tool()(fn)


_register(
    [
        tools.search_logs,
        tools.aggregate_logs,
        tools.search_rum_events,
        tools.aggregate_rum_events,
        tools.list_hosts,
        tools.get_host_totals,
        tools.list_containers,
        tools.list_processes,
        tools.list_events,
        tools.get_event,
        tools.search_spans,
        tools.aggregate_spans,
        tools.get_trace,
        tools.get_pruned_trace,
        tools.list_monitors,
        tools.get_monitor,
        tools.search_monitors,
        tools.query_timeseries,
        tools.query_scalar,
        tools.list_metrics,
        tools.list_downtimes,
        tools.get_downtime,
        tools.list_slos,
        tools.get_slo,
        tools.get_slo_status,
        tools.list_dashboards,
        tools.get_dashboard,
        tools.list_catalog_entities,
        tools.get_service_definition,
        tools.list_incidents,
        tools.get_incident,
        tools.search_incidents,
        tools.list_synthetic_tests,
        tools.get_api_test_results,
        tools.get_browser_test_results,
    ],
)

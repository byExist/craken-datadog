"""Tests for datadog_mcp.server — tool registration.

server.py registers every tool at import time under their bare function names;
the MCP client namespaces them by server (``mcp__…datadog__<name>``). There is no
scope or write gate, so the full set is always present.
"""

from datadog_mcp.server import mcp

ALL = [
    "search_logs",
    "aggregate_logs",
    "search_rum_events",
    "aggregate_rum_events",
    "list_hosts",
    "get_host_totals",
    "list_containers",
    "list_processes",
    "list_events",
    "get_event",
    "search_spans",
    "aggregate_spans",
    "get_trace",
    "get_pruned_trace",
    "list_monitors",
    "get_monitor",
    "search_monitors",
    "query_timeseries",
    "query_scalar",
    "list_metrics",
    "list_downtimes",
    "get_downtime",
    "list_slos",
    "get_slo",
    "get_slo_status",
    "list_dashboards",
    "get_dashboard",
    "list_catalog_entities",
    "get_service_definition",
    "list_incidents",
    "get_incident",
    "search_incidents",
    "list_synthetic_tests",
    "get_api_test_results",
    "get_browser_test_results",
]


def _tool_map() -> dict[str, str]:
    return {
        tool.name: tool.description or "" for tool in mcp._tool_manager.list_tools()
    }


def test_all_tools_registered():
    tools = _tool_map()

    for name in ALL:
        assert name in tools
    assert len(tools) == len(ALL)


def test_all_tools_documented():
    tools = _tool_map()

    assert all(desc for desc in tools.values())

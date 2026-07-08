"""Minimal-valid payload builders for models with required fields.

Each returns the smallest wire dict (API field names) that ``model_validate``
accepts, so a future requiredness change is edited here once instead of across
every fixture. Only models that declare required fields need an entry; all-optional
models validate from ``{}``.
"""

from typing import Any


def apm_trace_span(**overrides: Any) -> dict[str, Any]:
    return {
        "service": "svc",
        "name": "op",
        "resource": "res",
        "spanID": 1,
        "traceID": 1,
        "traceIDFull": "0" * 32,
        "startTime": 0,
        "endTime": 0,
        "type": "web",
        **overrides,
    }


def summarized_span(**overrides: Any) -> dict[str, Any]:
    return {
        "service": "svc",
        "name": "op",
        "resource": "res",
        "spanID": 1,
        "startTime": "2026-01-01T00:00:00Z",
        "endTime": "2026-01-01T00:00:00Z",
        "durationSeconds": 0.0,
        **overrides,
    }


def monitor(**overrides: Any) -> dict[str, Any]:
    return {"type": "metric alert", "query": "avg(last_5m):x > 1", **overrides}


def monitor_asset(**overrides: Any) -> dict[str, Any]:
    return {"category": "runbook", "name": "rb", "url": "https://x", **overrides}


def service_level_objective(**overrides: Any) -> dict[str, Any]:
    return {"name": "slo", "type": "metric", **overrides}


def slo_threshold(**overrides: Any) -> dict[str, Any]:
    return {"timeframe": "7d", **overrides}


def dashboard(**overrides: Any) -> dict[str, Any]:
    return {"title": "t", "layout_type": "ordered", **overrides}


def widget(**overrides: Any) -> dict[str, Any]:
    return {"definition": {}, **overrides}


def metric_custom_aggregation(**overrides: Any) -> dict[str, Any]:
    return {"space": "avg", "time": "avg", **overrides}


def incident_response_data(**overrides: Any) -> dict[str, Any]:
    return {"id": "inc-1", "type": "incidents", **overrides}

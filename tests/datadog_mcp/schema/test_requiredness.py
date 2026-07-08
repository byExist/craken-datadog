"""Requiredness contract for models whose spec-required fields we honor.

Locks two things: the required fields reject a payload that omits them, and the
span models still parse when the API drops Go zero-values (parentID, error, …) —
the omitempty mismatch that kept those fields optional despite the spec.
"""

from collections.abc import Callable
from typing import Any

import payloads
import pytest
from pydantic import ValidationError

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.dashboards import Dashboard, Widget
from datadog_mcp.schema.incidents import IncidentResponseData
from datadog_mcp.schema.metrics import MetricCustomAggregation
from datadog_mcp.schema.monitors import Monitor, MonitorAsset
from datadog_mcp.schema.slo import ServiceLevelObjective
from datadog_mcp.schema.traces import APMTraceSpan, SummarizedSpan

CASES: list[
    tuple[type[DatadogModel], Callable[..., dict[str, Any]], tuple[str, ...]]
] = [
    (
        APMTraceSpan,
        payloads.apm_trace_span,
        (
            "service",
            "name",
            "resource",
            "spanID",
            "traceID",
            "traceIDFull",
            "startTime",
            "endTime",
            "type",
        ),
    ),
    (
        SummarizedSpan,
        payloads.summarized_span,
        (
            "service",
            "name",
            "resource",
            "spanID",
            "startTime",
            "endTime",
            "durationSeconds",
        ),
    ),
    (Monitor, payloads.monitor, ("type", "query")),
    (MonitorAsset, payloads.monitor_asset, ("category", "name", "url")),
    (ServiceLevelObjective, payloads.service_level_objective, ("name", "type")),
    (Dashboard, payloads.dashboard, ("title", "layout_type")),
    (MetricCustomAggregation, payloads.metric_custom_aggregation, ("space", "time")),
    (Widget, payloads.widget, ("definition",)),
    (IncidentResponseData, payloads.incident_response_data, ("id", "type")),
]


@pytest.mark.parametrize(
    ("model", "build", "required"), CASES, ids=[c[0].__name__ for c in CASES]
)
def test_required_fields(
    model: type[DatadogModel],
    build: Callable[..., dict[str, Any]],
    required: tuple[str, ...],
):
    model.model_validate(build())  # minimal payload parses
    for key in required:
        payload = build()
        del payload[key]
        with pytest.raises(ValidationError):
            model.model_validate(payload)


def test_spans_parse_without_omitempty_dropped_fields():
    """The API omits Go zero-values; those fields must stay optional."""
    span = APMTraceSpan.model_validate(payloads.apm_trace_span())
    assert span.parent_id is None  # 0 on a trace root
    assert span.error is None  # 0 when no error
    assert span.meta is None and span.metrics is None  # empty maps

    root = SummarizedSpan.model_validate(payloads.summarized_span())
    assert root.parent_id is None
    assert root.span_kind is None
    assert root.children is None  # dropped on leaves

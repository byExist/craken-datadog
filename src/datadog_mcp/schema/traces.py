"""Datadog v2 APM Trace schemas (get trace / pruned trace by ID).

A trace is the assembled view of one request, distinct from the searchable
``Span`` resource (see ``spans``): ``TraceResponse`` carries every span as a flat
list, while ``PrunedTraceResponse`` is a size-reduced hierarchical tree.
"""

from typing import Any

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type APMSpanErrorFlag = int


class APMTraceSpan(DatadogModel):
    # Spec marks 14 fields required; the API drops these as Go zero-values, so they
    # stay optional: parentID (0 on root), error (0 = no error), meta/metrics (empty),
    # duration (0). The rest are always present with non-zero values.
    duration: int | None = None
    end_time: int = Field(alias="endTime")
    error: APMSpanErrorFlag | None = None
    meta: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    name: str
    parent_id: int | None = Field(default=None, alias="parentID")
    resource: str
    resource_hash: str | None = Field(default=None, alias="resourceHash")
    restricted: bool | None = None
    self_time: float | None = None
    service: str
    span_id: int = Field(alias="spanID")
    start_time: int = Field(alias="startTime")
    trace_id: int = Field(alias="traceID")
    trace_id_full: str = Field(alias="traceIDFull")
    type: str


type APMTraceSpans = list[APMTraceSpan]


class SummarizedSpan(DatadogModel):
    # Same story as APMTraceSpan: these stay optional because the API omits them for
    # some spans — parentID (root), error, meta/metrics, span_kind,
    # hidden_child_spans_count, children (leaves) — observed across live traces.
    children: list["SummarizedSpan"] | None = None
    duration_seconds: float = Field(alias="durationSeconds")
    end_time: str = Field(alias="endTime")
    error: APMSpanErrorFlag | None = None
    hidden_child_spans_count: int | None = None
    meta: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    name: str
    parent_id: int | None = Field(default=None, alias="parentID")
    resource: str
    service: str
    span_id: int = Field(alias="spanID")
    span_kind: str | None = None
    start_time: str = Field(alias="startTime")


class SummarizedTrace(DatadogModel):
    root: SummarizedSpan
    trace_id: str = Field(alias="traceId")


class TraceAttributes(DatadogModel):
    is_truncated: bool | None = None
    spans: APMTraceSpans


class PrunedTraceAttributes(DatadogModel):
    is_truncated: bool | None = None
    size_bytes: int | None = None
    summarized_trace: SummarizedTrace


type TraceData = JSONAPIResource[TraceAttributes]
type PrunedTraceData = JSONAPIResource[PrunedTraceAttributes]


class TraceResponse(DatadogModel):
    data: TraceData


class PrunedTraceResponse(DatadogModel):
    data: PrunedTraceData

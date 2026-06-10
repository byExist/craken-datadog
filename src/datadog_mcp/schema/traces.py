"""Datadog v2 APM Trace schemas (get trace / pruned trace by ID).

A trace is the assembled view of one request, distinct from the searchable
``Span`` resource (see ``spans``): ``TraceResponse`` carries every span as a flat
list, while ``PrunedTraceResponse`` is a size-reduced hierarchical tree.
"""

from typing import Any, Literal

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type APMSpanErrorFlag = Literal[0, 1]


class APMTraceSpan(DatadogModel):
    duration: int | None = None
    end_time: int | None = Field(default=None, alias="endTime")
    error: APMSpanErrorFlag | None = None
    meta: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    name: str | None = None
    parent_id: int | None = Field(default=None, alias="parentID")
    resource: str | None = None
    resource_hash: str | None = Field(default=None, alias="resourceHash")
    restricted: bool | None = None
    self_time: float | None = None
    service: str | None = None
    span_id: int | None = Field(default=None, alias="spanID")
    start_time: int | None = Field(default=None, alias="startTime")
    trace_id: int | None = Field(default=None, alias="traceID")
    trace_id_full: str | None = Field(default=None, alias="traceIDFull")
    type: str | None = None


type APMTraceSpans = list[APMTraceSpan]


class SummarizedSpan(DatadogModel):
    children: list["SummarizedSpan"] | None = None
    duration_seconds: float | None = Field(default=None, alias="durationSeconds")
    end_time: str | None = Field(default=None, alias="endTime")
    error: APMSpanErrorFlag | None = None
    hidden_child_spans_count: int | None = None
    meta: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    name: str | None = None
    parent_id: int | None = Field(default=None, alias="parentID")
    resource: str | None = None
    service: str | None = None
    span_id: int | None = Field(default=None, alias="spanID")
    span_kind: str | None = None
    start_time: str | None = Field(default=None, alias="startTime")


class SummarizedTrace(DatadogModel):
    root: SummarizedSpan | None = None
    trace_id: str | None = Field(default=None, alias="traceId")


class TraceAttributes(DatadogModel):
    is_truncated: bool | None = None
    spans: APMTraceSpans | None = None


class PrunedTraceAttributes(DatadogModel):
    is_truncated: bool | None = None
    size_bytes: int | None = None
    summarized_trace: SummarizedTrace | None = None


type TraceData = JSONAPIResource[TraceAttributes]
type PrunedTraceData = JSONAPIResource[PrunedTraceAttributes]


class TraceResponse(DatadogModel):
    data: TraceData | None = None


class PrunedTraceResponse(DatadogModel):
    data: PrunedTraceData | None = None

"""Datadog v2 APM span schemas (Spans search / aggregate, Spans Metrics, service list).

APM traces fetched by ID live in ``traces``; this module covers the searchable
``Span`` resource and its aggregation.
"""

from typing import Any

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type SpansAggregateResponseStatus = str
type SpansMetricComputeAggregationType = str


class SpansWarning(DatadogModel):
    code: str | None = None
    detail: str | None = None
    title: str | None = None


class SpansListResponseLinks(DatadogModel):
    next: str | None = None


class SpansResponseMetadataPage(DatadogModel):
    after: str | None = None


class SpansAttributes(DatadogModel):
    attributes: dict[str, Any] | None = None
    custom: dict[str, Any] | None = None
    end_timestamp: str | None = None
    env: str | None = None
    host: str | None = None
    ingestion_reason: str | None = None
    parent_id: str | None = None
    resource_hash: str | None = None
    resource_name: str | None = None
    retained_by: str | None = None
    service: str | None = None
    single_span: bool | None = None
    span_id: str | None = None
    start_timestamp: str | None = None
    tags: list[str] | None = None
    trace_id: str | None = None
    type: str | None = None


class SpansAggregateBucketValueTimeseriesPoint(DatadogModel):
    time: str | None = None
    value: float | None = None


type SpansAggregateBucketValueTimeseries = list[
    SpansAggregateBucketValueTimeseriesPoint
]
type SpansAggregateBucketValue = str | float | SpansAggregateBucketValueTimeseries


class SpansAggregateBucketAttributes(DatadogModel):
    by: dict[str, Any] | None = None
    compute: dict[str, Any] | None = None
    computes: dict[str, SpansAggregateBucketValue] | None = None


class SpansAggregateResponseMetadata(DatadogModel):
    elapsed: int | None = None
    request_id: str | None = None
    status: SpansAggregateResponseStatus | None = None
    warnings: list[SpansWarning] | None = None


class SpansListResponseMetadata(DatadogModel):
    elapsed: int | None = None
    page: SpansResponseMetadataPage | None = None
    request_id: str | None = None
    status: SpansAggregateResponseStatus | None = None
    warnings: list[SpansWarning] | None = None


class SpansMetricResponseFilter(DatadogModel):
    query: str | None = None


class SpansMetricResponseGroupBy(DatadogModel):
    path: str | None = None
    tag_name: str | None = None


class SpansMetricResponseCompute(DatadogModel):
    aggregation_type: SpansMetricComputeAggregationType | None = None
    include_percentiles: bool | None = None
    path: str | None = None


class SpansMetricResponseAttributes(DatadogModel):
    compute: SpansMetricResponseCompute | None = None
    filter: SpansMetricResponseFilter | None = None
    group_by: list[SpansMetricResponseGroupBy] | None = None


class ServiceListDataAttributesMetadataItems(DatadogModel):
    is_traced: bool | None = Field(default=None, alias="isTraced")
    is_usm: bool | None = Field(default=None, alias="isUsm")


class ServiceListDataAttributes(DatadogModel):
    metadata: list[ServiceListDataAttributesMetadataItems] | None = None
    services: list[str] | None = None


type Span = JSONAPIResource[SpansAttributes]
type SpansAggregateBucket = JSONAPIResource[SpansAggregateBucketAttributes]
type SpansMetricResponseData = JSONAPIResource[SpansMetricResponseAttributes]
type ServiceListData = JSONAPIResource[ServiceListDataAttributes]


class SpansListResponse(DatadogModel):
    data: list[Span] | None = None
    links: SpansListResponseLinks | None = None
    meta: SpansListResponseMetadata | None = None


class SpansAggregateResponse(DatadogModel):
    data: list[SpansAggregateBucket] | None = None
    meta: SpansAggregateResponseMetadata | None = None


class SpansMetricsResponse(DatadogModel):
    data: list[SpansMetricResponseData] | None = None


class ServiceList(DatadogModel):
    data: ServiceListData | None = None

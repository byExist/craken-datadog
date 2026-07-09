"""Datadog v2 RUM (Real User Monitoring) event schemas.

Structurally a sibling of ``logs``: a searchable event resource with a flat
search/aggregate request and a JSON:API event payload, here for browser and
mobile telemetry (sessions, views, errors, actions, resources).
"""

from typing import Any

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type RUMResponseStatus = str


class RUMEventAttributes(DatadogModel):
    attributes: dict[str, Any] | None = None
    service: str | None = None
    tags: list[str] | None = None
    timestamp: str | None = None


type RUMEvent = JSONAPIResource[RUMEventAttributes]


class RUMWarning(DatadogModel):
    code: str | None = None
    detail: str | None = None
    title: str | None = None


class RUMResponsePage(DatadogModel):
    after: str | None = None


class RUMResponseMetadata(DatadogModel):
    elapsed: int | None = None
    page: RUMResponsePage | None = None
    request_id: str | None = None
    status: RUMResponseStatus | None = None
    warnings: list[RUMWarning] | None = None


class RUMResponseLinks(DatadogModel):
    next: str | None = None


class RUMEventsResponse(DatadogModel):
    data: list[RUMEvent] | None = None
    links: RUMResponseLinks | None = None
    meta: RUMResponseMetadata | None = None


class RUMAggregateBucketValueTimeseriesPoint(DatadogModel):
    time: str | None = None
    value: float | None = None


type RUMAggregateBucketValueTimeseries = list[RUMAggregateBucketValueTimeseriesPoint]
type RUMAggregateBucketValue = str | float | RUMAggregateBucketValueTimeseries


class RUMBucketResponse(DatadogModel):
    by: dict[str, Any] | None = None
    computes: dict[str, RUMAggregateBucketValue] | None = None


class RUMAggregationBucketsResponse(DatadogModel):
    buckets: list[RUMBucketResponse] | None = None


class RUMAnalyticsAggregateResponse(DatadogModel):
    data: RUMAggregationBucketsResponse | None = None
    links: RUMResponseLinks | None = None
    meta: RUMResponseMetadata | None = None

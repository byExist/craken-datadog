"""Datadog log schemas — v2 Logs API events and v1 index configuration."""

from datetime import datetime
from typing import Any, Literal

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type LogsAggregateResponseStatus = Literal["done", "timeout"]


class LogAttributes(DatadogModel):
    attributes: dict[str, Any] | None = None
    host: str | None = None
    message: str | None = None
    service: str | None = None
    status: str | None = None
    tags: list[str] | None = None
    timestamp: datetime | None = None


type Log = JSONAPIResource[LogAttributes]


class LogsWarning(DatadogModel):
    code: str | None = None
    detail: str | None = None
    title: str | None = None


class LogsResponseMetadataPage(DatadogModel):
    after: str | None = None


class LogsResponseMetadata(DatadogModel):
    elapsed: int | None = None
    page: LogsResponseMetadataPage | None = None
    request_id: str | None = None
    status: LogsAggregateResponseStatus | None = None
    warnings: list[LogsWarning] | None = None


class LogsListResponseLinks(DatadogModel):
    next: str | None = None


class LogsListResponse(DatadogModel):
    data: list[Log] | None = None
    links: LogsListResponseLinks | None = None
    meta: LogsResponseMetadata | None = None


class LogsAggregateBucketValueTimeseriesPoint(DatadogModel):
    time: str | None = None
    value: float | None = None


type LogsAggregateBucketValueTimeseries = list[LogsAggregateBucketValueTimeseriesPoint]
type LogsAggregateBucketValue = str | float | LogsAggregateBucketValueTimeseries


class LogsAggregateBucket(DatadogModel):
    by: dict[str, Any] | None = None
    computes: dict[str, LogsAggregateBucketValue] | None = None


class LogsAggregateResponseData(DatadogModel):
    buckets: list[LogsAggregateBucket] | None = None


class LogsAggregateResponse(DatadogModel):
    data: LogsAggregateResponseData | None = None
    meta: LogsResponseMetadata | None = None


class LogsFilter(DatadogModel):
    query: str | None = None


class LogsExclusionFilter(DatadogModel):
    query: str | None = None
    sample_attribute: str | None = None
    sample_rate: float | None = None


class LogsExclusion(DatadogModel):
    name: str | None = None
    is_enabled: bool | None = None
    filter: LogsExclusionFilter | None = None


class LogsDailyLimitReset(DatadogModel):
    reset_time: str | None = None
    reset_utc_offset: str | None = None


class LogsIndex(DatadogModel):
    name: str | None = None
    filter: LogsFilter | None = None
    exclusion_filters: list[LogsExclusion] | None = None
    num_retention_days: int | None = None
    num_flex_logs_retention_days: int | None = None
    daily_limit: int | None = None
    daily_limit_reset: LogsDailyLimitReset | None = None
    daily_limit_warning_threshold_percentage: float | None = None
    is_rate_limited: bool | None = None
    tags: list[str] | None = None


class LogsIndexListResponse(DatadogModel):
    indexes: list[LogsIndex] | None = None

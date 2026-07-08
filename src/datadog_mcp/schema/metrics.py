"""Datadog v2 metric schemas — query core (Metrics API).

Scoped to the query/read path: timeseries & scalar formula queries, metric listing,
tag configuration, and tags. Metric-management surface (indexing rules, bulk tag
config, volumes, assets, cardinalities, suggested tags, estimates; ~71 schemas) is
deferred until those tools are exposed.
"""

from typing import Literal

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type MetricCustomSpaceAggregation = Literal["avg", "max", "min", "sum"]
type MetricCustomTimeAggregation = Literal["avg", "count", "max", "min", "sum"]
type MetricMetaPageType = Literal["cursor_limit"]
type MetricTagConfigurationMetricTypes = Literal[
    "gauge", "count", "rate", "distribution"
]
type ScalarColumnTypeGroup = Literal["group"]
type ScalarColumnTypeNumber = Literal["number"]
type ScalarFormulaResponseType = Literal["scalar_response"]
type TimeseriesFormulaResponseType = Literal["timeseries_response"]

type GroupTags = list[str]
type TimeseriesResponseTimes = list[int]
type TimeseriesResponseValues = list[float]


class Unit(DatadogModel):
    family: str | None = None
    name: str | None = None
    plural: str | None = None
    scale_factor: float | None = None
    short_name: str | None = None


class MetricAllTagsAttributes(DatadogModel):
    ingested_tags: list[str] | None = None
    tags: list[str] | None = None


class MetricCustomAggregation(DatadogModel):
    space: MetricCustomSpaceAggregation
    time: MetricCustomTimeAggregation


class MetricMetaPage(DatadogModel):
    cursor: str | None = None
    limit: int | None = None
    next_cursor: str | None = None
    type: MetricMetaPageType | None = None


class Metric(DatadogModel):
    id: str | None = None
    type: str | None = None


class MetricsListResponseLinks(DatadogModel):
    first: str | None = None
    last: str | None = None
    next: str | None = None
    prev: str | None = None
    self_: str | None = Field(default=None, alias="self")


type MetricCustomAggregations = list[MetricCustomAggregation]
type TimeseriesResponseValuesList = list[TimeseriesResponseValues]


class MetricTagConfigurationAttributes(DatadogModel):
    aggregations: MetricCustomAggregations | None = None
    created_at: str | None = None
    exclude_tags_mode: bool | None = None
    include_percentiles: bool | None = None
    metric_type: MetricTagConfigurationMetricTypes | None = None
    modified_at: str | None = None
    tags: list[str] | None = None


class MetricPaginationMeta(DatadogModel):
    pagination: MetricMetaPage | None = None


class ScalarMeta(DatadogModel):
    unit: list[Unit | None] | None = None


class DataScalarColumn(DatadogModel):
    meta: ScalarMeta | None = None
    name: str | None = None
    type: ScalarColumnTypeNumber | None = None
    values: list[float] | None = None


class GroupScalarColumn(DatadogModel):
    name: str | None = None
    type: ScalarColumnTypeGroup | None = None
    values: list[list[str]] | None = None


type ScalarColumn = GroupScalarColumn | DataScalarColumn


class ScalarFormulaResponseAtrributes(DatadogModel):
    columns: list[ScalarColumn] | None = None


class ScalarResponse(DatadogModel):
    attributes: ScalarFormulaResponseAtrributes | None = None
    type: ScalarFormulaResponseType | None = None


class ScalarFormulaQueryResponse(DatadogModel):
    data: ScalarResponse | None = None
    errors: str | None = None


class TimeseriesResponseSeries(DatadogModel):
    group_tags: GroupTags | None = None
    query_index: int | None = None
    unit: list[Unit | None] | None = None


type TimeseriesResponseSeriesList = list[TimeseriesResponseSeries]


class TimeseriesResponseAttributes(DatadogModel):
    series: TimeseriesResponseSeriesList | None = None
    times: TimeseriesResponseTimes | None = None
    values: TimeseriesResponseValuesList | None = None


class TimeseriesResponse(DatadogModel):
    attributes: TimeseriesResponseAttributes | None = None
    type: TimeseriesFormulaResponseType | None = None


class TimeseriesFormulaQueryResponse(DatadogModel):
    data: TimeseriesResponse | None = None
    errors: str | None = None


type MetricAllTags = JSONAPIResource[MetricAllTagsAttributes]
type MetricTagConfiguration = JSONAPIResource[MetricTagConfigurationAttributes]


class MetricAllTagsResponse(DatadogModel):
    data: MetricAllTags | None = None


class MetricTagConfigurationResponse(DatadogModel):
    data: MetricTagConfiguration | None = None


type MetricsAndMetricTagConfigurations = Metric | MetricTagConfiguration


class MetricsAndMetricTagConfigurationsResponse(DatadogModel):
    data: list[MetricsAndMetricTagConfigurations] | None = None
    links: MetricsListResponseLinks | None = None
    meta: MetricPaginationMeta | None = None

"""Datadog v1/v2 SLO schemas — config + status core (Service Level Objectives).

Scoped to reading SLO definitions (get/list) and v2 SLO status. History, search,
corrections, bulk-delete, and report endpoints are deferred to their own tools.
"""

from typing import Literal

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type FormulaAndFunctionMetricAggregation = Literal[
    "avg", "min", "max", "sum", "last", "area"
]
type FormulaAndFunctionMetricDataSource = Literal["metrics"]
type FormulaAndFunctionMetricSemanticMode = Literal["combined", "native"]
type SLOTimeSliceComparator = Literal[">", ">=", "<", "<="]
type SLOTimeSliceInterval = Literal[60, 300]
type SLOTimeframe = Literal["7d", "30d", "90d", "custom"]
type SLOType = Literal["metric", "monitor", "time_slice"]

type CrossOrgUuids = list[str]


class Creator(DatadogModel):
    email: str | None = None
    handle: str | None = None
    name: str | None = None


class SLOFormula(DatadogModel):
    formula: str | None = None


class ServiceLevelObjectiveQuery(DatadogModel):
    denominator: str
    numerator: str


class SLOThreshold(DatadogModel):
    target: float | None = None
    target_display: str | None = None
    timeframe: SLOTimeframe
    warning: float | None = None
    warning_display: str | None = None


class FormulaAndFunctionMetricQueryDefinition(DatadogModel):
    aggregator: FormulaAndFunctionMetricAggregation | None = None
    cross_org_uuids: CrossOrgUuids | None = None
    data_source: FormulaAndFunctionMetricDataSource | None = None
    name: str | None = None
    query: str | None = None
    semantic_mode: FormulaAndFunctionMetricSemanticMode | None = None


type SLODataSourceQueryDefinition = FormulaAndFunctionMetricQueryDefinition


class SLOCountDefinitionWithBadEventsFormula(DatadogModel):
    bad_events_formula: SLOFormula | None = None
    good_events_formula: SLOFormula | None = None
    queries: list[SLODataSourceQueryDefinition] | None = None


class SLOCountDefinitionWithTotalEventsFormula(DatadogModel):
    good_events_formula: SLOFormula | None = None
    queries: list[SLODataSourceQueryDefinition] | None = None
    total_events_formula: SLOFormula | None = None


type SLOCountDefinition = (
    SLOCountDefinitionWithTotalEventsFormula | SLOCountDefinitionWithBadEventsFormula
)


class SLOCountSpec(DatadogModel):
    count: SLOCountDefinition | None = None


class SLOTimeSliceQuery(DatadogModel):
    formulas: list[SLOFormula] | None = None
    queries: list[SLODataSourceQueryDefinition] | None = None


class SLOTimeSliceCondition(DatadogModel):
    comparator: SLOTimeSliceComparator | None = None
    query: SLOTimeSliceQuery | None = None
    query_interval_seconds: SLOTimeSliceInterval | None = None
    threshold: float | None = None


class SLOTimeSliceSpec(DatadogModel):
    time_slice: SLOTimeSliceCondition | None = None


type SLOSliSpec = SLOTimeSliceSpec | SLOCountSpec


class ServiceLevelObjective(DatadogModel):
    created_at: int | None = None
    creator: Creator | None = None
    description: str | None = None
    groups: list[str] | None = None
    id: str | None = None
    modified_at: int | None = None
    monitor_ids: list[int] | None = None
    monitor_tags: list[str] | None = None
    name: str
    query: ServiceLevelObjectiveQuery | None = None
    sli_specification: SLOSliSpec | None = None
    tags: list[str] | None = None
    target_threshold: float | None = None
    thresholds: list[SLOThreshold] | None = None
    timeframe: SLOTimeframe | None = None
    type: SLOType
    warning_threshold: float | None = None


class SLOResponseData(DatadogModel):
    configured_alert_ids: list[int] | None = None
    created_at: int | None = None
    creator: Creator | None = None
    description: str | None = None
    groups: list[str] | None = None
    id: str | None = None
    modified_at: int | None = None
    monitor_ids: list[int] | None = None
    monitor_tags: list[str] | None = None
    name: str
    query: ServiceLevelObjectiveQuery | None = None
    sli_specification: SLOSliSpec | None = None
    tags: list[str] | None = None
    target_threshold: float | None = None
    thresholds: list[SLOThreshold] | None = None
    timeframe: SLOTimeframe | None = None
    type: SLOType
    warning_threshold: float | None = None


class SLOResponse(DatadogModel):
    data: SLOResponseData | None = None
    errors: list[str] | None = None


class SLOListResponseMetadataPage(DatadogModel):
    total_count: int | None = None
    total_filtered_count: int | None = None


class SLOListResponseMetadata(DatadogModel):
    page: SLOListResponseMetadataPage | None = None


class SLOListResponse(DatadogModel):
    data: list[ServiceLevelObjective] | None = None
    errors: list[str] | None = None
    metadata: SLOListResponseMetadata | None = None


class RawErrorBudgetRemaining(DatadogModel):
    unit: str | None = None
    value: float | None = None


class SloStatusDataAttributes(DatadogModel):
    error_budget_remaining: float | None = None
    raw_error_budget_remaining: RawErrorBudgetRemaining | None = None
    sli: float | None = None
    span_precision: int | None = None
    state: str | None = None


type SloStatusData = JSONAPIResource[SloStatusDataAttributes]


class SloStatusResponse(DatadogModel):
    data: SloStatusData

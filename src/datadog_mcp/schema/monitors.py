"""Datadog v1 monitor schemas (Monitors API).

Formula/function query-definition variants (MonitorFormulaAndFunction*, 33 schemas)
are left loose as ``list[dict]`` on ``MonitorOptions.variables`` — a deep, rarely
needed query-definition zoo.
"""

from typing import Any, Literal

from datadog_mcp.schema.base import DatadogModel

type MonitorAssetCategory = Literal["runbook"]
type MonitorAssetResourceType = Literal["notebook"]
type MonitorDeviceID = Literal[
    "laptop_large",
    "tablet",
    "mobile_small",
    "chrome.laptop_large",
    "chrome.tablet",
    "chrome.mobile_small",
    "firefox.laptop_large",
]
type MonitorDraftStatus = Literal["draft", "published"]
type MonitorOptionsNotificationPresets = Literal[
    "show_all",
    "hide_query",
    "hide_handles",
    "hide_all",
    "hide_query_and_handles",
    "show_only_snapshot",
    "hide_handles_and_footer",
]
type MonitorOverallStates = Literal[
    "Alert", "Ignored", "No Data", "OK", "Skipped", "Unknown", "Warn"
]
type MonitorRenotifyStatusType = Literal["alert", "warn", "no data"]
type MonitorType = Literal[
    "composite",
    "event alert",
    "log alert",
    "metric alert",
    "process alert",
    "query alert",
    "rum alert",
]
type OnMissingDataOption = Literal[
    "default", "show_no_data", "show_and_notify_no_data", "resolve"
]
type QuerySortOrder = Literal["asc", "desc"]


class Creator(DatadogModel):
    email: str | None = None
    handle: str | None = None
    name: str | None = None


class DeletedMonitor(DatadogModel):
    deleted_monitor_id: int | None = None


class MatchingDowntime(DatadogModel):
    end: int | None = None
    id: int
    scope: list[str] | None = None
    start: int | None = None


class MonitorAsset(DatadogModel):
    category: MonitorAssetCategory
    name: str
    resource_key: str | None = None
    resource_type: MonitorAssetResourceType | None = None
    url: str


class MonitorSearchResultNotification(DatadogModel):
    handle: str | None = None
    name: str | None = None


class MonitorThresholdWindowOptions(DatadogModel):
    recovery_window: str | None = None
    trigger_window: str | None = None


class MonitorThresholds(DatadogModel):
    critical: float | None = None
    critical_query: str | None = None
    critical_recovery: float | None = None
    critical_recovery_query: str | None = None
    ok: float | None = None
    unknown: float | None = None
    warning: float | None = None
    warning_recovery: float | None = None


class MonitorStateGroup(DatadogModel):
    last_nodata_ts: int | None = None
    last_notified_ts: int | None = None
    last_resolved_ts: int | None = None
    last_triggered_ts: int | None = None
    name: str | None = None
    status: MonitorOverallStates | None = None


class MonitorOptionsAggregation(DatadogModel):
    group_by: str | None = None
    metric: str | None = None
    type: str | None = None


class MonitorOptionsCustomScheduleRecurrence(DatadogModel):
    rrule: str | None = None
    start: str | None = None
    timezone: str | None = None


class MonitorOptionsSchedulingOptionsEvaluationWindow(DatadogModel):
    day_starts: str | None = None
    hour_starts: int | None = None
    month_starts: int | None = None
    timezone: str | None = None


class MonitorSearchResponseMetadata(DatadogModel):
    page: int | None = None
    page_count: int | None = None
    per_page: int | None = None
    total_count: int | None = None


class MonitorSearchCountItem(DatadogModel):
    count: int | None = None
    name: Any | None = None


type MonitorSearchCount = list[MonitorSearchCountItem]


class CheckCanDeleteMonitorResponseData(DatadogModel):
    ok: list[int] | None = None


class MonitorOptionsCustomSchedule(DatadogModel):
    recurrences: list[MonitorOptionsCustomScheduleRecurrence] | None = None


class MonitorOptionsSchedulingOptions(DatadogModel):
    custom_schedule: MonitorOptionsCustomSchedule | None = None
    evaluation_window: MonitorOptionsSchedulingOptionsEvaluationWindow | None = None


class MonitorState(DatadogModel):
    groups: dict[str, MonitorStateGroup] | None = None


class MonitorOptions(DatadogModel):
    aggregation: MonitorOptionsAggregation | None = None
    device_ids: list[MonitorDeviceID] | None = None
    enable_logs_sample: bool | None = None
    enable_samples: bool | None = None
    escalation_message: str | None = None
    evaluation_delay: int | None = None
    group_retention_duration: str | None = None
    groupby_simple_monitor: bool | None = None
    include_tags: bool | None = None
    locked: bool | None = None
    min_failure_duration: int | None = None
    min_location_failed: int | None = None
    new_group_delay: int | None = None
    new_host_delay: int | None = None
    no_data_timeframe: int | None = None
    notification_preset_name: MonitorOptionsNotificationPresets | None = None
    notify_audit: bool | None = None
    notify_by: list[str] | None = None
    notify_no_data: bool | None = None
    on_missing_data: OnMissingDataOption | None = None
    renotify_interval: int | None = None
    renotify_occurrences: int | None = None
    renotify_statuses: list[MonitorRenotifyStatusType] | None = None
    require_full_window: bool | None = None
    scheduling_options: MonitorOptionsSchedulingOptions | None = None
    silenced: dict[str, Any] | None = None
    synthetics_check_id: str | None = None
    threshold_windows: MonitorThresholdWindowOptions | None = None
    thresholds: MonitorThresholds | None = None
    timeout_h: int | None = None
    variables: list[dict[str, Any]] | None = None


class MonitorGroupSearchResult(DatadogModel):
    group: str | None = None
    group_tags: list[str] | None = None
    last_nodata_ts: int | None = None
    last_triggered_ts: int | None = None
    monitor_id: int | None = None
    monitor_name: str | None = None
    status: MonitorOverallStates | None = None


class MonitorGroupSearchResponseCounts(DatadogModel):
    status: MonitorSearchCount | None = None
    type: MonitorSearchCount | None = None


class MonitorGroupSearchResponse(DatadogModel):
    counts: MonitorGroupSearchResponseCounts | None = None
    groups: list[MonitorGroupSearchResult] | None = None
    metadata: MonitorSearchResponseMetadata | None = None


class MonitorSearchResult(DatadogModel):
    classification: str | None = None
    creator: Creator | None = None
    id: int | None = None
    last_triggered_ts: int | None = None
    metrics: list[str] | None = None
    name: str | None = None
    notifications: list[MonitorSearchResultNotification] | None = None
    org_id: int | None = None
    quality_issues: list[str] | None = None
    query: str | None = None
    scopes: list[str] | None = None
    status: MonitorOverallStates | None = None
    tags: list[str] | None = None
    type: MonitorType | None = None


class MonitorSearchResponseCounts(DatadogModel):
    muted: MonitorSearchCount | None = None
    status: MonitorSearchCount | None = None
    tag: MonitorSearchCount | None = None
    type: MonitorSearchCount | None = None


class MonitorSearchResponse(DatadogModel):
    counts: MonitorSearchResponseCounts | None = None
    metadata: MonitorSearchResponseMetadata | None = None
    monitors: list[MonitorSearchResult] | None = None


class CheckCanDeleteMonitorResponse(DatadogModel):
    data: CheckCanDeleteMonitorResponseData
    errors: dict[str, Any] | None = None


class Monitor(DatadogModel):
    assets: list[MonitorAsset] | None = None
    created: str | None = None
    creator: Creator | None = None
    deleted: str | None = None
    draft_status: MonitorDraftStatus | None = None
    id: int | None = None
    matching_downtimes: list[MatchingDowntime] | None = None
    message: str | None = None
    modified: str | None = None
    multi: bool | None = None
    name: str | None = None
    options: MonitorOptions | None = None
    overall_state: MonitorOverallStates | None = None
    priority: int | None = None
    query: str
    restricted_roles: list[str] | None = None
    state: MonitorState | None = None
    tags: list[str] | None = None
    type: MonitorType

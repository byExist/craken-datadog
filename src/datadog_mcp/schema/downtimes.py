"""Datadog v2 downtime schemas (Downtimes API).

JSON:API ``relationships`` and ``included`` (the shared user/role/org sideload graph)
are left loose as ``dict`` / ``list[dict]`` — linkage data is preserved for reading
without modeling the cross-domain relationship zoo.
"""

from typing import Any, Literal

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type DowntimeStatus = Literal["active", "canceled", "ended", "scheduled"]
type DowntimeNotifyEndStateActions = Literal["canceled", "expired"]
type DowntimeNotifyEndStateTypes = Literal["alert", "no data", "warn"]

type DowntimeNotifyEndStates = list[DowntimeNotifyEndStateTypes]
type DowntimeNotifyEndTypes = list[DowntimeNotifyEndStateActions]


class DowntimeMonitorIdentifierId(DatadogModel):
    monitor_id: int | None = None


class DowntimeMonitorIdentifierTags(DatadogModel):
    monitor_tags: list[str] | None = None


type DowntimeMonitorIdentifier = (
    DowntimeMonitorIdentifierId | DowntimeMonitorIdentifierTags
)


class DowntimeScheduleCurrentDowntimeResponse(DatadogModel):
    end: str | None = None
    start: str | None = None


class DowntimeScheduleOneTimeResponse(DatadogModel):
    end: str | None = None
    start: str | None = None


class DowntimeScheduleRecurrenceResponse(DatadogModel):
    duration: str | None = None
    rrule: str | None = None
    start: str | None = None


class DowntimeScheduleRecurrencesResponse(DatadogModel):
    current_downtime: DowntimeScheduleCurrentDowntimeResponse | None = None
    recurrences: list[DowntimeScheduleRecurrenceResponse] | None = None
    timezone: str | None = None


type DowntimeScheduleResponse = (
    DowntimeScheduleRecurrencesResponse | DowntimeScheduleOneTimeResponse
)


class DowntimeResponseAttributes(DatadogModel):
    canceled: str | None = None
    created: str | None = None
    display_timezone: str | None = None
    message: str | None = None
    modified: str | None = None
    monitor_identifier: DowntimeMonitorIdentifier | None = None
    mute_first_recovery_notification: bool | None = None
    notify_end_states: DowntimeNotifyEndStates | None = None
    notify_end_types: DowntimeNotifyEndTypes | None = None
    schedule: DowntimeScheduleResponse | None = None
    scope: str | None = None
    status: DowntimeStatus | None = None


class DowntimeResponseData(DatadogModel):
    id: str | None = None
    type: str | None = None
    attributes: DowntimeResponseAttributes | None = None
    relationships: dict[str, Any] | None = None


class DowntimeMetaPage(DatadogModel):
    total_filtered_count: int | None = None


class DowntimeMeta(DatadogModel):
    page: DowntimeMetaPage | None = None


class DowntimeResponse(DatadogModel):
    data: DowntimeResponseData | None = None
    included: list[dict[str, Any]] | None = None


class ListDowntimesResponse(DatadogModel):
    data: list[DowntimeResponseData] | None = None
    included: list[dict[str, Any]] | None = None
    meta: DowntimeMeta | None = None


class MonitorDowntimeMatchResponseAttributes(DatadogModel):
    end: str | None = None
    groups: list[str] | None = None
    scope: str | None = None
    start: str | None = None


type MonitorDowntimeMatchResponseData = JSONAPIResource[
    MonitorDowntimeMatchResponseAttributes
]


class MonitorDowntimeMatchResponse(DatadogModel):
    data: list[MonitorDowntimeMatchResponseData] | None = None
    meta: DowntimeMeta | None = None

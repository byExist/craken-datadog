"""Datadog v2 incident schemas (read: list / get / search).

Scoped to the incident object. Custom ``fields``, creator objects, JSON:API
``relationships``/``included``, and search ``facets`` are left loose as ``dict`` /
``list[dict]``. Sub-resources (attachments, impacts, integration metadata,
notification rules/templates, todos, types, user-defined fields, postmortems) are
deferred to their own tools.
"""

from typing import Any

from datadog_mcp.schema.base import DatadogModel

# str, not Literal: severity sets are org-customizable and vary from the spec.
type IncidentSeverity = str


class IncidentNotificationHandle(DatadogModel):
    display_name: str | None = None
    handle: str | None = None


class IncidentResponseAttributes(DatadogModel):
    archived: str | None = None
    case_id: int | None = None
    created: str | None = None
    customer_impact_duration: int | None = None
    customer_impact_end: str | None = None
    customer_impact_scope: str | None = None
    customer_impact_start: str | None = None
    customer_impacted: bool | None = None
    declared: str | None = None
    declared_by: dict[str, Any] | None = None
    declared_by_uuid: str | None = None
    detected: str | None = None
    fields: dict[str, Any] | None = None
    incident_type_uuid: str | None = None
    is_test: bool | None = None
    modified: str | None = None
    non_datadog_creator: dict[str, Any] | None = None
    notification_handles: list[IncidentNotificationHandle] | None = None
    public_id: int | None = None
    resolved: str | None = None
    severity: IncidentSeverity | None = None
    state: str | None = None
    time_to_detect: int | None = None
    time_to_internal_response: int | None = None
    time_to_repair: int | None = None
    time_to_resolve: int | None = None
    title: str
    visibility: str | None = None


class IncidentResponseData(DatadogModel):
    id: str
    type: str
    attributes: IncidentResponseAttributes | None = None
    relationships: dict[str, Any] | None = None


class IncidentResponseMetaPagination(DatadogModel):
    next_offset: int | None = None
    offset: int | None = None
    size: int | None = None


class IncidentResponseMeta(DatadogModel):
    pagination: IncidentResponseMetaPagination | None = None


class IncidentResponse(DatadogModel):
    data: IncidentResponseData
    included: list[dict[str, Any]] | None = None


class IncidentsResponse(DatadogModel):
    data: list[IncidentResponseData] | None = None
    included: list[dict[str, Any]] | None = None
    meta: IncidentResponseMeta | None = None


class IncidentSearchResponseIncidentsData(DatadogModel):
    data: IncidentResponseData


class IncidentSearchResponseAttributes(DatadogModel):
    facets: dict[str, Any] | None = None
    incidents: list[IncidentSearchResponseIncidentsData] | None = None
    total: int | None = None


class IncidentSearchResponseData(DatadogModel):
    attributes: IncidentSearchResponseAttributes | None = None
    type: str | None = None


class IncidentSearchResponseMeta(DatadogModel):
    pagination: IncidentResponseMetaPagination | None = None


class IncidentSearchResponse(DatadogModel):
    data: IncidentSearchResponseData
    included: list[dict[str, Any]] | None = None
    meta: IncidentSearchResponseMeta | None = None

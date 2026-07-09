"""Datadog v2 event schemas (Events API)."""

from typing import Any, Literal

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource

type AlertEventAttributesLinksItemCategory = Literal[
    "runbook", "documentation", "dashboard"
]
# str, not Literal: /api/v2/events emits values the vendored spec omits
# (numeric priorities, "no data" status), so a Literal rejects real payloads.
type AlertEventAttributesPriority = str
type AlertEventAttributesStatus = str
type ChangeEventAttributesAuthorType = Literal["user", "system", "api", "automation"]
type ChangeEventAttributesChangedResourceType = Literal["feature_flag", "configuration"]
type ChangeEventAttributesImpactedResourcesItemType = Literal["service"]
# str, not Literal — same spec/live mismatch as AlertEventAttributes* above.
type EventPriority = str
type EventStatusType = str
type EventSystemAttributesCategory = Literal["change", "alert"]
type EventSystemAttributesIntegrationId = Literal["custom-events"]


class AlertEventAttributesLinksItem(DatadogModel):
    category: AlertEventAttributesLinksItemCategory | None = None
    title: str | None = None
    url: str | None = None


class ChangeEventAttributesAuthor(DatadogModel):
    name: str | None = None
    type: ChangeEventAttributesAuthorType | None = None


class ChangeEventAttributesChangedResource(DatadogModel):
    name: str | None = None
    type: ChangeEventAttributesChangedResourceType | None = None


class ChangeEventAttributesImpactedResourcesItem(DatadogModel):
    name: str | None = None
    type: ChangeEventAttributesImpactedResourcesItemType | None = None


class Event(DatadogModel):
    id: str | None = None
    name: str | None = None
    source_id: int | None = None
    type: str | None = None


class EventSystemAttributes(DatadogModel):
    category: EventSystemAttributesCategory | None = None
    id: str | None = None
    integration_id: EventSystemAttributesIntegrationId | None = None
    source_id: int | None = None
    uid: str | None = None


class MonitorType(DatadogModel):
    created_at: int | None = None
    group_status: int | None = None
    groups: list[str] | None = None
    id: int | None = None
    message: str | None = None
    modified: int | None = None
    name: str | None = None
    query: str | None = None
    tags: list[str] | None = None
    templated_name: str | None = None
    type: str | None = None


class EventsWarning(DatadogModel):
    code: str | None = None
    detail: str | None = None
    title: str | None = None


class EventsResponseMetadataPage(DatadogModel):
    after: str | None = None


class EventsListResponseLinks(DatadogModel):
    next: str | None = None


class EventCreateResponsePayloadLinks(DatadogModel):
    self_: str | None = Field(default=None, alias="self")


class EventCreateResponseAttributesAttributesEvt(DatadogModel):
    id: str | None = None
    uid: str | None = None


class AlertEventAttributes(DatadogModel):
    aggregation_key: str | None = None
    custom: dict[str, Any] | None = None
    evt: EventSystemAttributes | None = None
    links: list[AlertEventAttributesLinksItem] | None = None
    priority: AlertEventAttributesPriority | None = None
    service: str | None = None
    status: AlertEventAttributesStatus | None = None
    timestamp: int | None = None
    title: str | None = None


class ChangeEventAttributes(DatadogModel):
    aggregation_key: str | None = None
    author: ChangeEventAttributesAuthor | None = None
    change_metadata: dict[str, Any] | None = None
    changed_resource: ChangeEventAttributesChangedResource | None = None
    evt: EventSystemAttributes | None = None
    impacted_resources: list[ChangeEventAttributesImpactedResourcesItem] | None = None
    new_value: dict[str, Any] | None = None
    prev_value: dict[str, Any] | None = None
    service: str | None = None
    timestamp: int | None = None
    title: str | None = None


class EventAttributes(DatadogModel):
    aggregation_key: str | None = None
    date_happened: int | None = None
    device_name: str | None = None
    duration: int | None = None
    event_object: str | None = None
    evt: Event | None = None
    hostname: str | None = None
    monitor: MonitorType | None = None
    monitor_groups: list[str] | None = None
    monitor_id: int | None = None
    priority: EventPriority | None = None
    related_event_id: int | None = None
    service: str | None = None
    source_type_name: str | None = None
    sourcecategory: str | None = None
    status: EventStatusType | None = None
    tags: list[str] | None = None
    timestamp: int | None = None
    title: str | None = None


class EventCreateResponseAttributesAttributes(DatadogModel):
    evt: EventCreateResponseAttributesAttributesEvt | None = None


class EventResponseAttributes(DatadogModel):
    attributes: EventAttributes | None = None
    message: str | None = None
    tags: list[str] | None = None
    timestamp: str | None = None


class EventsResponseMetadata(DatadogModel):
    elapsed: int | None = None
    page: EventsResponseMetadataPage | None = None
    request_id: str | None = None
    status: str | None = None
    warnings: list[EventsWarning] | None = None


type V2EventAttributesAttributes = ChangeEventAttributes | AlertEventAttributes


class V2EventAttributes(DatadogModel):
    attributes: V2EventAttributesAttributes | None = None
    message: str | None = None
    tags: list[str] | None = None
    timestamp: str | None = None


class EventCreateResponseAttributes(DatadogModel):
    attributes: EventCreateResponseAttributesAttributes | None = None


type EventResponse = JSONAPIResource[EventResponseAttributes]
type V2Event = JSONAPIResource[V2EventAttributes]


class EventsListResponse(DatadogModel):
    data: list[EventResponse] | None = None
    links: EventsListResponseLinks | None = None
    meta: EventsResponseMetadata | None = None


class EventCreateResponse(DatadogModel):
    attributes: EventCreateResponseAttributes | None = None
    type: str | None = None


class EventCreateResponsePayload(DatadogModel):
    data: EventCreateResponse | None = None
    links: EventCreateResponsePayloadLinks | None = None


class V2EventResponse(DatadogModel):
    data: V2Event | None = None

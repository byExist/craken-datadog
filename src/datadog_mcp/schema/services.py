"""Datadog v2 software catalog & service definition schemas (read).

Scoped to entity listing and service-definition get/list. The entity
``relationships``/``included`` sideload graph and the versioned service-definition
``schema`` (v1/v2/v2.1/v2.2 zoo) are left loose as ``dict`` / ``list[dict]``.
Kinds, relations, and upsert endpoints are deferred to their own tools.
"""

from typing import Any

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource


class EntityResponseDataAttributes(DatadogModel):
    api_version: str | None = Field(default=None, alias="apiVersion")
    description: str | None = None
    display_name: str | None = Field(default=None, alias="displayName")
    kind: str | None = None
    name: str | None = None
    namespace: str | None = None
    owner: str | None = None
    properties: dict[str, Any] | None = None
    tags: list[str] | None = None


class EntityData(DatadogModel):
    id: str | None = None
    type: str | None = None
    attributes: EntityResponseDataAttributes | None = None
    relationships: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None


type EntityResponseData = list[EntityData]


class ListEntityCatalogResponseLinks(DatadogModel):
    next: str | None = None
    previous: str | None = None
    self_: str | None = Field(default=None, alias="self")


class EntityResponseMeta(DatadogModel):
    count: int | None = None
    include_count: int | None = Field(default=None, alias="includeCount")


class ListEntityCatalogResponse(DatadogModel):
    data: EntityResponseData | None = None
    included: list[dict[str, Any]] | None = None
    links: ListEntityCatalogResponseLinks | None = None
    meta: EntityResponseMeta | None = None


class ServiceDefinitionMetaWarnings(DatadogModel):
    instance_location: str | None = Field(default=None, alias="instance-location")
    keyword_location: str | None = Field(default=None, alias="keyword-location")
    message: str | None = None


class ServiceDefinitionMeta(DatadogModel):
    github_html_url: str | None = Field(default=None, alias="github-html-url")
    ingested_schema_version: str | None = Field(
        default=None, alias="ingested-schema-version"
    )
    ingestion_source: str | None = Field(default=None, alias="ingestion-source")
    last_modified_time: str | None = Field(default=None, alias="last-modified-time")
    origin: str | None = None
    origin_detail: str | None = Field(default=None, alias="origin-detail")
    warnings: list[ServiceDefinitionMetaWarnings] | None = None


class ServiceDefinitionDataAttributes(DatadogModel):
    meta: ServiceDefinitionMeta | None = None
    schema_: dict[str, Any] | None = Field(default=None, alias="schema")


type ServiceDefinitionData = JSONAPIResource[ServiceDefinitionDataAttributes]


class ServiceDefinitionGetResponse(DatadogModel):
    data: ServiceDefinitionData | None = None


class ServiceDefinitionsListResponse(DatadogModel):
    data: list[ServiceDefinitionData] | None = None

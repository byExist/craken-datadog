"""Datadog v2 live container inventory schemas.

The ``ContainerItem`` in the spec is a oneOf (``Container`` | ``ContainerGroup``);
the grouped variant only appears with ``group_by``, which the client does not
expose, so responses are always the typed single-container shape.
"""

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource


class ContainerAttributes(DatadogModel):
    container_id: str | None = None
    created_at: str | None = None
    host: str | None = None
    image_digest: str | None = None
    image_name: str | None = None
    image_tags: list[str] | None = None
    name: str | None = None
    started_at: str | None = None
    state: str | None = None
    tags: list[str] | None = None


type Container = JSONAPIResource[ContainerAttributes]


class ContainersResponseLinks(DatadogModel):
    first: str | None = None
    last: str | None = None
    next: str | None = None
    prev: str | None = None
    self_: str | None = Field(default=None, alias="self")


class ContainerMetaPage(DatadogModel):
    cursor: str | None = None
    limit: int | None = None
    next_cursor: str | None = None
    prev_cursor: str | None = None
    total: int | None = None
    type: str | None = None


class ContainerMeta(DatadogModel):
    pagination: ContainerMetaPage | None = None


class ContainersResponse(DatadogModel):
    data: list[Container] | None = None
    links: ContainersResponseLinks | None = None
    meta: ContainerMeta | None = None

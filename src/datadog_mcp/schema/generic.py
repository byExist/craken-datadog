"""Generic JSON:API models parametrized by the resource attributes."""

from datadog_mcp.schema.base import DatadogModel


class JSONAPIResource[AttributesT](DatadogModel):
    id: str | None = None
    type: str | None = None
    attributes: AttributesT | None = None

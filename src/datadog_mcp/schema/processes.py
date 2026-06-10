"""Datadog v2 live process inventory schemas."""

from datadog_mcp.schema.base import DatadogModel
from datadog_mcp.schema.generic import JSONAPIResource


class ProcessSummaryAttributes(DatadogModel):
    cmdline: str | None = None
    host: str | None = None
    pid: int | None = None
    ppid: int | None = None
    start: str | None = None
    tags: list[str] | None = None
    timestamp: str | None = None
    user: str | None = None


type ProcessSummary = JSONAPIResource[ProcessSummaryAttributes]


class ProcessSummariesMetaPage(DatadogModel):
    after: str | None = None
    size: int | None = None


class ProcessSummariesMeta(DatadogModel):
    page: ProcessSummariesMetaPage | None = None


class ProcessSummariesResponse(DatadogModel):
    data: list[ProcessSummary] | None = None
    meta: ProcessSummariesMeta | None = None

"""Datadog v1 synthetics schemas (read: list tests, latest results).

Test ``config``/``options``/``steps`` (the API/browser assertion & step zoo) and
result ``timings``/browser result detail are left loose as ``dict`` / ``list[dict]``.
Global variables, private locations, and CI triggers are deferred to their own tools.
"""

from typing import Any

from datadog_mcp.schema.base import DatadogModel

# str, not Literal: test types and subtypes grow (e.g. grpc), so a Literal rejects
# real payloads.
type SyntheticsTestDetailsType = str
type SyntheticsTestDetailsSubType = str
type SyntheticsTestPauseStatus = str
type SyntheticsTestMonitorStatus = int


class Creator(DatadogModel):
    email: str | None = None
    handle: str | None = None
    name: str | None = None


class SyntheticsTestDetailsWithoutSteps(DatadogModel):
    config: dict[str, Any] | None = None
    creator: Creator | None = None
    locations: list[str] | None = None
    message: str | None = None
    monitor_id: int | None = None
    name: str | None = None
    options: dict[str, Any] | None = None
    public_id: str | None = None
    status: SyntheticsTestPauseStatus | None = None
    subtype: SyntheticsTestDetailsSubType | None = None
    tags: list[str] | None = None
    type: SyntheticsTestDetailsType | None = None


class SyntheticsTestDetails(DatadogModel):
    config: dict[str, Any] | None = None
    creator: Creator | None = None
    locations: list[str] | None = None
    message: str | None = None
    monitor_id: int | None = None
    name: str | None = None
    options: dict[str, Any] | None = None
    public_id: str | None = None
    status: SyntheticsTestPauseStatus | None = None
    steps: list[dict[str, Any]] | None = None
    subtype: SyntheticsTestDetailsSubType | None = None
    tags: list[str] | None = None
    type: SyntheticsTestDetailsType | None = None


class SyntheticsListTestsResponse(DatadogModel):
    tests: list[SyntheticsTestDetailsWithoutSteps] | None = None


class SyntheticsAPITestResultShortResult(DatadogModel):
    passed: bool | None = None
    timings: dict[str, Any] | None = None


class SyntheticsAPITestResultShort(DatadogModel):
    check_time: float | None = None
    probe_dc: str | None = None
    result: SyntheticsAPITestResultShortResult | None = None
    result_id: str | None = None
    status: SyntheticsTestMonitorStatus | None = None


class SyntheticsGetAPITestLatestResultsResponse(DatadogModel):
    last_timestamp_fetched: int | None = None
    results: list[SyntheticsAPITestResultShort] | None = None


class SyntheticsBrowserTestResultShort(DatadogModel):
    check_time: float | None = None
    probe_dc: str | None = None
    result: dict[str, Any] | None = None
    result_id: str | None = None
    status: SyntheticsTestMonitorStatus | None = None


class SyntheticsGetBrowserTestLatestResultsResponse(DatadogModel):
    last_timestamp_fetched: int | None = None
    results: list[SyntheticsBrowserTestResultShort] | None = None

"""Datadog API client.

A lazy-singleton ``httpx.Client`` over ``https://api.{site}``, authenticated with
the ``DD-API-KEY`` / ``DD-APPLICATION-KEY`` headers and built on first use so the
MCP server starts even before credentials are configured. Module-level functions
issue one request each and return typed schema models; the shared ``error_hook``
raises on any non-2xx, so the functions stay at call-then-validate.
"""

from typing import Any

import httpx

from datadog_mcp.config import get_auth
from datadog_mcp.errors import error_hook
from datadog_mcp.schema.containers import ContainersResponse
from datadog_mcp.schema.dashboards import Dashboard, DashboardSummary
from datadog_mcp.schema.downtimes import DowntimeResponse, ListDowntimesResponse
from datadog_mcp.schema.events import EventsListResponse, V2EventResponse
from datadog_mcp.schema.host import HostListResponse, HostTotals
from datadog_mcp.schema.incidents import (
    IncidentResponse,
    IncidentSearchResponse,
    IncidentsResponse,
)
from datadog_mcp.schema.logs import LogsAggregateResponse, LogsListResponse
from datadog_mcp.schema.metrics import (
    MetricsAndMetricTagConfigurationsResponse,
    ScalarFormulaQueryResponse,
    TimeseriesFormulaQueryResponse,
)
from datadog_mcp.schema.monitors import Monitor, MonitorSearchResponse
from datadog_mcp.schema.processes import ProcessSummariesResponse
from datadog_mcp.schema.rum import RUMAnalyticsAggregateResponse, RUMEventsResponse
from datadog_mcp.schema.services import (
    ListEntityCatalogResponse,
    ServiceDefinitionGetResponse,
)
from datadog_mcp.schema.slo import SLOListResponse, SLOResponse, SloStatusResponse
from datadog_mcp.schema.spans import SpansAggregateResponse, SpansListResponse
from datadog_mcp.schema.synthetics import (
    SyntheticsGetAPITestLatestResultsResponse,
    SyntheticsGetBrowserTestLatestResultsResponse,
    SyntheticsListTestsResponse,
)
from datadog_mcp.schema.traces import PrunedTraceResponse, TraceResponse

_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        auth = get_auth()
        _client = httpx.Client(
            base_url=f"https://api.{auth.site}",
            headers={
                "DD-API-KEY": auth.api_key.get_secret_value(),
                "DD-APPLICATION-KEY": auth.app_key.get_secret_value(),
                "Accept": "application/json",
            },
            event_hooks={"response": [error_hook]},
        )
    return _client


def search_logs(
    query: str,
    *,
    from_: str | None = None,
    to: str | None = None,
    sort: str | None = None,
    limit: int = 25,
    cursor: str | None = None,
) -> LogsListResponse:
    filter_: dict[str, Any] = {"query": query}
    if from_ is not None:
        filter_["from"] = from_
    if to is not None:
        filter_["to"] = to
    page: dict[str, Any] = {"limit": limit}
    if cursor is not None:
        page["cursor"] = cursor
    body: dict[str, Any] = {"filter": filter_, "page": page}
    if sort is not None:
        body["sort"] = sort
    resp = _get_client().post("/api/v2/logs/events/search", json=body)
    return LogsListResponse.model_validate(resp.json())


def aggregate_logs(
    query: str,
    compute: list[dict[str, Any]],
    *,
    from_: str | None = None,
    to: str | None = None,
    group_by: list[dict[str, Any]] | None = None,
) -> LogsAggregateResponse:
    filter_: dict[str, Any] = {"query": query}
    if from_ is not None:
        filter_["from"] = from_
    if to is not None:
        filter_["to"] = to
    body: dict[str, Any] = {"filter": filter_, "compute": compute}
    if group_by is not None:
        body["group_by"] = group_by
    resp = _get_client().post("/api/v2/logs/analytics/aggregate", json=body)
    return LogsAggregateResponse.model_validate(resp.json())


def search_rum_events(
    query: str,
    *,
    from_: str | None = None,
    to: str | None = None,
    sort: str | None = None,
    limit: int = 25,
    cursor: str | None = None,
) -> RUMEventsResponse:
    filter_: dict[str, Any] = {"query": query}
    if from_ is not None:
        filter_["from"] = from_
    if to is not None:
        filter_["to"] = to
    page: dict[str, Any] = {"limit": limit}
    if cursor is not None:
        page["cursor"] = cursor
    body: dict[str, Any] = {"filter": filter_, "page": page}
    if sort is not None:
        body["sort"] = sort
    resp = _get_client().post("/api/v2/rum/events/search", json=body)
    return RUMEventsResponse.model_validate(resp.json())


def aggregate_rum_events(
    query: str,
    compute: list[dict[str, Any]],
    *,
    from_: str | None = None,
    to: str | None = None,
    group_by: list[dict[str, Any]] | None = None,
) -> RUMAnalyticsAggregateResponse:
    filter_: dict[str, Any] = {"query": query}
    if from_ is not None:
        filter_["from"] = from_
    if to is not None:
        filter_["to"] = to
    body: dict[str, Any] = {"filter": filter_, "compute": compute}
    if group_by is not None:
        body["group_by"] = group_by
    resp = _get_client().post("/api/v2/rum/analytics/aggregate", json=body)
    return RUMAnalyticsAggregateResponse.model_validate(resp.json())


def list_hosts(
    *,
    filter_: str | None = None,
    sort_field: str | None = None,
    sort_dir: str | None = None,
    start: int | None = None,
    count: int = 100,
    from_: int | None = None,
    include_muted_hosts_data: bool | None = None,
    include_hosts_metadata: bool | None = None,
) -> HostListResponse:
    params: dict[str, Any] = {"count": count}
    if filter_ is not None:
        params["filter"] = filter_
    if sort_field is not None:
        params["sort_field"] = sort_field
    if sort_dir is not None:
        params["sort_dir"] = sort_dir
    if start is not None:
        params["start"] = start
    if from_ is not None:
        params["from"] = from_
    if include_muted_hosts_data is not None:
        params["include_muted_hosts_data"] = include_muted_hosts_data
    if include_hosts_metadata is not None:
        params["include_hosts_metadata"] = include_hosts_metadata
    resp = _get_client().get("/api/v1/hosts", params=params)
    return HostListResponse.model_validate(resp.json())


def get_host_totals(*, from_: int | None = None) -> HostTotals:
    params: dict[str, Any] = {}
    if from_ is not None:
        params["from"] = from_
    resp = _get_client().get("/api/v1/hosts/totals", params=params)
    return HostTotals.model_validate(resp.json())


def list_containers(
    *,
    filter_tags: str | None = None,
    sort: str | None = None,
    page_size: int | None = None,
    page_cursor: str | None = None,
) -> ContainersResponse:
    params: dict[str, Any] = {}
    if filter_tags is not None:
        params["filter[tags]"] = filter_tags
    if sort is not None:
        params["sort"] = sort
    if page_size is not None:
        params["page[size]"] = page_size
    if page_cursor is not None:
        params["page[cursor]"] = page_cursor
    resp = _get_client().get("/api/v2/containers", params=params)
    return ContainersResponse.model_validate(resp.json())


def list_processes(
    *,
    search: str | None = None,
    tags: str | None = None,
    from_: int | None = None,
    to: int | None = None,
    limit: int | None = None,
    cursor: str | None = None,
) -> ProcessSummariesResponse:
    params: dict[str, Any] = {}
    if search is not None:
        params["search"] = search
    if tags is not None:
        params["tags"] = tags
    if from_ is not None:
        params["from"] = from_
    if to is not None:
        params["to"] = to
    if limit is not None:
        params["page[limit]"] = limit
    if cursor is not None:
        params["page[cursor]"] = cursor
    resp = _get_client().get("/api/v2/processes", params=params)
    return ProcessSummariesResponse.model_validate(resp.json())


def list_events(
    *,
    query: str | None = None,
    from_: str | None = None,
    to: str | None = None,
    sort: str | None = None,
    limit: int = 25,
    cursor: str | None = None,
) -> EventsListResponse:
    params: dict[str, Any] = {"page[limit]": limit}
    if query is not None:
        params["filter[query]"] = query
    if from_ is not None:
        params["filter[from]"] = from_
    if to is not None:
        params["filter[to]"] = to
    if sort is not None:
        params["sort"] = sort
    if cursor is not None:
        params["page[cursor]"] = cursor
    resp = _get_client().get("/api/v2/events", params=params)
    return EventsListResponse.model_validate(resp.json())


def get_event(event_id: str) -> V2EventResponse:
    resp = _get_client().get(f"/api/v2/events/{event_id}")
    return V2EventResponse.model_validate(resp.json())


def search_spans(
    query: str,
    *,
    from_: str | None = None,
    to: str | None = None,
    sort: str | None = None,
    limit: int = 25,
    cursor: str | None = None,
) -> SpansListResponse:
    filter_: dict[str, Any] = {"query": query}
    if from_ is not None:
        filter_["from"] = from_
    if to is not None:
        filter_["to"] = to
    page: dict[str, Any] = {"limit": limit}
    if cursor is not None:
        page["cursor"] = cursor
    attributes: dict[str, Any] = {"filter": filter_, "page": page}
    if sort is not None:
        attributes["sort"] = sort
    body = {"data": {"type": "search_request", "attributes": attributes}}
    resp = _get_client().post("/api/v2/spans/events/search", json=body)
    return SpansListResponse.model_validate(resp.json())


def aggregate_spans(
    query: str,
    compute: list[dict[str, Any]],
    *,
    from_: str | None = None,
    to: str | None = None,
    group_by: list[dict[str, Any]] | None = None,
) -> SpansAggregateResponse:
    filter_: dict[str, Any] = {"query": query}
    if from_ is not None:
        filter_["from"] = from_
    if to is not None:
        filter_["to"] = to
    attributes: dict[str, Any] = {"filter": filter_, "compute": compute}
    if group_by is not None:
        attributes["group_by"] = group_by
    body = {"data": {"type": "aggregate_request", "attributes": attributes}}
    resp = _get_client().post("/api/v2/spans/analytics/aggregate", json=body)
    return SpansAggregateResponse.model_validate(resp.json())


def get_trace(trace_id: str) -> TraceResponse:
    resp = _get_client().get(f"/api/v2/trace/{trace_id}")
    return TraceResponse.model_validate(resp.json())


def get_pruned_trace(trace_id: str) -> PrunedTraceResponse:
    resp = _get_client().get(f"/api/v2/pruned_trace/{trace_id}")
    return PrunedTraceResponse.model_validate(resp.json())


def list_monitors(
    *,
    group_states: str | None = None,
    name: str | None = None,
    tags: str | None = None,
    monitor_tags: str | None = None,
    with_downtimes: bool | None = None,
    page: int = 0,
    page_size: int = 100,
) -> list[Monitor]:
    params: dict[str, Any] = {"page": page, "page_size": page_size}
    if group_states is not None:
        params["group_states"] = group_states
    if name is not None:
        params["name"] = name
    if tags is not None:
        params["tags"] = tags
    if monitor_tags is not None:
        params["monitor_tags"] = monitor_tags
    if with_downtimes is not None:
        params["with_downtimes"] = with_downtimes
    resp = _get_client().get("/api/v1/monitor", params=params)
    return [Monitor.model_validate(item) for item in resp.json()]


def get_monitor(
    monitor_id: int,
    *,
    group_states: str | None = None,
    with_downtimes: bool | None = None,
) -> Monitor:
    params: dict[str, Any] = {}
    if group_states is not None:
        params["group_states"] = group_states
    if with_downtimes is not None:
        params["with_downtimes"] = with_downtimes
    resp = _get_client().get(f"/api/v1/monitor/{monitor_id}", params=params)
    return Monitor.model_validate(resp.json())


def search_monitors(
    query: str,
    *,
    page: int = 0,
    per_page: int = 30,
    sort: str | None = None,
) -> MonitorSearchResponse:
    params: dict[str, Any] = {"query": query, "page": page, "per_page": per_page}
    if sort is not None:
        params["sort"] = sort
    resp = _get_client().get("/api/v1/monitor/search", params=params)
    return MonitorSearchResponse.model_validate(resp.json())


def query_timeseries(
    queries: list[dict[str, Any]],
    *,
    from_: int,
    to: int,
    formulas: list[dict[str, Any]] | None = None,
) -> TimeseriesFormulaQueryResponse:
    attributes: dict[str, Any] = {"from": from_, "to": to, "queries": queries}
    if formulas is not None:
        attributes["formulas"] = formulas
    body = {"data": {"type": "timeseries_request", "attributes": attributes}}
    resp = _get_client().post("/api/v2/query/timeseries", json=body)
    return TimeseriesFormulaQueryResponse.model_validate(resp.json())


def query_scalar(
    queries: list[dict[str, Any]],
    *,
    from_: int,
    to: int,
    formulas: list[dict[str, Any]] | None = None,
) -> ScalarFormulaQueryResponse:
    attributes: dict[str, Any] = {"from": from_, "to": to, "queries": queries}
    if formulas is not None:
        attributes["formulas"] = formulas
    body = {"data": {"type": "scalar_request", "attributes": attributes}}
    resp = _get_client().post("/api/v2/query/scalar", json=body)
    return ScalarFormulaQueryResponse.model_validate(resp.json())


def list_metrics(
    *,
    filter_configured: bool | None = None,
    filter_tags: str | None = None,
    page_size: int | None = None,
    page_cursor: str | None = None,
) -> MetricsAndMetricTagConfigurationsResponse:
    params: dict[str, Any] = {}
    if filter_configured is not None:
        params["filter[configured]"] = filter_configured
    if filter_tags is not None:
        params["filter[tags]"] = filter_tags
    if page_size is not None:
        params["page[size]"] = page_size
    if page_cursor is not None:
        params["page[cursor]"] = page_cursor
    resp = _get_client().get("/api/v2/metrics", params=params)
    return MetricsAndMetricTagConfigurationsResponse.model_validate(resp.json())


def list_downtimes(
    *,
    current_only: bool | None = None,
    include: str | None = None,
    offset: int | None = None,
    limit: int = 30,
) -> ListDowntimesResponse:
    params: dict[str, Any] = {"page[limit]": limit}
    if current_only is not None:
        params["current_only"] = current_only
    if include is not None:
        params["include"] = include
    if offset is not None:
        params["page[offset]"] = offset
    resp = _get_client().get("/api/v2/downtime", params=params)
    return ListDowntimesResponse.model_validate(resp.json())


def get_downtime(downtime_id: str, *, include: str | None = None) -> DowntimeResponse:
    params: dict[str, Any] = {}
    if include is not None:
        params["include"] = include
    resp = _get_client().get(f"/api/v2/downtime/{downtime_id}", params=params)
    return DowntimeResponse.model_validate(resp.json())


def list_slos(
    *,
    ids: str | None = None,
    query: str | None = None,
    tags_query: str | None = None,
    metrics_query: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> SLOListResponse:
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if ids is not None:
        params["ids"] = ids
    if query is not None:
        params["query"] = query
    if tags_query is not None:
        params["tags_query"] = tags_query
    if metrics_query is not None:
        params["metrics_query"] = metrics_query
    resp = _get_client().get("/api/v1/slo", params=params)
    return SLOListResponse.model_validate(resp.json())


def get_slo(
    slo_id: str, *, with_configured_alert_ids: bool | None = None
) -> SLOResponse:
    params: dict[str, Any] = {}
    if with_configured_alert_ids is not None:
        params["with_configured_alert_ids"] = with_configured_alert_ids
    resp = _get_client().get(f"/api/v1/slo/{slo_id}", params=params)
    return SLOResponse.model_validate(resp.json())


def get_slo_status(
    slo_id: str,
    *,
    from_ts: int | None = None,
    to_ts: int | None = None,
    disable_corrections: bool | None = None,
) -> SloStatusResponse:
    params: dict[str, Any] = {}
    if from_ts is not None:
        params["from_ts"] = from_ts
    if to_ts is not None:
        params["to_ts"] = to_ts
    if disable_corrections is not None:
        params["disable_corrections"] = disable_corrections
    resp = _get_client().get(f"/api/v2/slo/{slo_id}/status", params=params)
    return SloStatusResponse.model_validate(resp.json())


def list_dashboards(
    *,
    filter_shared: bool | None = None,
    filter_deleted: bool | None = None,
    count: int | None = None,
    start: int | None = None,
) -> DashboardSummary:
    params: dict[str, Any] = {}
    if filter_shared is not None:
        params["filter[shared]"] = filter_shared
    if filter_deleted is not None:
        params["filter[deleted]"] = filter_deleted
    if count is not None:
        params["count"] = count
    if start is not None:
        params["start"] = start
    resp = _get_client().get("/api/v1/dashboard", params=params)
    return DashboardSummary.model_validate(resp.json())


def get_dashboard(dashboard_id: str) -> Dashboard:
    resp = _get_client().get(f"/api/v1/dashboard/{dashboard_id}")
    return Dashboard.model_validate(resp.json())


def list_catalog_entities(
    *,
    filter_name: str | None = None,
    filter_kind: str | None = None,
    filter_ref: str | None = None,
    include: str | None = None,
    page_limit: int = 100,
    page_offset: int | None = None,
) -> ListEntityCatalogResponse:
    params: dict[str, Any] = {"page[limit]": page_limit}
    if filter_name is not None:
        params["filter[name]"] = filter_name
    if filter_kind is not None:
        params["filter[kind]"] = filter_kind
    if filter_ref is not None:
        params["filter[ref]"] = filter_ref
    if include is not None:
        params["include"] = include
    if page_offset is not None:
        params["page[offset]"] = page_offset
    resp = _get_client().get("/api/v2/catalog/entity", params=params)
    return ListEntityCatalogResponse.model_validate(resp.json())


def get_service_definition(service_name: str) -> ServiceDefinitionGetResponse:
    resp = _get_client().get(f"/api/v2/services/definitions/{service_name}")
    return ServiceDefinitionGetResponse.model_validate(resp.json())


def list_incidents(
    *,
    include: str | None = None,
    size: int = 10,
    offset: int = 0,
) -> IncidentsResponse:
    params: dict[str, Any] = {"page[size]": size, "page[offset]": offset}
    if include is not None:
        params["include"] = include
    resp = _get_client().get("/api/v2/incidents", params=params)
    return IncidentsResponse.model_validate(resp.json())


def get_incident(incident_id: str, *, include: str | None = None) -> IncidentResponse:
    params: dict[str, Any] = {}
    if include is not None:
        params["include"] = include
    resp = _get_client().get(f"/api/v2/incidents/{incident_id}", params=params)
    return IncidentResponse.model_validate(resp.json())


def search_incidents(
    query: str,
    *,
    include: str | None = None,
    sort: str | None = None,
    size: int = 10,
    offset: int = 0,
) -> IncidentSearchResponse:
    params: dict[str, Any] = {
        "query": query,
        "page[size]": size,
        "page[offset]": offset,
    }
    if include is not None:
        params["include"] = include
    if sort is not None:
        params["sort"] = sort
    resp = _get_client().get("/api/v2/incidents/search", params=params)
    return IncidentSearchResponse.model_validate(resp.json())


def list_synthetic_tests(
    *,
    page_size: int | None = None,
    page_number: int | None = None,
) -> SyntheticsListTestsResponse:
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_number is not None:
        params["page_number"] = page_number
    resp = _get_client().get("/api/v1/synthetics/tests", params=params)
    return SyntheticsListTestsResponse.model_validate(resp.json())


def get_api_test_results(
    public_id: str,
    *,
    from_ts: int | None = None,
    to_ts: int | None = None,
    probe_dc: list[str] | None = None,
) -> SyntheticsGetAPITestLatestResultsResponse:
    params: dict[str, Any] = {}
    if from_ts is not None:
        params["from_ts"] = from_ts
    if to_ts is not None:
        params["to_ts"] = to_ts
    if probe_dc is not None:
        params["probe_dc"] = probe_dc
    resp = _get_client().get(
        f"/api/v1/synthetics/tests/{public_id}/results", params=params
    )
    return SyntheticsGetAPITestLatestResultsResponse.model_validate(resp.json())


def get_browser_test_results(
    public_id: str,
    *,
    from_ts: int | None = None,
    to_ts: int | None = None,
    probe_dc: list[str] | None = None,
) -> SyntheticsGetBrowserTestLatestResultsResponse:
    params: dict[str, Any] = {}
    if from_ts is not None:
        params["from_ts"] = from_ts
    if to_ts is not None:
        params["to_ts"] = to_ts
    if probe_dc is not None:
        params["probe_dc"] = probe_dc
    resp = _get_client().get(
        f"/api/v1/synthetics/tests/browser/{public_id}/results", params=params
    )
    return SyntheticsGetBrowserTestLatestResultsResponse.model_validate(resp.json())

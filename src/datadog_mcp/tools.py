"""Datadog MCP tools — thin wrappers over ``client``, registered by server.py.

Each tool delegates straight to a ``client`` function and returns its typed
schema model; the wrapper exists only to give the model an LLM-facing docstring
(the tool description) and parameter descriptions. All tools are read-only.
"""

from typing import Annotated, Any, TypeAlias

from pydantic import Field

from datadog_mcp import client
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

Query: TypeAlias = Annotated[
    str, Field(description="Datadog search query, e.g. 'service:web status:error'.")
]
TimeFrom: TypeAlias = Annotated[
    str | None,
    Field(
        description="Window start — relative date math like 'now-15m', ISO 8601, or epoch milliseconds."
    ),
]
TimeTo: TypeAlias = Annotated[
    str | None,
    Field(
        description="Window end — relative date math like 'now', ISO 8601, or epoch milliseconds."
    ),
]
Sort: TypeAlias = Annotated[
    str | None,
    Field(description="Sort order, e.g. 'timestamp' or '-timestamp' for descending."),
]
Limit: TypeAlias = Annotated[int, Field(description="Maximum number of results.")]
Cursor: TypeAlias = Annotated[
    str | None, Field(description="Pagination cursor returned by a prior call.")
]
Include: TypeAlias = Annotated[
    str | None, Field(description="Comma-separated related resources to side-load.")
]
Compute: TypeAlias = Annotated[
    list[dict[str, Any]],
    Field(description="Aggregations, e.g. [{'aggregation': 'count'}]."),
]
GroupBy: TypeAlias = Annotated[
    list[dict[str, Any]] | None,
    Field(description="Group-by facets, e.g. [{'facet': 'service'}]."),
]
Queries: TypeAlias = Annotated[
    list[dict[str, Any]],
    Field(
        description="Formula-and-function queries, e.g. "
        "[{'data_source': 'metrics', 'query': 'avg:system.cpu.user{*}', 'name': 'a'}]."
    ),
]
Formulas: TypeAlias = Annotated[
    list[dict[str, Any]] | None,
    Field(description="Formulas over the queries, e.g. [{'formula': 'a'}]."),
]
EpochMs: TypeAlias = Annotated[
    int, Field(description="Timestamp in milliseconds since the Unix epoch.")
]


def search_logs(
    query: Query,
    *,
    from_: TimeFrom = None,
    to: TimeTo = None,
    sort: Sort = None,
    limit: Limit = 25,
    cursor: Cursor = None,
) -> LogsListResponse:
    """Search log events matching a Datadog log query (set sort for order)."""
    return client.search_logs(
        query, from_=from_, to=to, sort=sort, limit=limit, cursor=cursor
    )


def aggregate_logs(
    query: Query,
    compute: Compute,
    *,
    from_: TimeFrom = None,
    to: TimeTo = None,
    group_by: GroupBy = None,
) -> LogsAggregateResponse:
    """Aggregate logs into buckets (counts, timeseries, group-bys) for trends."""
    return client.aggregate_logs(query, compute, from_=from_, to=to, group_by=group_by)


def search_rum_events(
    query: Query,
    *,
    from_: TimeFrom = None,
    to: TimeTo = None,
    sort: Sort = None,
    limit: Limit = 25,
    cursor: Cursor = None,
) -> RUMEventsResponse:
    """Search RUM (Real User Monitoring) events — browser/mobile sessions, views, errors, actions."""
    return client.search_rum_events(
        query, from_=from_, to=to, sort=sort, limit=limit, cursor=cursor
    )


def aggregate_rum_events(
    query: Query,
    compute: Compute,
    *,
    from_: TimeFrom = None,
    to: TimeTo = None,
    group_by: GroupBy = None,
) -> RUMAnalyticsAggregateResponse:
    """Aggregate RUM events into buckets (counts, timeseries, group-bys) for frontend trends."""
    return client.aggregate_rum_events(
        query, compute, from_=from_, to=to, group_by=group_by
    )


def list_hosts(
    *,
    filter_: Annotated[
        str | None, Field(description="Host filter query, e.g. 'env:prod'.")
    ] = None,
    sort_field: Annotated[
        str | None, Field(description="Field to sort by, e.g. 'cpu', 'status'.")
    ] = None,
    sort_dir: Annotated[
        str | None, Field(description="Sort direction: 'asc' or 'desc'.")
    ] = None,
    start: Annotated[int | None, Field(description="Result offset for paging.")] = None,
    count: Annotated[int, Field(description="Max hosts to return (max 1000).")] = 100,
    from_: Annotated[
        int | None,
        Field(description="Only hosts reporting since this Unix epoch (seconds)."),
    ] = None,
    include_muted_hosts_data: Annotated[
        bool | None, Field(description="Include each host's mute status.")
    ] = None,
    include_hosts_metadata: Annotated[
        bool | None, Field(description="Include host metadata (agent version, etc.).")
    ] = None,
) -> HostListResponse:
    """List infrastructure hosts by name, alias, or tag (active in the last 3 hours by default) with metadata and mute status."""
    return client.list_hosts(
        filter_=filter_,
        sort_field=sort_field,
        sort_dir=sort_dir,
        start=start,
        count=count,
        from_=from_,
        include_muted_hosts_data=include_muted_hosts_data,
        include_hosts_metadata=include_hosts_metadata,
    )


def get_host_totals(
    *,
    from_: Annotated[
        int | None,
        Field(
            description="Only count hosts reporting since this Unix epoch (seconds)."
        ),
    ] = None,
) -> HostTotals:
    """Get the total number of active (reported in the last hour) and up (last two hours) hosts."""
    return client.get_host_totals(from_=from_)


def list_containers(
    *,
    filter_tags: Annotated[
        str | None, Field(description="Filter by tags, e.g. 'kube_namespace:prod'.")
    ] = None,
    sort: Annotated[
        str | None, Field(description="Sort field; prefix '-' for descending.")
    ] = None,
    page_size: Annotated[int | None, Field(description="Containers per page.")] = None,
    page_cursor: Cursor = None,
) -> ContainersResponse:
    """List running containers with their image, host, state, and tags."""
    return client.list_containers(
        filter_tags=filter_tags, sort=sort, page_size=page_size, page_cursor=page_cursor
    )


def list_processes(
    *,
    search: Annotated[
        str | None, Field(description="Substring match on the process command line.")
    ] = None,
    tags: Annotated[
        str | None, Field(description="Filter by tags, e.g. 'host:web-1'.")
    ] = None,
    from_: Annotated[
        int | None, Field(description="Window start in epoch seconds.")
    ] = None,
    to: Annotated[int | None, Field(description="Window end in epoch seconds.")] = None,
    limit: Annotated[int | None, Field(description="Processes per page.")] = None,
    cursor: Cursor = None,
) -> ProcessSummariesResponse:
    """List running processes (command line, host, user, PID) across your hosts."""
    return client.list_processes(
        search=search, tags=tags, from_=from_, to=to, limit=limit, cursor=cursor
    )


def list_events(
    *,
    query: Annotated[
        str | None, Field(description="Event search query; omit to match all.")
    ] = None,
    from_: TimeFrom = None,
    to: TimeTo = None,
    sort: Sort = None,
    limit: Limit = 25,
    cursor: Cursor = None,
) -> EventsListResponse:
    """List events from the event stream (deployments, alerts, changes)."""
    return client.list_events(
        query=query, from_=from_, to=to, sort=sort, limit=limit, cursor=cursor
    )


def get_event(
    event_id: Annotated[str, Field(description="The event's ID.")],
) -> V2EventResponse:
    """Get a single event by its ID."""
    return client.get_event(event_id)


def search_spans(
    query: Query,
    *,
    from_: TimeFrom = None,
    to: TimeTo = None,
    sort: Sort = None,
    limit: Limit = 25,
    cursor: Cursor = None,
) -> SpansListResponse:
    """Search APM spans (distributed traces) matching a query; rate limited to 300 req/hour."""
    return client.search_spans(
        query, from_=from_, to=to, sort=sort, limit=limit, cursor=cursor
    )


def aggregate_spans(
    query: Query,
    compute: Compute,
    *,
    from_: TimeFrom = None,
    to: TimeTo = None,
    group_by: GroupBy = None,
) -> SpansAggregateResponse:
    """Aggregate APM spans into buckets for latency/throughput/error analytics; rate limited to 300 req/hour."""
    return client.aggregate_spans(query, compute, from_=from_, to=to, group_by=group_by)


def get_trace(
    trace_id: Annotated[str, Field(description="The 128-bit trace ID (32-char hex).")],
) -> TraceResponse:
    """Get a full APM trace by ID — every span as a flat list (preview API; large traces can be sizable)."""
    return client.get_trace(trace_id)


def get_pruned_trace(
    trace_id: Annotated[str, Field(description="The 128-bit trace ID (32-char hex).")],
) -> PrunedTraceResponse:
    """Get a pruned APM trace by ID — a size-reduced hierarchical span tree, ideal for inspecting one trace cheaply (preview API)."""
    return client.get_pruned_trace(trace_id)


def list_monitors(
    *,
    group_states: Annotated[
        str | None,
        Field(
            description="Group states to annotate, any of: all, alert, warn, no data (comma-separated)."
        ),
    ] = None,
    name: Annotated[str | None, Field(description="Filter by monitor name.")] = None,
    tags: Annotated[
        str | None, Field(description="Filter by scope tags, e.g. 'env:prod'.")
    ] = None,
    monitor_tags: Annotated[
        str | None, Field(description="Filter by monitor-level tags, e.g. 'team:sre'.")
    ] = None,
    with_downtimes: Annotated[
        bool | None, Field(description="Include matching downtimes per monitor.")
    ] = None,
    page: Annotated[int, Field(description="Zero-based page number.")] = 0,
    page_size: Annotated[int, Field(description="Monitors per page (max 1000).")] = 100,
) -> list[Monitor]:
    """List monitors, optionally filtered by name or tags, with current states."""
    return client.list_monitors(
        group_states=group_states,
        name=name,
        tags=tags,
        monitor_tags=monitor_tags,
        with_downtimes=with_downtimes,
        page=page,
        page_size=page_size,
    )


def get_monitor(
    monitor_id: Annotated[int, Field(description="The monitor's numeric ID.")],
    *,
    group_states: Annotated[
        str | None,
        Field(
            description="Group states to annotate, any of: all, alert, warn, no data (comma-separated)."
        ),
    ] = None,
    with_downtimes: Annotated[
        bool | None, Field(description="Include matching downtimes.")
    ] = None,
) -> Monitor:
    """Get a single monitor by ID, including its current state."""
    return client.get_monitor(
        monitor_id, group_states=group_states, with_downtimes=with_downtimes
    )


def search_monitors(
    query: Annotated[
        str, Field(description="Monitor search query, e.g. 'type:metric status:alert'.")
    ],
    *,
    page: Annotated[int, Field(description="Zero-based page number.")] = 0,
    per_page: Annotated[int, Field(description="Results per page.")] = 30,
    sort: Sort = None,
) -> MonitorSearchResponse:
    """Search monitors with a monitor query; returns matches with facet counts."""
    return client.search_monitors(query, page=page, per_page=per_page, sort=sort)


def query_timeseries(
    queries: Queries,
    *,
    from_: EpochMs,
    to: EpochMs,
    formulas: Formulas = None,
) -> TimeseriesFormulaQueryResponse:
    """Run a metrics timeseries query (v2 formula API), returning series of points."""
    return client.query_timeseries(queries, from_=from_, to=to, formulas=formulas)


def query_scalar(
    queries: Queries,
    *,
    from_: EpochMs,
    to: EpochMs,
    formulas: Formulas = None,
) -> ScalarFormulaQueryResponse:
    """Run a metrics scalar query (v2 formula API), one aggregated value per series."""
    return client.query_scalar(queries, from_=from_, to=to, formulas=formulas)


def list_metrics(
    *,
    filter_configured: Annotated[
        bool | None,
        Field(
            description="Only custom metrics configured with Metrics Without Limits."
        ),
    ] = None,
    filter_tags: Annotated[
        str | None,
        Field(
            description="Only metrics whose tags match this expression (supports AND/OR/IN and wildcards)."
        ),
    ] = None,
    page_size: Annotated[int | None, Field(description="Metrics per page.")] = None,
    page_cursor: Cursor = None,
) -> MetricsAndMetricTagConfigurationsResponse:
    """List metric names and their tag configurations, optionally filtered."""
    return client.list_metrics(
        filter_configured=filter_configured,
        filter_tags=filter_tags,
        page_size=page_size,
        page_cursor=page_cursor,
    )


def list_downtimes(
    *,
    current_only: Annotated[
        bool | None, Field(description="Only currently active downtimes.")
    ] = None,
    include: Include = None,
    offset: Annotated[
        int | None, Field(description="Result offset for paging.")
    ] = None,
    limit: Limit = 30,
) -> ListDowntimesResponse:
    """List scheduled downtimes that mute monitor notifications."""
    return client.list_downtimes(
        current_only=current_only, include=include, offset=offset, limit=limit
    )


def get_downtime(
    downtime_id: Annotated[str, Field(description="The downtime's ID.")],
    *,
    include: Include = None,
) -> DowntimeResponse:
    """Get a single downtime by ID."""
    return client.get_downtime(downtime_id, include=include)


def list_slos(
    *,
    ids: Annotated[
        str | None, Field(description="Comma-separated SLO IDs to fetch.")
    ] = None,
    query: Annotated[
        str | None, Field(description="Search by name, e.g. 'service:api'.")
    ] = None,
    tags_query: Annotated[
        str | None, Field(description="Filter by tags, e.g. 'env:prod'.")
    ] = None,
    metrics_query: Annotated[
        str | None, Field(description="Filter by metric in the SLO definition.")
    ] = None,
    limit: Limit = 100,
    offset: Annotated[int, Field(description="Result offset for paging.")] = 0,
) -> SLOListResponse:
    """List service level objectives, optionally filtered by query or tags."""
    return client.list_slos(
        ids=ids,
        query=query,
        tags_query=tags_query,
        metrics_query=metrics_query,
        limit=limit,
        offset=offset,
    )


def get_slo(
    slo_id: Annotated[str, Field(description="The SLO's ID.")],
    *,
    with_configured_alert_ids: Annotated[
        bool | None, Field(description="Include IDs of alerts tied to the SLO.")
    ] = None,
) -> SLOResponse:
    """Get a single SLO by ID with its config and thresholds."""
    return client.get_slo(slo_id, with_configured_alert_ids=with_configured_alert_ids)


def get_slo_status(
    slo_id: Annotated[str, Field(description="The SLO's ID.")],
    *,
    from_ts: Annotated[
        int | None,
        Field(
            description="Window start in epoch seconds (defaults to the SLO timeframe)."
        ),
    ] = None,
    to_ts: Annotated[
        int | None, Field(description="Window end in epoch seconds.")
    ] = None,
    disable_corrections: Annotated[
        bool | None,
        Field(description="Exclude SLO correction windows from the calculation."),
    ] = None,
) -> SloStatusResponse:
    """Get an SLO's live status — current SLI value and error budget remaining over a window (preview API)."""
    return client.get_slo_status(
        slo_id, from_ts=from_ts, to_ts=to_ts, disable_corrections=disable_corrections
    )


def list_dashboards(
    *,
    filter_shared: Annotated[
        bool | None, Field(description="Only shared (or non-shared) dashboards.")
    ] = None,
    filter_deleted: Annotated[
        bool | None, Field(description="Only deleted dashboards.")
    ] = None,
    count: Annotated[int | None, Field(description="Max dashboards to return.")] = None,
    start: Annotated[int | None, Field(description="Result offset for paging.")] = None,
) -> DashboardSummary:
    """List custom and cloned dashboards with summary metadata (id, title, author); preset dashboards are excluded."""
    return client.list_dashboards(
        filter_shared=filter_shared,
        filter_deleted=filter_deleted,
        count=count,
        start=start,
    )


def get_dashboard(
    dashboard_id: Annotated[str, Field(description="The dashboard's ID.")],
) -> Dashboard:
    """Get a single dashboard by ID, including its widgets and layout."""
    return client.get_dashboard(dashboard_id)


def list_catalog_entities(
    *,
    filter_name: Annotated[
        str | None, Field(description="Filter by entity name.")
    ] = None,
    filter_kind: Annotated[
        str | None, Field(description="Filter by kind, e.g. 'service', 'system'.")
    ] = None,
    filter_ref: Annotated[
        str | None, Field(description="Filter by reference, e.g. 'service:checkout'.")
    ] = None,
    include: Include = None,
    page_limit: Annotated[int, Field(description="Entities per page.")] = 100,
    page_offset: Annotated[
        int | None, Field(description="Result offset for paging.")
    ] = None,
) -> ListEntityCatalogResponse:
    """List software catalog entities (services, systems) with their metadata."""
    return client.list_catalog_entities(
        filter_name=filter_name,
        filter_kind=filter_kind,
        filter_ref=filter_ref,
        include=include,
        page_limit=page_limit,
        page_offset=page_offset,
    )


def get_service_definition(
    service_name: Annotated[str, Field(description="The service's name.")],
) -> ServiceDefinitionGetResponse:
    """Get a service's definition (schema v2) from the service catalog."""
    return client.get_service_definition(service_name)


def list_incidents(
    *,
    include: Include = None,
    size: Annotated[int, Field(description="Incidents per page (max 100).")] = 10,
    offset: Annotated[int, Field(description="Result offset for paging.")] = 0,
) -> IncidentsResponse:
    """List incidents with their attributes (severity, state, timing)."""
    return client.list_incidents(include=include, size=size, offset=offset)


def get_incident(
    incident_id: Annotated[str, Field(description="The incident's ID.")],
    *,
    include: Include = None,
) -> IncidentResponse:
    """Get a single incident by ID."""
    return client.get_incident(incident_id, include=include)


def search_incidents(
    query: Annotated[
        str, Field(description="Incident search query, e.g. 'state:active'.")
    ],
    *,
    include: Include = None,
    sort: Sort = None,
    size: Annotated[int, Field(description="Incidents per page (max 100).")] = 10,
    offset: Annotated[int, Field(description="Result offset for paging.")] = 0,
) -> IncidentSearchResponse:
    """Search incidents with a query; returns matches with facets."""
    return client.search_incidents(
        query, include=include, sort=sort, size=size, offset=offset
    )


def list_synthetic_tests(
    *,
    page_size: Annotated[int | None, Field(description="Tests per page.")] = None,
    page_number: Annotated[
        int | None, Field(description="Zero-based page number.")
    ] = None,
) -> SyntheticsListTestsResponse:
    """List Synthetic tests (API and browser) with their config and status."""
    return client.list_synthetic_tests(page_size=page_size, page_number=page_number)


def get_api_test_results(
    public_id: Annotated[str, Field(description="The Synthetic test's public ID.")],
    *,
    from_ts: Annotated[
        int | None, Field(description="Results after this Unix epoch (milliseconds).")
    ] = None,
    to_ts: Annotated[
        int | None, Field(description="Results before this Unix epoch (milliseconds).")
    ] = None,
    probe_dc: Annotated[
        list[str] | None,
        Field(description="Filter to these locations, e.g. ['aws:us-east-1']."),
    ] = None,
) -> SyntheticsGetAPITestLatestResultsResponse:
    """Get the last 150 result summaries for a Synthetic API test."""
    return client.get_api_test_results(
        public_id, from_ts=from_ts, to_ts=to_ts, probe_dc=probe_dc
    )


def get_browser_test_results(
    public_id: Annotated[str, Field(description="The Synthetic test's public ID.")],
    *,
    from_ts: Annotated[
        int | None, Field(description="Results after this Unix epoch (milliseconds).")
    ] = None,
    to_ts: Annotated[
        int | None, Field(description="Results before this Unix epoch (milliseconds).")
    ] = None,
    probe_dc: Annotated[
        list[str] | None,
        Field(description="Filter to these locations, e.g. ['aws:us-east-1']."),
    ] = None,
) -> SyntheticsGetBrowserTestLatestResultsResponse:
    """Get the latest results for a Synthetic browser test."""
    return client.get_browser_test_results(
        public_id, from_ts=from_ts, to_ts=to_ts, probe_dc=probe_dc
    )

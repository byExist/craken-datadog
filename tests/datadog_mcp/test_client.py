from support import MockServer

from datadog_mcp.client import (
    aggregate_logs,
    aggregate_rum_events,
    aggregate_spans,
    get_api_test_results,
    get_browser_test_results,
    get_dashboard,
    get_downtime,
    get_event,
    get_host_totals,
    get_incident,
    get_log_indexes,
    get_monitor,
    get_pruned_trace,
    get_service_definition,
    get_slo,
    get_slo_status,
    get_trace,
    list_catalog_entities,
    list_containers,
    list_dashboards,
    list_downtimes,
    list_events,
    list_hosts,
    list_incidents,
    list_metrics,
    list_monitors,
    list_processes,
    list_slos,
    list_synthetic_tests,
    query_scalar,
    query_timeseries,
    search_incidents,
    search_logs,
    search_monitors,
    search_rum_events,
    search_spans,
)


def test_search_logs(datadog_api: MockServer):
    datadog_api.add(
        "POST",
        "/api/v2/logs/events/search",
        json={
            "data": [
                {
                    "id": "log1",
                    "type": "log",
                    "attributes": {
                        "message": "boom",
                        "service": "api",
                        "status": "error",
                    },
                }
            ],
            "meta": {"page": {"after": "cursor123"}},
            "links": {"next": "https://app/next"},
        },
    )

    result = search_logs(
        "service:api status:error",
        from_="now-15m",
        to="now",
        sort="-timestamp",
        limit=10,
        cursor="prev",
    )

    assert result.data is not None
    assert result.data[0].id == "log1"
    assert result.data[0].attributes is not None
    assert result.data[0].attributes.message == "boom"
    assert result.meta is not None
    assert result.meta.page is not None
    assert result.meta.page.after == "cursor123"

    req = datadog_api.last
    assert req.headers["DD-API-KEY"] == "dd-api-test"
    assert req.headers["DD-APPLICATION-KEY"] == "dd-app-test"
    assert str(req.url) == "https://api.datadoghq.com/api/v2/logs/events/search"
    body = MockServer.body(req)
    assert body["filter"] == {
        "query": "service:api status:error",
        "from": "now-15m",
        "to": "now",
    }
    assert body["page"] == {"limit": 10, "cursor": "prev"}
    assert body["sort"] == "-timestamp"


def test_search_logs_minimal(datadog_api: MockServer):
    datadog_api.add("POST", "/api/v2/logs/events/search", json={"data": []})

    result = search_logs("*")

    assert result.data == []
    assert MockServer.body(datadog_api.last) == {
        "filter": {"query": "*"},
        "page": {"limit": 25},
    }


def test_aggregate_logs(datadog_api: MockServer):
    datadog_api.add(
        "POST",
        "/api/v2/logs/analytics/aggregate",
        json={
            "data": {"buckets": [{"by": {"service": "api"}, "computes": {"c0": 42.0}}]}
        },
    )

    result = aggregate_logs(
        "service:api",
        compute=[{"aggregation": "count"}],
        from_="now-1h",
        to="now",
        group_by=[{"facet": "service"}],
    )

    assert result.data is not None
    assert result.data.buckets is not None
    assert result.data.buckets[0].computes == {"c0": 42.0}
    body = MockServer.body(datadog_api.last)
    assert body["filter"] == {"query": "service:api", "from": "now-1h", "to": "now"}
    assert body["compute"] == [{"aggregation": "count"}]
    assert body["group_by"] == [{"facet": "service"}]


def test_list_hosts(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v1/hosts", json={"host_list": [{}], "total_matching": 7}
    )

    result = list_hosts(
        filter_="env:prod",
        sort_field="cpu",
        sort_dir="desc",
        start=0,
        count=50,
        from_=1600000000,
        include_muted_hosts_data=True,
        include_hosts_metadata=False,
    )

    assert result.total_matching == 7
    assert result.host_list is not None
    p = datadog_api.last.url.params
    assert p["filter"] == "env:prod"
    assert p["sort_field"] == "cpu"
    assert p["sort_dir"] == "desc"
    assert p["start"] == "0"
    assert p["count"] == "50"
    assert p["from"] == "1600000000"
    assert p["include_muted_hosts_data"] == "true"
    assert p["include_hosts_metadata"] == "false"


def test_get_host_totals(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v1/hosts/totals", json={"total_active": 12, "total_up": 11}
    )

    result = get_host_totals(from_=1600000000)

    assert result.total_active == 12
    assert datadog_api.last.url.params["from"] == "1600000000"


def test_list_events(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v2/events", json={"data": [{"id": "e1", "type": "event"}]}
    )

    result = list_events(
        query="status:error",
        from_="now-1h",
        to="now",
        sort="-timestamp",
        limit=50,
        cursor="next",
    )

    assert result.data is not None
    assert result.data[0].id == "e1"
    p = datadog_api.last.url.params
    assert p["filter[query]"] == "status:error"
    assert p["filter[from]"] == "now-1h"
    assert p["filter[to]"] == "now"
    assert p["sort"] == "-timestamp"
    assert p["page[limit]"] == "50"
    assert p["page[cursor]"] == "next"


def test_get_event(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v2/events/abc", json={"data": {"id": "abc", "type": "event"}}
    )

    result = get_event("abc")

    assert result.data is not None
    assert result.data.id == "abc"
    assert datadog_api.last.url.path == "/api/v2/events/abc"


def test_search_spans(datadog_api: MockServer):
    datadog_api.add(
        "POST",
        "/api/v2/spans/events/search",
        json={"data": [{"id": "s1", "type": "spans"}], "meta": {"status": "done"}},
    )

    result = search_spans(
        "service:api",
        from_="now-15m",
        to="now",
        sort="-timestamp",
        limit=10,
        cursor="prev",
    )

    assert result.data is not None
    assert result.data[0].id == "s1"
    body = MockServer.body(datadog_api.last)
    assert body == {
        "data": {
            "type": "search_request",
            "attributes": {
                "filter": {"query": "service:api", "from": "now-15m", "to": "now"},
                "page": {"limit": 10, "cursor": "prev"},
                "sort": "-timestamp",
            },
        }
    }


def test_aggregate_spans(datadog_api: MockServer):
    datadog_api.add(
        "POST",
        "/api/v2/spans/analytics/aggregate",
        json={"data": [{"id": "b1", "type": "bucket"}]},
    )

    result = aggregate_spans(
        "service:api",
        compute=[{"aggregation": "count"}],
        from_="now-1h",
        to="now",
        group_by=[{"facet": "resource_name"}],
    )

    assert result.data is not None
    body = MockServer.body(datadog_api.last)
    assert body == {
        "data": {
            "type": "aggregate_request",
            "attributes": {
                "filter": {"query": "service:api", "from": "now-1h", "to": "now"},
                "compute": [{"aggregation": "count"}],
                "group_by": [{"facet": "resource_name"}],
            },
        }
    }


def test_get_trace(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/trace/abc123",
        json={
            "data": {
                "id": "abc123",
                "type": "trace",
                "attributes": {"spans": [{"spanID": 1, "service": "api"}]},
            }
        },
    )

    result = get_trace("abc123")

    assert result.data is not None
    assert result.data.id == "abc123"
    assert result.data.attributes is not None
    assert result.data.attributes.spans is not None
    assert result.data.attributes.spans[0].span_id == 1
    assert datadog_api.last.url.path == "/api/v2/trace/abc123"


def test_get_pruned_trace(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/pruned_trace/abc123",
        json={
            "data": {
                "id": "abc123",
                "type": "pruned_trace",
                "attributes": {
                    "size_bytes": 2048,
                    "summarized_trace": {
                        "root": {"spanID": 1, "children": [{"spanID": 2}]}
                    },
                },
            }
        },
    )

    result = get_pruned_trace("abc123")

    assert result.data is not None
    assert result.data.attributes is not None
    assert result.data.attributes.size_bytes == 2048
    st = result.data.attributes.summarized_trace
    assert st is not None
    assert st.root is not None
    assert st.root.children is not None
    assert st.root.children[0].span_id == 2
    assert datadog_api.last.url.path == "/api/v2/pruned_trace/abc123"


def test_list_monitors(datadog_api: MockServer):
    datadog_api.add("GET", "/api/v1/monitor", json=[{"id": 1, "name": "cpu high"}])

    result = list_monitors(
        group_states="all",
        name="cpu",
        tags="env:prod",
        monitor_tags="team:sre",
        with_downtimes=True,
        page=0,
        page_size=50,
    )

    assert result[0].id == 1
    assert result[0].name == "cpu high"
    p = datadog_api.last.url.params
    assert p["group_states"] == "all"
    assert p["name"] == "cpu"
    assert p["tags"] == "env:prod"
    assert p["monitor_tags"] == "team:sre"
    assert p["with_downtimes"] == "true"
    assert p["page"] == "0"
    assert p["page_size"] == "50"


def test_get_monitor(datadog_api: MockServer):
    datadog_api.add("GET", "/api/v1/monitor/42", json={"id": 42, "name": "disk"})

    result = get_monitor(42, group_states="alert", with_downtimes=False)

    assert result.id == 42
    p = datadog_api.last.url.params
    assert p["group_states"] == "alert"
    assert p["with_downtimes"] == "false"


def test_search_monitors(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v1/monitor/search",
        json={"monitors": [{"id": 1, "name": "x"}], "counts": {}, "metadata": {}},
    )

    result = search_monitors("type:metric", page=1, per_page=10, sort="name,asc")

    assert result.monitors is not None
    assert result.monitors[0].id == 1
    p = datadog_api.last.url.params
    assert p["query"] == "type:metric"
    assert p["page"] == "1"
    assert p["per_page"] == "10"
    assert p["sort"] == "name,asc"


def test_query_timeseries(datadog_api: MockServer):
    datadog_api.add("POST", "/api/v2/query/timeseries", json={"data": {}})

    result = query_timeseries(
        [{"data_source": "metrics", "query": "avg:system.cpu.user{*}", "name": "a"}],
        from_=1000,
        to=2000,
        formulas=[{"formula": "a"}],
    )

    assert result.data is not None
    body = MockServer.body(datadog_api.last)
    assert body == {
        "data": {
            "type": "timeseries_request",
            "attributes": {
                "from": 1000,
                "to": 2000,
                "queries": [
                    {
                        "data_source": "metrics",
                        "query": "avg:system.cpu.user{*}",
                        "name": "a",
                    }
                ],
                "formulas": [{"formula": "a"}],
            },
        }
    }


def test_query_scalar(datadog_api: MockServer):
    datadog_api.add("POST", "/api/v2/query/scalar", json={"data": {}})

    result = query_scalar(
        [{"data_source": "metrics", "query": "avg:system.cpu.user{*}", "name": "a"}],
        from_=1000,
        to=2000,
        formulas=[{"formula": "a"}],
    )

    assert result.data is not None
    body = MockServer.body(datadog_api.last)
    assert body["data"]["type"] == "scalar_request"
    assert body["data"]["attributes"]["from"] == 1000
    assert body["data"]["attributes"]["formulas"] == [{"formula": "a"}]


def test_list_metrics(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v2/metrics", json={"data": [{"id": "m1", "type": "metrics"}]}
    )

    result = list_metrics(
        filter_configured=True,
        filter_tags="env:prod",
        page_size=100,
        page_cursor="c1",
    )

    assert result.data is not None
    p = datadog_api.last.url.params
    assert p["filter[configured]"] == "true"
    assert p["filter[tags]"] == "env:prod"
    assert p["page[size]"] == "100"
    assert p["page[cursor]"] == "c1"


def test_list_downtimes(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v2/downtime", json={"data": [{"id": "d1", "type": "downtime"}]}
    )

    result = list_downtimes(
        current_only=True, include="created_by", offset=20, limit=50
    )

    assert result.data is not None
    assert result.data[0].id == "d1"
    p = datadog_api.last.url.params
    assert p["current_only"] == "true"
    assert p["include"] == "created_by"
    assert p["page[offset]"] == "20"
    assert p["page[limit]"] == "50"


def test_get_downtime(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v2/downtime/d1", json={"data": {"id": "d1", "type": "downtime"}}
    )

    result = get_downtime("d1", include="created_by")

    assert result.data is not None
    assert result.data.id == "d1"
    assert datadog_api.last.url.params["include"] == "created_by"


def test_list_slos(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v1/slo", json={"data": [{"id": "slo1", "name": "uptime"}]}
    )

    result = list_slos(
        ids="slo1,slo2",
        query="service:api",
        tags_query="env:prod",
        metrics_query="avg:x",
        limit=50,
        offset=10,
    )

    assert result.data is not None
    assert result.data[0].id == "slo1"
    p = datadog_api.last.url.params
    assert p["ids"] == "slo1,slo2"
    assert p["query"] == "service:api"
    assert p["tags_query"] == "env:prod"
    assert p["metrics_query"] == "avg:x"
    assert p["limit"] == "50"
    assert p["offset"] == "10"


def test_get_slo(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v1/slo/slo1", json={"data": {"id": "slo1", "name": "x"}}
    )

    result = get_slo("slo1", with_configured_alert_ids=True)

    assert result.data is not None
    assert result.data.id == "slo1"
    assert datadog_api.last.url.params["with_configured_alert_ids"] == "true"


def test_list_dashboards(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v1/dashboard",
        json={"dashboards": [{"id": "dash1", "title": "Ops"}]},
    )

    result = list_dashboards(
        filter_shared=True, filter_deleted=False, count=20, start=0
    )

    assert result.dashboards is not None
    assert result.dashboards[0].id == "dash1"
    p = datadog_api.last.url.params
    assert p["filter[shared]"] == "true"
    assert p["filter[deleted]"] == "false"
    assert p["count"] == "20"
    assert p["start"] == "0"


def test_get_dashboard(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v1/dashboard/dash1", json={"id": "dash1", "title": "Ops"}
    )

    result = get_dashboard("dash1")

    assert result.id == "dash1"
    assert datadog_api.last.url.path == "/api/v1/dashboard/dash1"


def test_list_catalog_entities(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/catalog/entity",
        json={"data": [{"id": "svc1", "type": "entity"}]},
    )

    result = list_catalog_entities(
        filter_name="checkout",
        filter_kind="service",
        filter_ref="service:checkout",
        include="schema",
        page_limit=50,
        page_offset=10,
    )

    assert result.data is not None
    assert result.data[0].id == "svc1"
    p = datadog_api.last.url.params
    assert p["filter[name]"] == "checkout"
    assert p["filter[kind]"] == "service"
    assert p["filter[ref]"] == "service:checkout"
    assert p["include"] == "schema"
    assert p["page[limit]"] == "50"
    assert p["page[offset]"] == "10"


def test_get_service_definition(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/services/definitions/checkout",
        json={"data": {"id": "checkout", "type": "service-definition"}},
    )

    result = get_service_definition("checkout")

    assert result.data is not None
    assert result.data.id == "checkout"
    assert datadog_api.last.url.path == "/api/v2/services/definitions/checkout"


def test_list_incidents(datadog_api: MockServer):
    datadog_api.add(
        "GET", "/api/v2/incidents", json={"data": [{"id": "inc1", "type": "incidents"}]}
    )

    result = list_incidents(include="users", size=20, offset=10)

    assert result.data is not None
    assert result.data[0].id == "inc1"
    p = datadog_api.last.url.params
    assert p["include"] == "users"
    assert p["page[size]"] == "20"
    assert p["page[offset]"] == "10"


def test_get_incident(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/incidents/inc1",
        json={"data": {"id": "inc1", "type": "incidents"}},
    )

    result = get_incident("inc1", include="attachments")

    assert result.data is not None
    assert result.data.id == "inc1"
    assert datadog_api.last.url.params["include"] == "attachments"


def test_search_incidents(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/incidents/search",
        json={"data": {"type": "incidents_search_results", "attributes": {"total": 1}}},
    )

    result = search_incidents(
        "state:active", include="users", sort="created", size=20, offset=10
    )

    assert result.data is not None
    assert result.data.attributes is not None
    assert result.data.attributes.total == 1
    p = datadog_api.last.url.params
    assert p["query"] == "state:active"
    assert p["include"] == "users"
    assert p["sort"] == "created"
    assert p["page[size]"] == "20"
    assert p["page[offset]"] == "10"


def test_list_synthetic_tests(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v1/synthetics/tests",
        json={"tests": [{"public_id": "abc-def-ghi", "name": "uptime"}]},
    )

    result = list_synthetic_tests(page_size=10, page_number=0)

    assert result.tests is not None
    assert result.tests[0].public_id == "abc-def-ghi"
    p = datadog_api.last.url.params
    assert p["page_size"] == "10"
    assert p["page_number"] == "0"


def test_get_api_test_results(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v1/synthetics/tests/abc/results",
        json={"last_timestamp_fetched": 1600000000, "results": [{"result_id": "r1"}]},
    )

    result = get_api_test_results(
        "abc", from_ts=1600000000, to_ts=1600003600, probe_dc=["aws:us-east-1"]
    )

    assert result.results is not None
    assert result.results[0].result_id == "r1"
    p = datadog_api.last.url.params
    assert p["from_ts"] == "1600000000"
    assert p["to_ts"] == "1600003600"
    assert p.get_list("probe_dc") == ["aws:us-east-1"]


def test_get_browser_test_results(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v1/synthetics/tests/browser/abc/results",
        json={"last_timestamp_fetched": 1600000000, "results": [{"result_id": "r1"}]},
    )

    result = get_browser_test_results(
        "abc", from_ts=1600000000, to_ts=1600003600, probe_dc=["aws:us-east-1"]
    )

    assert result.results is not None
    assert result.results[0].result_id == "r1"
    p = datadog_api.last.url.params
    assert p["from_ts"] == "1600000000"
    assert p.get_list("probe_dc") == ["aws:us-east-1"]


def test_search_rum_events(datadog_api: MockServer):
    datadog_api.add(
        "POST",
        "/api/v2/rum/events/search",
        json={
            "data": [
                {"id": "r1", "type": "rum", "attributes": {"service": "web-store"}}
            ],
            "meta": {"page": {"after": "cur"}},
        },
    )

    result = search_rum_events(
        "@type:error", from_="now-1h", to="now", sort="-timestamp", limit=10, cursor="p"
    )

    assert result.data is not None
    assert result.data[0].id == "r1"
    body = MockServer.body(datadog_api.last)
    assert body["filter"] == {"query": "@type:error", "from": "now-1h", "to": "now"}
    assert body["page"] == {"limit": 10, "cursor": "p"}
    assert body["sort"] == "-timestamp"


def test_aggregate_rum_events(datadog_api: MockServer):
    datadog_api.add(
        "POST",
        "/api/v2/rum/analytics/aggregate",
        json={
            "data": {"buckets": [{"by": {"service": "web"}, "computes": {"c0": 5.0}}]}
        },
    )

    result = aggregate_rum_events(
        "@type:view",
        compute=[{"aggregation": "count"}],
        from_="now-1h",
        to="now",
        group_by=[{"facet": "@view.name"}],
    )

    assert result.data is not None
    assert result.data.buckets is not None
    assert result.data.buckets[0].computes == {"c0": 5.0}
    body = MockServer.body(datadog_api.last)
    assert body["compute"] == [{"aggregation": "count"}]
    assert body["group_by"] == [{"facet": "@view.name"}]


def test_get_slo_status(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/slo/slo1/status",
        json={"data": {"id": "slo1", "type": "slo_status"}},
    )

    result = get_slo_status(
        "slo1", from_ts=1600000000, to_ts=1600003600, disable_corrections=True
    )

    assert result.data is not None
    p = datadog_api.last.url.params
    assert datadog_api.last.url.path == "/api/v2/slo/slo1/status"
    assert p["from_ts"] == "1600000000"
    assert p["to_ts"] == "1600003600"
    assert p["disable_corrections"] == "true"


def test_list_containers(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/containers",
        json={
            "data": [
                {"id": "c1", "type": "container", "attributes": {"name": "checkout"}}
            ]
        },
    )

    result = list_containers(
        filter_tags="env:prod", sort="-name", page_size=50, page_cursor="c"
    )

    assert result.data is not None
    assert result.data[0].id == "c1"
    p = datadog_api.last.url.params
    assert p["filter[tags]"] == "env:prod"
    assert p["sort"] == "-name"
    assert p["page[size]"] == "50"
    assert p["page[cursor]"] == "c"


def test_list_processes(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v2/processes",
        json={"data": [{"id": "p1", "type": "process", "attributes": {"pid": 1234}}]},
    )

    result = list_processes(
        search="python",
        tags="host:web-1",
        from_=1600000000,
        to=1600003600,
        limit=50,
        cursor="c",
    )

    assert result.data is not None
    assert result.data[0].id == "p1"
    p = datadog_api.last.url.params
    assert p["search"] == "python"
    assert p["tags"] == "host:web-1"
    assert p["from"] == "1600000000"
    assert p["to"] == "1600003600"
    assert p["page[limit]"] == "50"
    assert p["page[cursor]"] == "c"


def test_get_log_indexes(datadog_api: MockServer):
    datadog_api.add(
        "GET",
        "/api/v1/logs/config/indexes",
        json={
            "indexes": [
                {
                    "name": "main",
                    "num_retention_days": 15,
                    "num_flex_logs_retention_days": 360,
                    "filter": {"query": "*"},
                    "daily_limit": 300000000,
                }
            ]
        },
    )

    result = get_log_indexes()

    assert result.indexes is not None
    assert result.indexes[0].name == "main"
    assert result.indexes[0].num_retention_days == 15
    assert result.indexes[0].filter is not None
    assert result.indexes[0].filter.query == "*"

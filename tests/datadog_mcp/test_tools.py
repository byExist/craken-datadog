"""Tests for datadog_mcp.tools — the MCP tool layer (thin delegation to client)."""

from unittest.mock import call

from pytest_mock import MockerFixture

from datadog_mcp import client, tools


def test_search_logs_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "search_logs", return_value=sentinel)

    assert (
        tools.search_logs(
            "q", from_="now-1h", to="now", sort="-timestamp", limit=5, cursor="c"
        )
        is sentinel
    )
    assert fn.call_args == call(
        "q", from_="now-1h", to="now", sort="-timestamp", limit=5, cursor="c"
    )


def test_aggregate_logs_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "aggregate_logs", return_value=sentinel)

    assert (
        tools.aggregate_logs(
            "q",
            [{"aggregation": "count"}],
            from_="now-1h",
            to="now",
            group_by=[{"facet": "x"}],
        )
        is sentinel
    )
    assert fn.call_args == call(
        "q",
        [{"aggregation": "count"}],
        from_="now-1h",
        to="now",
        group_by=[{"facet": "x"}],
    )


def test_list_hosts_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_hosts", return_value=sentinel)

    assert (
        tools.list_hosts(
            filter_="env:prod",
            sort_field="cpu",
            sort_dir="desc",
            start=0,
            count=50,
            from_=1,
            include_muted_hosts_data=True,
            include_hosts_metadata=False,
        )
        is sentinel
    )
    assert fn.call_args == call(
        filter_="env:prod",
        sort_field="cpu",
        sort_dir="desc",
        start=0,
        count=50,
        from_=1,
        include_muted_hosts_data=True,
        include_hosts_metadata=False,
    )


def test_get_host_totals_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_host_totals", return_value=sentinel)

    assert tools.get_host_totals(from_=1) is sentinel
    assert fn.call_args == call(from_=1)


def test_list_events_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_events", return_value=sentinel)

    assert (
        tools.list_events(
            query="status:error",
            from_="now-1h",
            to="now",
            sort="-timestamp",
            limit=5,
            cursor="c",
        )
        is sentinel
    )
    assert fn.call_args == call(
        query="status:error",
        from_="now-1h",
        to="now",
        sort="-timestamp",
        limit=5,
        cursor="c",
    )


def test_get_event_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_event", return_value=sentinel)

    assert tools.get_event("e1") is sentinel
    assert fn.call_args == call("e1")


def test_search_spans_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "search_spans", return_value=sentinel)

    assert (
        tools.search_spans(
            "service:api",
            from_="now-1h",
            to="now",
            sort="-timestamp",
            limit=5,
            cursor="c",
        )
        is sentinel
    )
    assert fn.call_args == call(
        "service:api", from_="now-1h", to="now", sort="-timestamp", limit=5, cursor="c"
    )


def test_aggregate_spans_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "aggregate_spans", return_value=sentinel)

    assert (
        tools.aggregate_spans(
            "service:api",
            [{"aggregation": "count"}],
            from_="now-1h",
            to="now",
            group_by=[{"facet": "x"}],
        )
        is sentinel
    )
    assert fn.call_args == call(
        "service:api",
        [{"aggregation": "count"}],
        from_="now-1h",
        to="now",
        group_by=[{"facet": "x"}],
    )


def test_get_trace_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_trace", return_value=sentinel)

    assert tools.get_trace("abc123") is sentinel
    assert fn.call_args == call("abc123")


def test_get_pruned_trace_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_pruned_trace", return_value=sentinel)

    assert tools.get_pruned_trace("abc123") is sentinel
    assert fn.call_args == call("abc123")


def test_list_monitors_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_monitors", return_value=sentinel)

    assert (
        tools.list_monitors(
            group_states="alert",
            name="cpu",
            tags="env:prod",
            monitor_tags="team:sre",
            with_downtimes=True,
            page=1,
            page_size=50,
        )
        is sentinel
    )
    assert fn.call_args == call(
        group_states="alert",
        name="cpu",
        tags="env:prod",
        monitor_tags="team:sre",
        with_downtimes=True,
        page=1,
        page_size=50,
    )


def test_get_monitor_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_monitor", return_value=sentinel)

    assert tools.get_monitor(42, group_states="alert", with_downtimes=False) is sentinel
    assert fn.call_args == call(42, group_states="alert", with_downtimes=False)


def test_search_monitors_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "search_monitors", return_value=sentinel)

    assert (
        tools.search_monitors("type:metric", page=1, per_page=10, sort="name,asc")
        is sentinel
    )
    assert fn.call_args == call("type:metric", page=1, per_page=10, sort="name,asc")


def test_query_timeseries_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "query_timeseries", return_value=sentinel)

    assert (
        tools.query_timeseries(
            [{"query": "avg:x{*}"}], from_=1000, to=2000, formulas=[{"formula": "a"}]
        )
        is sentinel
    )
    assert fn.call_args == call(
        [{"query": "avg:x{*}"}], from_=1000, to=2000, formulas=[{"formula": "a"}]
    )


def test_query_scalar_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "query_scalar", return_value=sentinel)

    assert (
        tools.query_scalar(
            [{"query": "avg:x{*}"}], from_=1000, to=2000, formulas=[{"formula": "a"}]
        )
        is sentinel
    )
    assert fn.call_args == call(
        [{"query": "avg:x{*}"}], from_=1000, to=2000, formulas=[{"formula": "a"}]
    )


def test_list_metrics_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_metrics", return_value=sentinel)

    assert (
        tools.list_metrics(
            filter_configured=True,
            filter_tags="env:prod",
            page_size=100,
            page_cursor="c",
        )
        is sentinel
    )
    assert fn.call_args == call(
        filter_configured=True, filter_tags="env:prod", page_size=100, page_cursor="c"
    )


def test_list_downtimes_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_downtimes", return_value=sentinel)

    assert (
        tools.list_downtimes(
            current_only=True, include="created_by", offset=20, limit=50
        )
        is sentinel
    )
    assert fn.call_args == call(
        current_only=True, include="created_by", offset=20, limit=50
    )


def test_get_downtime_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_downtime", return_value=sentinel)

    assert tools.get_downtime("d1", include="created_by") is sentinel
    assert fn.call_args == call("d1", include="created_by")


def test_list_slos_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_slos", return_value=sentinel)

    assert (
        tools.list_slos(
            ids="a,b",
            query="service:api",
            tags_query="env:prod",
            metrics_query="avg:x",
            limit=50,
            offset=10,
        )
        is sentinel
    )
    assert fn.call_args == call(
        ids="a,b",
        query="service:api",
        tags_query="env:prod",
        metrics_query="avg:x",
        limit=50,
        offset=10,
    )


def test_get_slo_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_slo", return_value=sentinel)

    assert tools.get_slo("slo1", with_configured_alert_ids=True) is sentinel
    assert fn.call_args == call("slo1", with_configured_alert_ids=True)


def test_list_dashboards_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_dashboards", return_value=sentinel)

    assert (
        tools.list_dashboards(
            filter_shared=True, filter_deleted=False, count=20, start=0
        )
        is sentinel
    )
    assert fn.call_args == call(
        filter_shared=True, filter_deleted=False, count=20, start=0
    )


def test_get_dashboard_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_dashboard", return_value=sentinel)

    assert tools.get_dashboard("dash1") is sentinel
    assert fn.call_args == call("dash1")


def test_list_catalog_entities_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_catalog_entities", return_value=sentinel)

    assert (
        tools.list_catalog_entities(
            filter_name="checkout",
            filter_kind="service",
            filter_ref="service:checkout",
            include="schema",
            page_limit=50,
            page_offset=10,
        )
        is sentinel
    )
    assert fn.call_args == call(
        filter_name="checkout",
        filter_kind="service",
        filter_ref="service:checkout",
        include="schema",
        page_limit=50,
        page_offset=10,
    )


def test_get_service_definition_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_service_definition", return_value=sentinel)

    assert tools.get_service_definition("checkout") is sentinel
    assert fn.call_args == call("checkout")


def test_list_incidents_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_incidents", return_value=sentinel)

    assert tools.list_incidents(include="users", size=20, offset=10) is sentinel
    assert fn.call_args == call(include="users", size=20, offset=10)


def test_get_incident_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_incident", return_value=sentinel)

    assert tools.get_incident("inc1", include="attachments") is sentinel
    assert fn.call_args == call("inc1", include="attachments")


def test_search_incidents_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "search_incidents", return_value=sentinel)

    assert (
        tools.search_incidents(
            "state:active", include="users", sort="created", size=20, offset=10
        )
        is sentinel
    )
    assert fn.call_args == call(
        "state:active", include="users", sort="created", size=20, offset=10
    )


def test_list_synthetic_tests_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_synthetic_tests", return_value=sentinel)

    assert tools.list_synthetic_tests(page_size=10, page_number=0) is sentinel
    assert fn.call_args == call(page_size=10, page_number=0)


def test_get_api_test_results_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_api_test_results", return_value=sentinel)

    assert (
        tools.get_api_test_results(
            "abc", from_ts=1, to_ts=2, probe_dc=["aws:us-east-1"]
        )
        is sentinel
    )
    assert fn.call_args == call("abc", from_ts=1, to_ts=2, probe_dc=["aws:us-east-1"])


def test_get_browser_test_results_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_browser_test_results", return_value=sentinel)

    assert (
        tools.get_browser_test_results(
            "abc", from_ts=1, to_ts=2, probe_dc=["aws:us-east-1"]
        )
        is sentinel
    )
    assert fn.call_args == call("abc", from_ts=1, to_ts=2, probe_dc=["aws:us-east-1"])


def test_search_rum_events_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "search_rum_events", return_value=sentinel)

    assert (
        tools.search_rum_events(
            "@type:error",
            from_="now-1h",
            to="now",
            sort="-timestamp",
            limit=5,
            cursor="c",
        )
        is sentinel
    )
    assert fn.call_args == call(
        "@type:error", from_="now-1h", to="now", sort="-timestamp", limit=5, cursor="c"
    )


def test_aggregate_rum_events_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "aggregate_rum_events", return_value=sentinel)

    assert (
        tools.aggregate_rum_events(
            "@type:view",
            [{"aggregation": "count"}],
            from_="now-1h",
            to="now",
            group_by=[{"facet": "x"}],
        )
        is sentinel
    )
    assert fn.call_args == call(
        "@type:view",
        [{"aggregation": "count"}],
        from_="now-1h",
        to="now",
        group_by=[{"facet": "x"}],
    )


def test_get_slo_status_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "get_slo_status", return_value=sentinel)

    assert (
        tools.get_slo_status("slo1", from_ts=1, to_ts=2, disable_corrections=True)
        is sentinel
    )
    assert fn.call_args == call("slo1", from_ts=1, to_ts=2, disable_corrections=True)


def test_list_containers_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_containers", return_value=sentinel)

    assert (
        tools.list_containers(
            filter_tags="env:prod", sort="-name", page_size=50, page_cursor="c"
        )
        is sentinel
    )
    assert fn.call_args == call(
        filter_tags="env:prod", sort="-name", page_size=50, page_cursor="c"
    )


def test_list_processes_delegates(mocker: MockerFixture):
    sentinel = object()
    fn = mocker.patch.object(client, "list_processes", return_value=sentinel)

    assert (
        tools.list_processes(
            search="python", tags="host:web-1", from_=1, to=2, limit=50, cursor="c"
        )
        is sentinel
    )
    assert fn.call_args == call(
        search="python", tags="host:web-1", from_=1, to=2, limit=50, cursor="c"
    )

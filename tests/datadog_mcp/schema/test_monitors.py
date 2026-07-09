import payloads

from datadog_mcp.schema.monitors import (
    CheckCanDeleteMonitorResponse,
    Monitor,
    MonitorSearchResponse,
)


def test_monitor_full():
    m = Monitor.model_validate(
        {
            "id": 123,
            "name": "high cpu",
            "type": "metric alert",
            "query": "avg(...)>0.9",
            "overall_state": "Alert",
            "tags": ["env:prod"],
            "multi": True,
            "priority": 2,
            "creator": {"email": "a@b.com", "handle": "h", "name": "n"},
            "matching_downtimes": [{"id": 1, "start": 100, "end": 200, "scope": ["*"]}],
            "options": {
                "thresholds": {"critical": 0.9, "warning": 0.75},
                "notify_no_data": True,
                "renotify_statuses": ["alert", "warn"],
                "on_missing_data": "show_and_notify_no_data",
                "scheduling_options": {"evaluation_window": {"hour_starts": 0}},
                "variables": [{"data_source": "metrics", "name": "q", "query": "x"}],
            },
            "state": {"groups": {"host:a": {"status": "Alert", "name": "host:a"}}},
            "assets": [payloads.monitor_asset(resource_type="notebook")],
        }
    )
    assert m.id == 123
    assert m.type == "metric alert"
    assert m.overall_state == "Alert"
    assert m.options is not None
    assert m.options.thresholds is not None
    assert m.options.thresholds.critical == 0.9
    assert m.options.renotify_statuses == ["alert", "warn"]
    assert m.options.variables == [
        {"data_source": "metrics", "name": "q", "query": "x"}
    ]
    assert m.state is not None
    assert m.state.groups is not None
    assert m.state.groups["host:a"].status == "Alert"
    assert m.creator is not None
    assert m.creator.email == "a@b.com"
    assert m.matching_downtimes is not None
    assert m.matching_downtimes[0].id == 1
    assert m.assets is not None
    assert m.assets[0].category == "runbook"


def test_monitor_accepts_type_beyond_the_old_enum():
    # Datadog's monitor type set (22+ in the spec) grows over time; the field is
    # required and list_monitors parses each monitor, so an unlisted type like
    # "slo alert" or "audit alert" used to fail the whole call.
    m = Monitor.model_validate(
        {
            "id": 1,
            "name": "slo burn",
            "type": "slo alert",
            "query": "burn_rate(...)",
            "overall_state": "Alert",
        }
    )
    assert m.type == "slo alert"


def test_monitor_search_response():
    r = MonitorSearchResponse.model_validate(
        {
            "counts": {
                "status": [{"count": 3, "name": "Alert"}],
                "type": [{"count": 5, "name": "metric alert"}],
            },
            "metadata": {"page": 0, "page_count": 1, "per_page": 30, "total_count": 8},
            "monitors": [
                {
                    "id": 1,
                    "name": "m1",
                    "type": "log alert",
                    "status": "OK",
                    "tags": ["a"],
                }
            ],
        }
    )
    assert r.metadata is not None
    assert r.metadata.total_count == 8
    assert r.counts is not None
    assert r.counts.status is not None
    assert r.counts.status[0].count == 3
    assert r.counts.status[0].name == "Alert"
    assert r.monitors is not None
    assert r.monitors[0].type == "log alert"


def test_check_can_delete():
    r = CheckCanDeleteMonitorResponse.model_validate(
        {"data": {"ok": [1, 2, 3]}, "errors": {"5": ["in use"]}}
    )
    assert r.data is not None
    assert r.data.ok == [1, 2, 3]
    assert r.errors == {"5": ["in use"]}


def test_dump_drops_none():
    dumped = Monitor.model_validate(payloads.monitor(id=1, name="x")).model_dump()
    assert dumped == payloads.monitor(id=1, name="x")

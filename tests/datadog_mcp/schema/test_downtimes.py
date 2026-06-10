from datadog_mcp.schema.downtimes import (
    DowntimeMonitorIdentifierId,
    DowntimeScheduleRecurrencesResponse,
    ListDowntimesResponse,
    MonitorDowntimeMatchResponse,
)


def test_list_downtimes():
    r = ListDowntimesResponse.model_validate(
        {
            "data": [
                {
                    "id": "dt1",
                    "type": "downtime",
                    "attributes": {
                        "status": "active",
                        "scope": "env:prod",
                        "monitor_identifier": {"monitor_id": 123},
                        "schedule": {
                            "timezone": "UTC",
                            "recurrences": [{"rrule": "FREQ=DAILY", "start": "2020"}],
                        },
                        "notify_end_states": ["alert", "warn"],
                    },
                    "relationships": {"monitor": {"data": {"id": "123"}}},
                }
            ],
            "included": [
                {"type": "monitors", "id": "123", "attributes": {"name": "m"}}
            ],
            "meta": {"page": {"total_filtered_count": 1}},
        }
    )
    assert r.data is not None
    d = r.data[0]
    assert d.id == "dt1"
    assert d.attributes is not None
    assert d.attributes.status == "active"
    assert d.attributes.scope == "env:prod"
    assert isinstance(d.attributes.monitor_identifier, DowntimeMonitorIdentifierId)
    assert d.attributes.monitor_identifier.monitor_id == 123
    assert isinstance(d.attributes.schedule, DowntimeScheduleRecurrencesResponse)
    assert d.attributes.schedule.recurrences is not None
    assert d.attributes.schedule.recurrences[0].rrule == "FREQ=DAILY"
    assert d.relationships == {"monitor": {"data": {"id": "123"}}}
    assert r.included is not None
    assert r.included[0]["id"] == "123"
    assert r.meta is not None
    assert r.meta.page is not None
    assert r.meta.page.total_filtered_count == 1


def test_monitor_downtime_match():
    r = MonitorDowntimeMatchResponse.model_validate(
        {
            "data": [
                {
                    "id": "m1",
                    "type": "downtime_match",
                    "attributes": {
                        "scope": "env:prod",
                        "groups": ["host:a"],
                        "start": "2020",
                        "end": "2021",
                    },
                }
            ],
            "meta": {"page": {"total_filtered_count": 1}},
        }
    )
    assert r.data is not None
    assert r.data[0].attributes is not None
    assert r.data[0].attributes.scope == "env:prod"


def test_dump_drops_none():
    dumped = ListDowntimesResponse.model_validate(
        {"meta": {"page": {"total_filtered_count": 2}}}
    ).model_dump()
    assert dumped == {"meta": {"page": {"total_filtered_count": 2}}}

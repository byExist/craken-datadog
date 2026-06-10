from datetime import datetime

from datadog_mcp.schema.logs import LogsAggregateResponse, LogsListResponse


def test_logs_list_response_envelope():
    r = LogsListResponse.model_validate(
        {
            "data": [
                {
                    "id": "ABC",
                    "type": "log",
                    "attributes": {
                        "service": "agent",
                        "status": "INFO",
                        "message": "hi",
                        "host": "i-0123",
                        "tags": ["team:A"],
                        "timestamp": "2019-01-02T09:42:36.320Z",
                        "attributes": {"duration": 2345},
                    },
                }
            ],
            "links": {"next": "https://app.datadoghq.com/x"},
            "meta": {
                "elapsed": 132,
                "status": "done",
                "page": {"after": "cur=="},
                "warnings": [{"code": "unknown_index", "title": "t", "detail": "d"}],
            },
        }
    )
    assert r.data is not None
    log = r.data[0]
    assert log.id == "ABC"
    assert log.type == "log"
    assert log.attributes is not None
    assert log.attributes.service == "agent"
    assert isinstance(log.attributes.timestamp, datetime)
    assert log.attributes.attributes == {"duration": 2345}
    assert r.meta is not None
    assert r.meta.page is not None
    assert r.meta.page.after == "cur=="
    assert r.meta.status == "done"
    assert r.meta.warnings is not None
    assert r.meta.warnings[0].code == "unknown_index"
    assert r.links is not None
    assert r.links.next is not None
    assert r.links.next.startswith("https://")


def test_aggregate_response_union_values():
    r = LogsAggregateResponse.model_validate(
        {
            "data": {
                "buckets": [
                    {
                        "by": {"@state": "success"},
                        "computes": {
                            "c0": 19.0,
                            "c1": "abc",
                            "c2": [{"time": "2020-06-08T11:55:00Z", "value": 19}],
                        },
                    }
                ]
            },
            "meta": {"status": "done"},
        }
    )
    assert r.data is not None
    assert r.data.buckets is not None
    b = r.data.buckets[0]
    assert b.by == {"@state": "success"}
    assert b.computes is not None
    assert b.computes["c0"] == 19.0
    assert b.computes["c1"] == "abc"
    ts = b.computes["c2"]
    assert isinstance(ts, list)
    assert ts[0].value == 19


def test_dump_drops_none():
    dumped = LogsListResponse.model_validate({"meta": {"elapsed": 1}}).model_dump()
    assert dumped == {"meta": {"elapsed": 1}}

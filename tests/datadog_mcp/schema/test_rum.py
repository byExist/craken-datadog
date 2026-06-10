from datadog_mcp.schema.rum import RUMAnalyticsAggregateResponse, RUMEventsResponse


def test_rum_events_response():
    r = RUMEventsResponse.model_validate(
        {
            "data": [
                {
                    "id": "AAAA",
                    "type": "rum",
                    "attributes": {
                        "service": "web-store",
                        "tags": ["env:prod"],
                        "timestamp": "2026-06-11T09:15:00.000Z",
                        "attributes": {"type": "error", "error": {"message": "boom"}},
                    },
                }
            ],
            "links": {"next": "https://app/next"},
            "meta": {"elapsed": 7, "status": "done", "page": {"after": "cur"}},
        }
    )
    assert r.data is not None
    e = r.data[0]
    assert e.id == "AAAA"
    assert e.attributes is not None
    assert e.attributes.service == "web-store"
    assert e.attributes.attributes == {"type": "error", "error": {"message": "boom"}}
    assert r.meta is not None
    assert r.meta.page is not None
    assert r.meta.page.after == "cur"


def test_rum_aggregate_union():
    r = RUMAnalyticsAggregateResponse.model_validate(
        {
            "data": {
                "buckets": [
                    {
                        "by": {"service": "web-store"},
                        "computes": {
                            "c0": 9.0,
                            "c1": "x",
                            "c2": [{"time": "2026-06-11T09:00:00Z", "value": 2}],
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
    assert b.computes is not None
    assert b.computes["c0"] == 9.0
    ts = b.computes["c2"]
    assert isinstance(ts, list)
    assert ts[0].value == 2


def test_dump_drops_none():
    dumped = RUMEventsResponse.model_validate({"meta": {"elapsed": 1}}).model_dump()
    assert dumped == {"meta": {"elapsed": 1}}

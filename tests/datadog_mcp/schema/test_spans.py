from datadog_mcp.schema.spans import (
    SpansAggregateResponse,
    SpansListResponse,
    SpansMetricsResponse,
)


def test_spans_list_response():
    r = SpansListResponse.model_validate(
        {
            "data": [
                {
                    "id": "s1",
                    "type": "spans",
                    "attributes": {
                        "service": "api",
                        "resource_name": "GET /x",
                        "trace_id": "t1",
                        "span_id": "sp1",
                        "type": "web",
                        "tags": ["env:prod"],
                        "custom": {"k": "v"},
                        "single_span": False,
                    },
                }
            ],
            "links": {"next": "https://x"},
            "meta": {
                "elapsed": 5,
                "status": "done",
                "page": {"after": "c"},
                "warnings": [{"code": "w", "title": "t", "detail": "d"}],
            },
        }
    )
    assert r.data is not None
    sp = r.data[0]
    assert sp.id == "s1"
    assert sp.attributes is not None
    assert sp.attributes.service == "api"
    assert sp.attributes.resource_name == "GET /x"
    assert r.meta is not None
    assert r.meta.status == "done"


def test_spans_aggregate_union():
    r = SpansAggregateResponse.model_validate(
        {
            "data": [
                {
                    "id": "b1",
                    "type": "bucket",
                    "attributes": {
                        "by": {"service": "api"},
                        "computes": {
                            "c0": 3.0,
                            "c1": "x",
                            "c2": [{"time": "2020-06-08T11:55:00Z", "value": 1}],
                        },
                    },
                }
            ],
            "meta": {"status": "done"},
        }
    )
    assert r.data is not None
    b = r.data[0]
    assert b.attributes is not None
    assert b.attributes.computes is not None
    assert b.attributes.computes["c0"] == 3.0
    ts = b.attributes.computes["c2"]
    assert isinstance(ts, list)
    assert ts[0].value == 1


def test_spans_metrics_response():
    r = SpansMetricsResponse.model_validate(
        {
            "data": [
                {
                    "id": "m1",
                    "type": "spans_metrics",
                    "attributes": {
                        "compute": {
                            "aggregation_type": "count",
                            "include_percentiles": False,
                        },
                        "filter": {"query": "*"},
                        "group_by": [{"path": "service", "tag_name": "svc"}],
                    },
                }
            ]
        }
    )
    assert r.data is not None
    m = r.data[0]
    assert m.attributes is not None
    assert m.attributes.compute is not None
    assert m.attributes.compute.aggregation_type == "count"
    assert m.attributes.group_by is not None
    assert m.attributes.group_by[0].tag_name == "svc"


def test_dump_drops_none():
    dumped = SpansListResponse.model_validate({"meta": {"elapsed": 1}}).model_dump()
    assert dumped == {"meta": {"elapsed": 1}}

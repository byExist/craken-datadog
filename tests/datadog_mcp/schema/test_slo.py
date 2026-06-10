from datadog_mcp.schema.slo import (
    SLOCountSpec,
    SLOListResponse,
    SLOResponse,
    SloStatusResponse,
    SLOTimeSliceSpec,
)


def test_slo_response_time_slice():
    r = SLOResponse.model_validate(
        {
            "data": {
                "id": "slo1",
                "name": "api availability",
                "type": "time_slice",
                "timeframe": "30d",
                "target_threshold": 99.9,
                "thresholds": [{"timeframe": "30d", "target": 99.9, "warning": 99.95}],
                "sli_specification": {
                    "time_slice": {
                        "comparator": ">=",
                        "threshold": 0.99,
                        "query_interval_seconds": 300,
                        "query": {
                            "formulas": [{"formula": "query1"}],
                            "queries": [
                                {
                                    "data_source": "metrics",
                                    "name": "query1",
                                    "query": "avg:x{*}",
                                }
                            ],
                        },
                    }
                },
                "monitor_ids": [1, 2],
            }
        }
    )
    assert r.data is not None
    assert r.data.type == "time_slice"
    assert r.data.thresholds is not None
    assert r.data.thresholds[0].target == 99.9
    assert isinstance(r.data.sli_specification, SLOTimeSliceSpec)
    ts = r.data.sli_specification.time_slice
    assert ts is not None
    assert ts.comparator == ">="
    assert ts.query_interval_seconds == 300
    assert ts.query is not None
    assert ts.query.queries is not None
    assert ts.query.queries[0].data_source == "metrics"


def test_slo_list_count_spec():
    r = SLOListResponse.model_validate(
        {
            "data": [
                {
                    "id": "slo2",
                    "name": "errors",
                    "type": "metric",
                    "timeframe": "7d",
                    "sli_specification": {
                        "count": {
                            "good_events_formula": {"formula": "good"},
                            "total_events_formula": {"formula": "total"},
                            "queries": [
                                {"data_source": "metrics", "name": "good", "query": "x"}
                            ],
                        }
                    },
                }
            ],
            "metadata": {"page": {"total_count": 1, "total_filtered_count": 1}},
        }
    )
    assert r.data is not None
    slo = r.data[0]
    assert slo.name == "errors"
    assert isinstance(slo.sli_specification, SLOCountSpec)
    assert slo.sli_specification.count is not None
    assert r.metadata is not None
    assert r.metadata.page is not None
    assert r.metadata.page.total_count == 1


def test_slo_status():
    r = SloStatusResponse.model_validate(
        {
            "data": {
                "id": "slo1",
                "type": "slo_status",
                "attributes": {
                    "sli": 99.5,
                    "error_budget_remaining": 50.0,
                    "state": "ok",
                    "raw_error_budget_remaining": {"unit": "percent", "value": 50.0},
                },
            }
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    assert r.data.attributes.sli == 99.5
    assert r.data.attributes.raw_error_budget_remaining is not None
    assert r.data.attributes.raw_error_budget_remaining.value == 50.0


def test_dump_drops_none():
    dumped = SLOResponse.model_validate({"errors": ["boom"]}).model_dump()
    assert dumped == {"errors": ["boom"]}

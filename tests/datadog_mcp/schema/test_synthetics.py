from datadog_mcp.schema.synthetics import (
    SyntheticsGetAPITestLatestResultsResponse,
    SyntheticsListTestsResponse,
)


def test_list_tests():
    r = SyntheticsListTestsResponse.model_validate(
        {
            "tests": [
                {
                    "public_id": "abc-def-ghi",
                    "name": "homepage uptime",
                    "type": "api",
                    "subtype": "http",
                    "status": "live",
                    "monitor_id": 123,
                    "locations": ["aws:us-east-1"],
                    "tags": ["env:prod"],
                    "config": {
                        "assertions": [{"type": "statusCode", "operator": "is"}]
                    },
                    "options": {"tick_every": 60},
                }
            ]
        }
    )
    assert r.tests is not None
    t = r.tests[0]
    assert t.public_id == "abc-def-ghi"
    assert t.type == "api"
    assert t.subtype == "http"
    assert t.status == "live"
    assert t.monitor_id == 123
    assert t.locations == ["aws:us-east-1"]
    assert t.config == {"assertions": [{"type": "statusCode", "operator": "is"}]}
    assert t.options == {"tick_every": 60}


def test_api_latest_results():
    r = SyntheticsGetAPITestLatestResultsResponse.model_validate(
        {
            "last_timestamp_fetched": 1600000000,
            "results": [
                {
                    "result_id": "r1",
                    "probe_dc": "aws:us-east-1",
                    "check_time": 1600000000.0,
                    "status": 0,
                    "result": {"passed": True, "timings": {"total": 123.4}},
                }
            ],
        }
    )
    assert r.results is not None
    res = r.results[0]
    assert res.status == 0
    assert res.result is not None
    assert res.result.passed is True
    assert res.result.timings == {"total": 123.4}


def test_dump_drops_none():
    dumped = SyntheticsListTestsResponse.model_validate(
        {"tests": [{"name": "t"}]}
    ).model_dump()
    assert dumped == {"tests": [{"name": "t"}]}

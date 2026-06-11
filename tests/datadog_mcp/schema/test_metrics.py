from datadog_mcp.schema.metrics import (
    DataScalarColumn,
    GroupScalarColumn,
    MetricAllTagsResponse,
    MetricsAndMetricTagConfigurationsResponse,
    MetricTagConfigurationResponse,
    ScalarFormulaQueryResponse,
    TimeseriesFormulaQueryResponse,
)


def test_timeseries_query():
    r = TimeseriesFormulaQueryResponse.model_validate(
        {
            "data": {
                "type": "timeseries_response",
                "attributes": {
                    "series": [
                        {
                            "group_tags": ["service:web"],
                            "query_index": 0,
                            "unit": [{"name": "byte", "family": "bytes"}, None],
                        }
                    ],
                    "times": [1000, 2000],
                    "values": [[1.5, 2.5]],
                },
            }
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    attrs = r.data.attributes
    assert attrs.series is not None
    assert attrs.series[0].group_tags == ["service:web"]
    assert attrs.series[0].unit is not None
    assert attrs.series[0].unit[0] is not None
    assert attrs.series[0].unit[0].name == "byte"
    assert attrs.series[0].unit[1] is None
    assert attrs.times == [1000, 2000]
    assert attrs.values == [[1.5, 2.5]]


def test_scalar_query_columns_union():
    r = ScalarFormulaQueryResponse.model_validate(
        {
            "data": {
                "type": "scalar_response",
                "attributes": {
                    "columns": [
                        {
                            "type": "number",
                            "name": "cpu",
                            "values": [1.0, 2.0],
                            "meta": {"unit": [{"name": "percent"}, None]},
                        },
                        {
                            "type": "group",
                            "name": "service",
                            "values": [["web"], ["db"]],
                        },
                    ]
                },
            }
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    cols = r.data.attributes.columns
    assert cols is not None
    assert isinstance(cols[0], DataScalarColumn)
    assert cols[0].values == [1.0, 2.0]
    assert cols[0].meta is not None
    assert cols[0].meta.unit is not None
    assert cols[0].meta.unit[0] is not None
    assert cols[0].meta.unit[0].name == "percent"
    assert cols[0].meta.unit[1] is None
    assert isinstance(cols[1], GroupScalarColumn)
    assert cols[1].values == [["web"], ["db"]]


def test_metrics_list_response():
    r = MetricsAndMetricTagConfigurationsResponse.model_validate(
        {
            "data": [{"id": "system.cpu", "type": "metrics"}],
            "links": {"self": "https://app/x", "next": "https://app/n"},
            "meta": {"pagination": {"next_cursor": "c", "type": "cursor_limit"}},
        }
    )
    assert r.data is not None
    assert len(r.data) == 1
    assert r.links is not None
    assert r.links.self_ == "https://app/x"
    assert r.meta is not None
    assert r.meta.pagination is not None
    assert r.meta.pagination.next_cursor == "c"


def test_tag_config_and_all_tags():
    r = MetricTagConfigurationResponse.model_validate(
        {
            "data": {
                "id": "system.cpu",
                "type": "manage_tags",
                "attributes": {
                    "metric_type": "gauge",
                    "tags": ["env"],
                    "include_percentiles": True,
                    "aggregations": [{"space": "avg", "time": "sum"}],
                },
            }
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    assert r.data.attributes.metric_type == "gauge"
    assert r.data.attributes.aggregations is not None
    assert r.data.attributes.aggregations[0].space == "avg"

    t = MetricAllTagsResponse.model_validate(
        {
            "data": {
                "id": "system.cpu",
                "type": "metrics",
                "attributes": {"tags": ["env:prod"], "ingested_tags": ["env"]},
            }
        }
    )
    assert t.data is not None
    assert t.data.attributes is not None
    assert t.data.attributes.tags == ["env:prod"]


def test_dump_drops_none():
    dumped = TimeseriesFormulaQueryResponse.model_validate(
        {"errors": "boom"}
    ).model_dump()
    assert dumped == {"errors": "boom"}

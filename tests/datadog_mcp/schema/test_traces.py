import payloads

from datadog_mcp.schema.traces import PrunedTraceResponse, TraceResponse


def test_trace_response_camel_aliases():
    r = TraceResponse.model_validate(
        {
            "data": {
                "id": "t1",
                "type": "trace",
                "attributes": {
                    "is_truncated": False,
                    "spans": [
                        payloads.apm_trace_span(
                            spanID=1,
                            traceID=2,
                            parentID=0,
                            startTime=100,
                            endTime=200,
                            error=1,
                            service="api",
                            name="op",
                        )
                    ],
                },
            }
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    assert r.data.attributes.spans is not None
    s = r.data.attributes.spans[0]
    assert s.span_id == 1
    assert s.trace_id == 2
    assert s.start_time == 100
    assert s.error == 1


def test_pruned_trace_recursive_summarized_span():
    r = PrunedTraceResponse.model_validate(
        {
            "data": {
                "id": "p1",
                "type": "pruned_trace",
                "attributes": {
                    "is_truncated": True,
                    "size_bytes": 1024,
                    "summarized_trace": {
                        "traceId": "t1",
                        "root": payloads.summarized_span(
                            spanID=1,
                            durationSeconds=0.5,
                            name="root",
                            children=[payloads.summarized_span(spanID=2, name="child")],
                        ),
                    },
                },
            }
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    st = r.data.attributes.summarized_trace
    assert st is not None
    assert st.trace_id == "t1"
    assert st.root is not None
    assert st.root.span_id == 1
    assert st.root.duration_seconds == 0.5
    assert st.root.children is not None
    assert st.root.children[0].span_id == 2


def test_dump_drops_none():
    dumped = TraceResponse.model_validate(
        {"data": {"id": "t1", "type": "trace"}}
    ).model_dump()
    assert dumped == {"data": {"id": "t1", "type": "trace"}}

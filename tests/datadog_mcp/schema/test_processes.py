from datadog_mcp.schema.processes import ProcessSummariesResponse


def test_processes_response():
    r = ProcessSummariesResponse.model_validate(
        {
            "data": [
                {
                    "id": "p1",
                    "type": "process",
                    "attributes": {
                        "cmdline": "python app.py",
                        "host": "host-42",
                        "pid": 1234,
                        "ppid": 1,
                        "user": "app",
                        "tags": ["env:prod"],
                    },
                }
            ],
            "meta": {"page": {"after": "cur", "size": 25}},
        }
    )
    assert r.data is not None
    p = r.data[0]
    assert p.id == "p1"
    assert p.attributes is not None
    assert p.attributes.cmdline == "python app.py"
    assert p.attributes.pid == 1234
    assert p.attributes.host == "host-42"
    assert r.meta is not None
    assert r.meta.page is not None
    assert r.meta.page.after == "cur"


def test_dump_drops_none():
    dumped = ProcessSummariesResponse.model_validate(
        {"meta": {"page": {"size": 10}}}
    ).model_dump()
    assert dumped == {"meta": {"page": {"size": 10}}}

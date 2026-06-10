from datadog_mcp.schema.containers import ContainersResponse


def test_containers_response():
    r = ContainersResponse.model_validate(
        {
            "data": [
                {
                    "id": "abc123",
                    "type": "container",
                    "attributes": {
                        "name": "checkout",
                        "container_id": "abc123",
                        "host": "host-42",
                        "image_name": "checkout",
                        "image_tags": ["v12"],
                        "state": "running",
                        "tags": ["env:prod"],
                    },
                }
            ],
            "links": {"next": "https://app/next", "self": "https://app/self"},
            "meta": {
                "pagination": {"limit": 100, "next_cursor": "c", "type": "cursor_limit"}
            },
        }
    )
    assert r.data is not None
    c = r.data[0]
    assert c.id == "abc123"
    assert c.attributes is not None
    assert c.attributes.name == "checkout"
    assert c.attributes.image_tags == ["v12"]
    assert c.attributes.state == "running"
    assert r.links is not None
    assert r.links.self_ == "https://app/self"
    assert r.meta is not None
    assert r.meta.pagination is not None
    assert r.meta.pagination.next_cursor == "c"


def test_dump_drops_none():
    dumped = ContainersResponse.model_validate(
        {"meta": {"pagination": {"limit": 50}}}
    ).model_dump()
    assert dumped == {"meta": {"pagination": {"limit": 50}}}

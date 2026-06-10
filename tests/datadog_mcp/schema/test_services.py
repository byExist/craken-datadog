from datadog_mcp.schema.services import (
    ListEntityCatalogResponse,
    ServiceDefinitionGetResponse,
)


def test_list_entity_catalog():
    r = ListEntityCatalogResponse.model_validate(
        {
            "data": [
                {
                    "id": "svc-1",
                    "type": "entity",
                    "attributes": {
                        "apiVersion": "v3",
                        "kind": "service",
                        "name": "checkout",
                        "displayName": "Checkout",
                        "owner": "team-payments",
                        "tags": ["env:prod"],
                        "properties": {"tier": "1"},
                    },
                    "relationships": {"oncalls": {"data": [{"id": "oc1"}]}},
                }
            ],
            "included": [{"type": "oncall", "id": "oc1"}],
            "links": {"self": "https://app/x", "next": "https://app/n"},
            "meta": {"count": 1, "includeCount": 1},
        }
    )
    assert r.data is not None
    e = r.data[0]
    assert e.id == "svc-1"
    assert e.attributes is not None
    assert e.attributes.api_version == "v3"
    assert e.attributes.display_name == "Checkout"
    assert e.attributes.owner == "team-payments"
    assert e.attributes.properties == {"tier": "1"}
    assert e.relationships == {"oncalls": {"data": [{"id": "oc1"}]}}
    assert r.included is not None
    assert r.included[0]["id"] == "oc1"
    assert r.links is not None
    assert r.links.self_ == "https://app/x"
    assert r.meta is not None
    assert r.meta.include_count == 1


def test_service_definition_get():
    r = ServiceDefinitionGetResponse.model_validate(
        {
            "data": {
                "id": "checkout",
                "type": "service-definition",
                "attributes": {
                    "schema": {"schema-version": "v2.2", "kind": "service"},
                    "meta": {
                        "ingestion-source": "api",
                        "github-html-url": "https://github.com/x",
                        "warnings": [
                            {"message": "w", "instance-location": "/x"},
                        ],
                    },
                },
            }
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    assert r.data.attributes.schema_ == {"schema-version": "v2.2", "kind": "service"}
    assert r.data.attributes.meta is not None
    assert r.data.attributes.meta.ingestion_source == "api"
    assert r.data.attributes.meta.github_html_url == "https://github.com/x"
    assert r.data.attributes.meta.warnings is not None
    assert r.data.attributes.meta.warnings[0].instance_location == "/x"


def test_dump_drops_none():
    dumped = ListEntityCatalogResponse.model_validate(
        {"meta": {"count": 3}}
    ).model_dump()
    assert dumped == {"meta": {"count": 3}}

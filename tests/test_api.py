import json

from api.index import handle_api_route


def test_chatgpt_openapi_contract():
    status, content_type, body = handle_api_route("/openapi.json")
    document = json.loads(body)

    assert status == 200
    assert content_type == "application/json"
    assert document["openapi"] == "3.0.3"
    assert "/api/generate/video" in document["paths"]
    assert document["paths"]["/api/generate/video"]["post"]["operationId"] == "generateVideoProject"


def test_legacy_chatgpt_plugin_manifest():
    status, _, body = handle_api_route("/.well-known/ai-plugin.json")
    manifest = json.loads(body)

    assert status == 200
    assert manifest["name_for_model"] == "agentbroko"
    assert manifest["api"]["url"].endswith("/openapi.json")
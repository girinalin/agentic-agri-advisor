import requests

from tests.integration.test_server_e2e import BASE_URL


def test_collapsible_nav_elements_served(server_fixture) -> None:
    """Verify that the collapsible navigation components are successfully served in index.html."""
    res = requests.get(f"{BASE_URL}/agui/", timeout=10)
    assert res.status_code == 200
    html_content = res.text

    # Assert container elements exist
    assert 'id="left-nav"' in html_content
    assert 'class="left-nav-container"' in html_content
    assert 'id="left-nav-backdrop"' in html_content
    assert 'id="menu-toggle-btn"' in html_content
    assert 'id="left-nav-toggle-btn"' in html_content

    # Assert expert canvases exist
    assert 'id="console-canvas"' in html_content
    assert 'id="governance-canvas"' in html_content
    assert 'id="evaluation-canvas"' in html_content
    assert 'id="audit-canvas"' in html_content


def test_observability_logs_endpoint(server_fixture) -> None:
    """Verify that the observability logs retrieval API works."""
    payload = {
        "correlation_id": "test_corr_1",
        "event_type": "page_view",
        "screen": "console",
        "agent": "farmer_twin",
        "tool": "none",
        "route": "local",
        "safety_decision": "allowed",
        "latency": 0.12,
        "device_tier": "Chromebook",
    }
    res_post = requests.post(
        f"{BASE_URL}/api/observability/log", json=payload, timeout=10
    )
    assert res_post.status_code == 200

    res_get = requests.get(f"{BASE_URL}/api/observability/logs", timeout=10)
    assert res_get.status_code == 200
    logs_data = res_get.json()
    assert logs_data["status"] == "success"
    assert len(logs_data["logs"]) >= 1
    assert logs_data["logs"][0]["correlation_id"] == "test_corr_1"

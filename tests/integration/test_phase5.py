import requests

from tests.integration.test_server_e2e import BASE_URL, HEADERS


def test_phase5_routes(server_fixture) -> None:
    """Test all Phase 5 backend API endpoints on the server."""

    # 1. Test expert operations console queue
    res_queue = requests.get(f"{BASE_URL}/api/expert/queue", timeout=10)
    assert res_queue.status_code == 200
    assert res_queue.json()["status"] == "success"

    # Update case state
    action_payload = {
        "escalation_id": "esc_test_1",
        "state": "expert_replied",
        "expert_response": "Apply organic leaf mulch."
    }
    res_action = requests.post(f"{BASE_URL}/api/expert/action", json=action_payload, headers=HEADERS, timeout=10)
    assert res_action.status_code == 200
    assert res_action.json()["status"] == "success"

    # 2. Test outbreak intelligence endpoints
    res_outbreaks = requests.get(f"{BASE_URL}/api/outbreaks", timeout=10)
    assert res_outbreaks.status_code == 200
    assert res_outbreaks.json()["status"] == "success"

    verify_payload = {
        "outbreak_id": "out_1",
        "status": "confirmed"
    }
    res_verify = requests.post(f"{BASE_URL}/api/outbreaks/verify", json=verify_payload, headers=HEADERS, timeout=10)
    assert res_verify.status_code == 200
    assert res_verify.json()["status"] == "success"

    # 3. Test governance version rollback
    gov_payload = {
        "content_id": "gov_1"
    }
    res_rollback = requests.post(f"{BASE_URL}/api/governance/rollback", json=gov_payload, headers=HEADERS, timeout=10)
    assert res_rollback.status_code == 200
    assert res_rollback.json()["status"] == "success"

    # 4. Test observability event logging
    obs_payload = {
        "correlation_id": "corr_9999",
        "event_type": "screen_rendered",
        "screen": "expert_console",
        "agent": "dashboard_agent",
        "tool": "get_ui_schema",
        "route": "local",
        "safety_decision": "approved",
        "latency": 0.125,
        "device_tier": "Chromebook-tier"
    }
    res_obs = requests.post(f"{BASE_URL}/api/observability/log", json=obs_payload, headers=HEADERS, timeout=10)
    assert res_obs.status_code == 200
    assert res_obs.json()["status"] == "success"

    # 5. Test farmer privacy & consent routes
    priv_payload = {
        "user_id": "test_delete_user",
        "location_sharing": 1,
        "image_retention": 0,
        "voice_retention": 0,
        "expert_consultation_sharing": 1,
        "regional_outbreak_participation": 1,
        "analytics_participation": 1
      }
    res_priv = requests.post(f"{BASE_URL}/api/privacy/preferences", json=priv_payload, headers=HEADERS, timeout=10)
    assert res_priv.status_code == 200
    assert res_priv.json()["status"] == "success"

    # Export my data
    export_payload = {
        "user_id": "test_delete_user"
    }
    res_export = requests.post(f"{BASE_URL}/api/privacy/export", json=export_payload, headers=HEADERS, timeout=10)
    assert res_export.status_code == 200
    assert res_export.json()["status"] == "success"
    assert "data" in res_export.json()

    # Delete my data
    delete_payload = {
        "user_id": "test_delete_user"
    }
    res_delete = requests.post(f"{BASE_URL}/api/privacy/delete", json=delete_payload, headers=HEADERS, timeout=10)
    assert res_delete.status_code == 200
    assert res_delete.json()["status"] == "success"

    # 6. Test model evaluation offline dataset execution
    res_eval = requests.get(f"{BASE_URL}/api/evaluation/run", timeout=10)
    assert res_eval.status_code == 200
    assert res_eval.json()["status"] == "success"
    assert "routing_accuracy" in res_eval.json()["metrics"]

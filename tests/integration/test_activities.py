import requests

from tests.integration.test_server_e2e import BASE_URL, HEADERS


def test_activities_logging_flow(server_fixture) -> None:
    """Test retrieving and logging activities."""
    # 1. Fetch initial activities
    response = requests.get(f"{BASE_URL}/api/activities/planting_1", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    initial_count = len(data["activities"])
    assert initial_count >= 2  # act_1 and act_2 should be seeded

    # 2. Log a new activity
    payload = {
        "planting_id": "planting_1",
        "activity_type": "pest_treatment",
        "quantity": 5.0,
        "unit": "litres",
        "details": "Sprayed organic neem oil emulsion on tomato plants",
        "timestamp": "2026-07-02 12:00:00",
    }
    log_res = requests.post(
        f"{BASE_URL}/api/activities/log", json=payload, headers=HEADERS, timeout=10
    )
    assert log_res.status_code == 200
    log_data = log_res.json()
    assert log_data["status"] == "success"
    assert "activity_id" in log_data

    # 3. Verify the activity was added
    new_response = requests.get(f"{BASE_URL}/api/activities/planting_1", timeout=10)
    assert new_response.status_code == 200
    new_data = new_response.json()
    assert len(new_data["activities"]) == initial_count + 1

    # Check details of the added activity
    logged = new_data["activities"][0]  # sorted by timestamp desc, so should be first
    assert logged["activity_type"] == "pest_treatment"
    assert logged["quantity"] == 5.0
    assert logged["unit"] == "litres"
    assert logged["details"] == "Sprayed organic neem oil emulsion on tomato plants"

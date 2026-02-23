import json
import pytest

# Load test data
with open("data/users_test_data.json") as f:
    users_test_data = json.load(f)

@pytest.mark.parametrize("user_data", users_test_data)
def test_get_user_parametrized(api_client, user_data):
    user_id = user_data["id"]
    response = api_client.get(f"/users/{user_id}")

    #check status
    assert response.status_code == 200

    #Check json content
    data = response.json()
    assert data["name"] == user_data["expected_name"]
    assert data["email"] == user_data["expected_email"]
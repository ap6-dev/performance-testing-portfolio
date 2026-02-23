import json
import pytest
from src.utils.validation import validate_user_fields

# Load test data
with open("data/users_test_data.json") as f:
    users_test_data = json.load(f)



#Test to verify that list of users is not empty
def test_get_all_users(api_client):
    #Act
    response = api_client.get("/users")

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0



#Test for users specified in users_test_data
@pytest.mark.parametrize("user_data", users_test_data)
def test_get_user_parametrized(api_client, user_data):
    #Arrange
    user_id = user_data["id"]
    
    # Act
    response = api_client.get(f"/users/{user_id}")

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]



#Test that specified user data is valid
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_valid_id(api_client, user_id):
    #Act
    response = api_client.get(f"/users/{user_id}")

    #Assert
    assert response.status_code == 200
    data = response.json()

    #Reusable validation helper
    validate_user_fields(data)

    #Verify returned id matches the requested id
    assert data["id"] == user_id



#Negative test for specified invalid user id
@pytest.mark.parametrize("invalid_id", [0, -1, 999])
def test_get_user_invalid(api_client, invalid_id):
    #Act
    response = api_client.get(f"/users/{invalid_id}")
    
    #Assert
    assert response.status_code == 404



#Test creating a user
#Using JSONPlaceholder as endpoint
@pytest.mark.parametrize("user_payload", users_test_data)
def test_create_user(api_client, user_payload):
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    assert response.status_code in (200, 201)
   
    #Helper function to validate all fields
    validate_user_fields(data)
    
    #Only validate the fields that are reliable
    for key in ("name", "email"):
        assert data[key] == user_payload[key]
    
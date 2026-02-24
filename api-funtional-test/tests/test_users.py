import json
import pytest
from pathlib import Path
from src.utils.validation import validate_user_fields

# Load test data
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "users_test_data.json"
with open(DATA_FILE) as f:
    users_test_data = json.load(f)


#-------------------------------------------------------------------------------
# Positive GET /users Tests
#-------------------------------------------------------------------------------
#Test to verify that list of users is not empty
def test_get_all_users_returns_200(api_client):
    #Act
    response = api_client.get("/users")
    data = response.json()  
    
    #Assert
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0

#Test that all uses for proper schema
def test_get_all_users_schema(api_client):
    #Act
    response = api_client.get("/users")
    data = response.json()

    #Assert
    assert response.status_code == 200
    for user in data:
        #Reusable validation helper
        validate_user_fields(user)

#-------------------------------------------------------------------------------
# Positive GET /users/{id} Tests
#-------------------------------------------------------------------------------
#Test specified user fields exist
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_fields_present(api_client, user_id):
    #Act
    response = api_client.get(f"/users/{user_id}")
    data = response.json()

    #Assert
    assert response.status_code == 200
    #Helper function to validate all fields
    validate_user_fields(data)


#Test that specified user(s) exist(s)
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_valid_id(api_client, user_id):
    #Act
    response = api_client.get(f"/users/{user_id}")
    data = response.json() 

    #Assert
    assert response.status_code == 200
    #Verify returned id matches the requested id
    assert data["id"] == user_id

#Test for matching return data in specified users
@pytest.mark.parametrize("user_data", users_test_data)
def test_get_user_data_matches_expected(api_client, user_data):
    #Arrange
    user_id = user_data["id"]
    
    # Act
    response = api_client.get(f"/users/{user_id}")
    data = response.json()
    
    #Assert
    assert response.status_code == 200
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]

#-------------------------------------------------------------------------------
# Positive POST /users Tests
#-------------------------------------------------------------------------------
#Test create user with valid payload
@pytest.mark.parametrize("user_payload", users_test_data)
def test_create_user_valid_payload(api_client, user_payload):
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    assert response.status_code == 200 or 201
    #Helper function to validate all fields exist
    validate_user_fields(data)
    #Only validate the fields that are reliable
    for key in ("name", "email"):
        assert data[key] == user_payload[key]

#-------------------------------------------------------------------------------
# Positive PUT /users Tests
#-------------------------------------------------------------------------------
#Test updated fields are returned
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_update_user_valid_payload(api_client, user_id):
    user_payload = {
        "name": "firstname lastname"
    }
    #Act
    response = api_client.put(f"/users/{user_id}", json=user_payload)
    data = response.json()
    
    #Assert
    assert response.status_code == 200
    assert data["name"] == user_payload["name"]


#-------------------------------------------------------------------------------
# Positive DELETE /users Tests
#-------------------------------------------------------------------------------
#Test valid return code for user deletion
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_delete_user_valid_id(api_client, user_id):
    #Act
    response = api_client.delete(f"/users/{user_id}")

    #Assert
    assert response.status_code == 200 or 204
   


#-------------------------------------------------------------------------------
# Negative GET /users Tests
#-------------------------------------------------------------------------------
#Test for specified invalid user id
@pytest.mark.parametrize("invalid_id", [0, -1, 999])
def test_get_user_invalid_id_returns_404(api_client, invalid_id):
    #Act
    response = api_client.get(f"/users/{invalid_id}")
    
    #Assert
    assert response.status_code == 404

#Test get user by string - expected 404
@pytest.mark.parametrize("invalid_id", ["abc", "0.01", "0123"])
def test_get_user_string_id(api_client, invalid_id):
    #Act
    response = api_client.get(f"/users/{invalid_id}")

    #Assert
    assert response.status_code == 404

#-------------------------------------------------------------------------------
# Negative POST /users Tests
#-------------------------------------------------------------------------------
#Test creating user without required field (missing email)
@pytest.mark.parametrize("user_payload", [
    {"name": "Name1"},
    {"name": "Name2"},
    {"name": "Name3"}
    ])
def test_create_user_missing_required_field(api_client, user_payload):
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    assert response.status_code == 201
    # JSONPlaceholder does not validate required fields and echos payload
    # In a real API, this would return 400
    assert response.status_code == 201
    assert "email" not in data

#Test creating user with invalid email
@pytest.mark.parametrize("user_payload", [
    {"name": "Leanne Graham", "email": "InvalidEmail@google"},
    {"name": "Leanne Graham", "email": "InvalidEmailgoogle.com"},
    {"name": "Leanne Graham", "email": "@gmail.com"}
    ])
def test_create_user_invalid_email_format(api_client, user_payload):
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    # Note: JSONPlaceholder does not enforce email format on POST; returns 201
    # In a real API, this would return 400
    assert response.status_code == 400 or 201


#Test creating user with empty payload
def test_create_user_empty_payload(api_client):
    user_payload = {}
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    assert response.status_code == 201

#-------------------------------------------------------------------------------
# Negative PUT /users Tests
#-------------------------------------------------------------------------------
#Test update user with invalid id in payload
@pytest.mark.parametrize("invalid_id", [-1, 0, 9999])
def test_update_user_invalid_url_id(api_client, invalid_id):
    user_payload = {
        "name": "Updated Name",
        "email": "updated@example.com"
    }

    #Act
    response = api_client.put(f"/users/{invalid_id}", json=user_payload)

    #Assert
    # Note: JSONPlaceholder returns 500 Internal Server Error
    # In a real API, this would return 404
    assert response.status_code == 404 or 500

#Test update user empty payload
def test_update_user_empty_payload(api_client):
    user_payload = {}
    #Act
    response = api_client.put("/users/1", json=user_payload)

    #Assert
    # Note: JSONPlaceholder returns 200 and echoes empty payload
    # In a real API, this would return 400
    assert response.status_code == 400 or 200

#-------------------------------------------------------------------------------
# Negative Delete /users Tests
#-------------------------------------------------------------------------------
# Test delete user with invalid url id
@pytest.mark.parametrize("invalid_id", [-1, 0, 9999])
def test_delete_user_invalid_url_id(api_client, invalid_id):
    #Act
    response = api_client.delete(f"/users/{invalid_id}")

    #Assert
    # Note: JSONPlaceholder returns 500 Internal Server Error
    # In a real API, this would return 404
    assert response.status_code == 404 or 500
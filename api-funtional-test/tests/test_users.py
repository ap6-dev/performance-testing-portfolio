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

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

#Test that all uses for proper schema
def test_get_all_users_schema(api_client):
    #Act
    response = api_client.get("/users")

    #Assert
    assert response.status_code == 200
    data = response.json()
    for user in data:
        #Reusable validation helper
        validate_user_fields(user)

#-------------------------------------------------------------------------------
# Positive GET /users/{id} Tests
#-------------------------------------------------------------------------------
#Test specified user fields exist
@pytest.mark.parametrize("user_id", [1])
def test_get_user_fields_present(api_client, user_id):
    #Act
    response = api_client.get(f"/users/{user_id}")

    #Assert
    assert response.status_code == 200
    data = response.json()
    #Helper function to validate all fields
    validate_user_fields(data)


#Test specified user(s) id exists
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_valid_id(api_client, user_id):
    #Act
    response = api_client.get(f"/users/{user_id}")

    #Assert
    assert response.status_code == 200
    data = response.json()
    #Verify returned id matches the requested id
    assert data["id"] == user_id

#Test for users specified in users_test_data
@pytest.mark.parametrize("user_data", users_test_data)
def test_get_user_data_matches_expected(api_client, user_data):
    #Arrange
    user_id = user_data["id"]
    
    # Act
    response = api_client.get(f"/users/{user_id}")

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]

#-------------------------------------------------------------------------------
# Positive POST Tests
#-------------------------------------------------------------------------------
#Test create user
#Using JSONPlaceholder as endpoint
@pytest.mark.parametrize("user_payload", users_test_data)
def test_create_user_valid_payload(api_client, user_payload):
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

#Test create user minimum payload------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Positive PUT Tests
#-------------------------------------------------------------------------------
#Test updated fields are returned
@pytest.mark.parametrize("user_payload", [{"name": "Leanne Graham"}])
def test_update_user_valid_payload(api_client, user_payload):
    #Act
    response = api_client.put("/users/1", json=user_payload)
    data = response.json()
    
    #Assert
    assert response.status_code == 200
    assert data["name"] == user_payload["name"]


#-------------------------------------------------------------------------------
# Positive DELETE Tests
#-------------------------------------------------------------------------------
#Test valid return code for user deletion
@pytest.mark.parametrize("user_payload", users_test_data)
def test_delete_user_valid_id(api_client, user_payload):
    #Act
    response = api_client.delete("/users", json=user_payload)

    #Assert
    assert response.status_code == 200 or 204
   


#-------------------------------------------------------------------------------
# Negative GET Tests
#-------------------------------------------------------------------------------
#Test for specified invalid user id
@pytest.mark.parametrize("invalid_id", [0, -1, 999])
def test_get_user_invalid_id_returns_404(api_client, invalid_id):
    #Act
    response = api_client.get(f"/users/{invalid_id}")
    
    #Assert
    assert response.status_code == 404

#Test get user by string - expected 404
@pytest.mark.parametrize("invalid_id", "abc")
def test_get_user_string_id(api_client, invalid_id):
    #Act
    response = api_client.get(f"/users/{invalid_id}")

    #Assert
    assert response.status_code == 404

#-------------------------------------------------------------------------------
# Negative POST Tests
#-------------------------------------------------------------------------------
#Test create user without required field (missing Address)
@pytest.mark.parametrize("user_payload", [{
        "id": 1,
        "name": "Leanne Graham",
        "email": "Sincere@april.biz"
    }])
def test_create_user_missing_required_field(api_client, user_payload):
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    assert response.status_code == 201
    # Note: JSONPlaceholder does not enforce required fields on test POST
    validate_user_fields(data)

#Test create user with invalid email
@pytest.mark.parametrize("user_payload", [{
        "id": 11,
        "name": "Leanne Graham",
        "email": "InvalidEmail@google"
    }])
def test_create_user_invalid_email_format(api_client, user_payload):
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    assert response.status_code == 201
    # Note: JSONPlaceholder does not enforce email format on test POST
    validate_user_fields(data)

#Test create user with empty payload
@pytest.mark.parametrize("user_payload", [{}])
def test_create_user_empty_payload(api_client, user_payload):
    #Act
    response = api_client.post("/users", json=user_payload)
    data = response.json()

    #Assert
    assert response.status_code == 201
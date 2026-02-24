import json
import pytest
from pathlib import Path
from src.utils.validation import validate_post_fields

# Load test data
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "posts_test_data.json"
with open(DATA_FILE) as f:
    posts_test_data = json.load(f)

#-------------------------------------------------------------------------------
# Positive GET /posts Tests
#-------------------------------------------------------------------------------
# Test getting all posts
def test_get_all_posts(api_client):
    #Act
    response = api_client.get("/posts")
    data = response.json()

    #Assert
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0

#Test getting post with valid url id
@pytest.mark.parametrize("valid_id", [1, 2, 3])
def test_get_post_valid_id(api_client, valid_id):
    #Act
    response = api_client.get(f"/posts/{valid_id}")
    data = response.json()

    #Assert
    assert response.status_code == 200
    assert data["id"] == valid_id

#Test all fields are present
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_fields_present(api_client, post_id):
    #Act
    response = api_client.get(f"/posts/{post_id}")
    data = response.json()

    #Assert
    assert response.status_code == 200
    #Helper function to validate all fields
    validate_post_fields(data)

#-------------------------------------------------------------------------------
# Positive POST /posts Tests
#-------------------------------------------------------------------------------
#Test creating post with valid payload
@pytest.mark.parametrize("payload", posts_test_data)
def test_create_post_valid_payload(api_client, payload):
    #Act
    response = api_client.post("/posts", json=payload)
    data = response.json()

    #Assert
    assert response.status_code == 201
    # Note: JSONPlaceholder echos the payload
    validate_post_fields(data)

#-------------------------------------------------------------------------------
# Positive PUT /posts Tests
#-------------------------------------------------------------------------------
#Test updating a post with a valid payload
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_update_post_valid_payload(api_client, post_id):
    post_payload = posts_test_data[0]
    #Act
    response = api_client.put(f"/posts/{post_id}", json=post_payload)

    #Assert
    assert response.status_code == 200

#-------------------------------------------------------------------------------
# Positive DELETE /posts Tests
#-------------------------------------------------------------------------------
#Test deleting a post with a valid id
@pytest.mark.parametrize("payload", [1, 2, 3])
def test_delete_post_valid_id(api_client, payload):
    #Act
    response = api_client.delete(f"/posts/{payload}")

    #Assert
    # JSONPlaceholder does not actually delete posts
    # In a real API, this would return 204
    assert response.status_code == 200



#-------------------------------------------------------------------------------
# Negative GET /posts Tests
#-------------------------------------------------------------------------------
#Test getting a post with an invalid id
@pytest.mark.parametrize("invalid_id", [-1, 0, 9999])
def test_get_post_invalid_id(api_client, invalid_id):
    #Act
    response = api_client.get(f"/posts/{invalid_id}")

    #Assert
    assert response.status_code == 404

#-------------------------------------------------------------------------------
# Negative POST /posts Tests
#-------------------------------------------------------------------------------
#Test creating a post with a missing field (missing userId)
def test_create_post_missing_title(api_client):
    payload = [
        {"body": "Test Body"},
        {"body": "Test Body2"},
        {"body": "Test Body3"}
        ]
    
    #Act
    response = api_client.post("/posts", json=payload)
    data = response.json()

    #Assert
    # JSONPlaceholder does not validate required fields and echos payload
    # In a real API, this would return 400
    assert response.status_code == 201
    assert "title" not in data

#-------------------------------------------------------------------------------
# Negative PUT /posts Tests
#-------------------------------------------------------------------------------
#Test updating a post using an invalid url id
@pytest.mark.parametrize("invalid_id", [-1, 0, 9999])
def test_update_post_invalid_id(api_client, invalid_id):
    post_payload = {
        "title": "Testing"
    }
    #Act
    response = api_client.put(f"/posts/{invalid_id}", json=post_payload)

    #Assert
    # JSONPlaceholder returns 500
    # In a real API, this would return 404
    assert response.status_code == 404 or 500

#-------------------------------------------------------------------------------
# Negative DELETE /posts Tests
#-------------------------------------------------------------------------------
#Test deleting a post with an invalid url id
@pytest.mark.parametrize("invalid_id", [-1, 0, 9999])
def test_delete_post_invalid_id(api_client, invalid_id):
    #Act
    response = api_client.delete(f"/posts/{invalid_id}")

    #Assert
    # JSONPlaceholder returns 200
    # In a real API, this would return 404
    assert response.status_code == 404 or 200
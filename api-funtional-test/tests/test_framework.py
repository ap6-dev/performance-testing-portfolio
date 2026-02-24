import pytest

#-------------------------------------------------------------------------------
# Test response time
#-------------------------------------------------------------------------------
#Test to see if API response time is under specified threshold
def test_response_time(api_client):
    #Act
    response = api_client.get("/users")

    #Assert response time is under 500ms
    #JSONPlaceholder is fast
    assert response.elapsed.total_seconds() < 0.5

#-------------------------------------------------------------------------------
# Test response content type
#-------------------------------------------------------------------------------
#Test verifying response data returned is json format
def test_content_type_is_json(api_client):
    #Act
    response = api_client.get("/users/1")

    content_type = response.headers.get("Content-Type")
    #Assert
    assert content_type is not None
    assert "application/json" in content_type

#-------------------------------------------------------------------------------
# Test Status Code Type
#-------------------------------------------------------------------------------
# Test verifying all responses return an integer HTTP status code
@pytest.mark.parametrize("endpoint", ["/users", "/users/1", "/posts", "/posts/1"])
def test_status_code_is_int(api_client, endpoint):
    #Act
    response = api_client.get(endpoint)

    #Assert
    assert isinstance(response.status_code, int)
    #Valid HTTP range
    assert 100 <= response.status_code <= 599
def validate_user_fields(data, expected_fields=("id", "name", "email")):
    for field in expected_fields:
        assert field in data, f"Missing User field: {field}"

def validate_post_fields(data, expected_fields=("userId", "id", "title", "body")):
    for field in expected_fields:
        assert field in data, f"Missing Post field: {field}"
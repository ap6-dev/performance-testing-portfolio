def validate_user_fields(data, expected_fields=("id", "name", "email")):
    for field in expected_fields:
        assert field in data, f"Missing field: {field}"
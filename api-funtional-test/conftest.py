import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from clients.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def api_client():
    return APIClient(BASE_URL)
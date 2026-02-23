import logging
import pytest
from src.clients.api_client import APIClient

#--------------------------
# Logging Setup
#--------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_logs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def api_client():
    return APIClient(BASE_URL)
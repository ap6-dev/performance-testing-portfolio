import logging
import pytest
from src.clients.api_client import APIClient
from pathlib import Path

# Load test data
PROJECT_ROOT = Path(__file__).resolve().parent
LOG_FILE = PROJECT_ROOT / "test_logs.log"


#-------------------------------------------------------------------------------
# Logging Setup
#-------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Pytest Fixture Setup
#-------------------------------------------------------------------------------
BASE_URL = "https://jsonplaceholder.typicode.com"
#Json placeholder for testing

@pytest.fixture
def api_client():
    return APIClient(BASE_URL)
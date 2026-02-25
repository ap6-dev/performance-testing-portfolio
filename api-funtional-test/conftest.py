import os
import logging
import pytest
from src.clients.api_client import APIClient
from pathlib import Path
from src.utils.performance import print_summary

# Load test data
PROJECT_ROOT = Path(__file__).resolve().parent
LOG_FILE = PROJECT_ROOT / "test_logs.log"


#-------------------------------------------------------------------------------
# Logging Setup
#-------------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.truncate(0)

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

@pytest.fixture(scope="session")
def api_client():
    return APIClient(BASE_URL)

#-------------------------------------------------------------------------------
# Performance Summary
#-------------------------------------------------------------------------------
def pytest_sessionfinish(session, exitstatus):
    print_summary()
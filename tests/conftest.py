import pytest
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://auth.vvdntech.com/api/v1")

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def api_headers():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if os.getenv("API_KEY"):
        headers["X-API-Key"] = os.getenv("API_KEY")
    if os.getenv("AUTH_TOKEN"):
        headers["Authorization"] = f"Bearer {os.getenv('AUTH_TOKEN')}"
    return headers

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://auth.vvdntech.com/api/v1")
API_KEY = os.getenv("API_KEY", "")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
TIMEOUT = int(os.getenv("TIMEOUT", "30"))

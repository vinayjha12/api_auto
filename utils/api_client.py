import requests
import os
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "https://api.example.com")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        if os.getenv("API_KEY"):
            self.session.headers["X-API-Key"] = os.getenv("API_KEY")
        if os.getenv("AUTH_TOKEN"):
            self.session.headers["Authorization"] = f"Bearer {os.getenv('AUTH_TOKEN')}"

    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", **kwargs)

    def put(self, endpoint, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.session.patch(f"{self.base_url}{endpoint}", **kwargs)

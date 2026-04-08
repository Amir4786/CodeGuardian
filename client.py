import os
import httpx
from models import Action, Observation

class CodeGuardianClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.environ.get("ENV_BASE_URL", "http://localhost:7860")
        self.client = httpx.Client(timeout=30.0)

    def reset(self):
        resp = self.client.post(f"{self.base_url}/reset")
        resp.raise_for_status()
        return Observation(**resp.json())

    def state(self):
        resp = self.client.get(f"{self.base_url}/state")
        resp.raise_for_status()
        return Observation(**resp.json())

    def step(self, action: Action):
        data = action.model_dump()
        resp = self.client.post(f"{self.base_url}/step", json=data)
        resp.raise_for_status()
        resp_data = resp.json()
        return Observation(**resp_data["observation"]), resp_data["reward"], resp_data["done"], resp_data["info"]

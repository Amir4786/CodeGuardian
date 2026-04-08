from fastapi import FastAPI
from pydantic import BaseModel
from models import Action, Observation
from server.security_env import SecurityEnv

app = FastAPI(title="CodeGuardian OpenEnv API", description="Security focused code review environment.")

env = SecurityEnv()

@app.get("/")
def home():
    return {
        "name": "CodeGuardian OpenEnv API",
        "status": "running",
        "message": "Welcome to the CodeGuardian Environment. Use the OpenEnv SDK or visit /docs to interact with the endpoints.",
        "endpoints": ["/reset (POST)", "/step (POST)", "/state (GET)"]
    }

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict

@app.post("/reset", response_model=Observation)
def reset_env():
    return env.reset()

@app.get("/state", response_model=Observation)
def get_state():
    return env.state()

@app.post("/step", response_model=StepResponse)
def step_env(action: Action):
    obs, reward, done, info = env.step(action)
    return StepResponse(observation=obs, reward=reward, done=done, info=info)

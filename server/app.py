from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os
from models import Action, Observation
from server.security_env import SecurityEnv
from utils.scanner import execute_scan

app = FastAPI(title="CodeGuardian OpenEnv API", description="Security focused code review environment.")

env = SecurityEnv()

@app.get("/")
def home():
    return {
        "name": "CodeGuardian OpenEnv API",
        "status": "running",
        "message": "Welcome to the CodeGuardian Environment. Use the OpenEnv SDK or visit /docs to interact with the endpoints.",
        "endpoints": ["/reset (POST)", "/step (POST)", "/state (GET)", "/scan (POST)"]
    }

class ScanRequest(BaseModel):
    file_path: Optional[str] = None
    code_content: Optional[str] = None

@app.post("/scan")
def scan_code(request: ScanRequest):
    if not request.file_path and not request.code_content:
        return {"error": "Must provide either 'file_path' or 'code_content'."}
        
    content_to_scan = ""
    if request.code_content:
        content_to_scan = request.code_content
    elif request.file_path:
        # Protect against non-existent paths on the host/container
        if not os.path.exists(request.file_path):
            return {"error": f"Path '{request.file_path}' not found on server."}
            
        if os.path.isdir(request.file_path):
            # Aggregator for directory scans
            py_files = []
            for root, _, files in os.walk(request.file_path):
                for f in files:
                    if f.endswith('.py'):
                        py_files.append(os.path.join(root, f))
                        
            if not py_files:
                 return {"error": "No Python files found in directory."}
                 
            for pyf in py_files[:10]: # Limit to 10 files to avoid massive context
                with open(pyf, "r", encoding="utf-8") as file:
                    content_to_scan += f"\\n# File: {pyf}\\n{file.read()}\\n"
        else:
            with open(request.file_path, "r", encoding="utf-8") as file:
                content_to_scan = file.read()
                
    result = execute_scan(content_to_scan)
    return result

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

from pydantic import BaseModel, Field
from typing import List, Optional

class Action(BaseModel):
    vulnerability_type: Optional[str] = Field(None, description="The type of vulnerability found")
    vulnerable_lines: Optional[List[int]] = Field(default_factory=list, description="Line numbers containing vulnerabilities")
    secrets_found: Optional[List[str]] = Field(default_factory=list, description="Exact secret values found (for easy task)")
    fixed_code: Optional[str] = Field(None, description="Secure version of the code snippet (for hard task)")
    explanation: Optional[str] = Field(None, description="Explanation of the fix and vulnerability")

class Observation(BaseModel):
    code_snippet: str = Field(..., description="The code to review")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    instructions: str = Field(..., description="Instructions for the current task")
    current_reward: float = Field(0.0, description="Cumulative reward of the current step")
    done: bool = Field(False, description="Whether the episode or state is completed")

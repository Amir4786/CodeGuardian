from models import Action, Observation
from tasks.easy_tasks import EASY_TASKS
from tasks.medium_tasks import MEDIUM_TASKS
from tasks.hard_tasks import HARD_TASKS
from graders.easy_grader import grade as grade_easy
from graders.medium_grader import grade as grade_medium
from graders.hard_grader import grade as grade_hard

class SecurityEnv:
    def __init__(self):
        self._difficulty_cycle = ["easy", "medium", "hard"]
        self._cycle_idx = -1
        self.reset()
        
    def reset(self):
        self._cycle_idx = (self._cycle_idx + 1) % len(self._difficulty_cycle)
        self.current_difficulty = self._difficulty_cycle[self._cycle_idx]
        self.task_idx = 0 # Just take the first task of each type for simplicity in validation
        self.cumulative_reward = 0.01
        self.all_tasks = {
            "easy": EASY_TASKS,
            "medium": MEDIUM_TASKS,
            "hard": HARD_TASKS
        }
        self.is_done = False
        return self.state()
        
    def state(self) -> Observation:
        current_task = self.all_tasks[self.current_difficulty][self.task_idx]
        
        instructions = ""
        if self.current_difficulty == "easy":
            instructions = "Find all hardcoded secrets in the code snippet. Return line numbers containing secrets."
        elif self.current_difficulty == "medium":
            instructions = "Identify SQL injection vulnerabilities. Return line numbers containing the vulnerability."
        elif self.current_difficulty == "hard":
            instructions = current_task.get("instruction", "Rewrite code securely and explain the fix.")
            
        return Observation(
            code_snippet=current_task["code"],
            difficulty=self.current_difficulty,
            instructions=instructions,
            current_reward=round(self.cumulative_reward, 3),
            done=self.is_done
        )

    def step(self, action: Action):
        if self.is_done:
            return self.state(), 0.01, True, {}
            
        current_task = self.all_tasks[self.current_difficulty][self.task_idx]
        
        score = 0.0
        if self.current_difficulty == "easy":
            true_lines = current_task.get("secret_lines", [])
            score = grade_easy(action.vulnerable_lines, true_lines)
            
        elif self.current_difficulty == "medium":
            true_lines = current_task.get("vulnerable_lines", [])
            score = grade_medium(action.vulnerable_lines, true_lines)
            
        elif self.current_difficulty == "hard":
            score = grade_hard(
                current_task["id"], 
                action.fixed_code if action.fixed_code else "", 
                action.explanation if action.explanation else "", 
                current_task.get("expected_fixes", [])
            )
        
        # Strictly between 0 and 1
        reward = max(0.01, min(0.99, score))
        self.cumulative_reward += reward
        self.is_done = True
                
        return self.state(), round(reward, 2), True, {"score": score}

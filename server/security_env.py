from models import Action, Observation
from tasks.easy_tasks import EASY_TASKS
from tasks.medium_tasks import MEDIUM_TASKS
from tasks.hard_tasks import HARD_TASKS
from graders.easy_grader import grade as grade_easy
from graders.medium_grader import grade as grade_medium
from graders.hard_grader import grade as grade_hard

class SecurityEnv:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.current_difficulty = "easy"
        self.task_idx = 0
        self.cumulative_reward = 0.0
        self.all_tasks = {
            "easy": EASY_TASKS,
            "medium": MEDIUM_TASKS,
            "hard": HARD_TASKS
        }
        return self.state()
        
    def state(self) -> Observation:
        if self.current_difficulty is None:
            return Observation(
                code_snippet="All tasks completed.",
                difficulty="done",
                instructions="You have finished all tasks.",
                current_reward=round(self.cumulative_reward, 2),
                done=True
            )
            
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
            current_reward=round(self.cumulative_reward, 2),
            done=False
        )

    def step(self, action: Action):
        if self.current_difficulty is None:
            return self.state(), 0.0, True, {}
            
        current_task = self.all_tasks[self.current_difficulty][self.task_idx]
        reward = 0.0
        
        # Reward logic based on User Spec
        # +0.1 per line analyzed (we will award this for the length of code lines automatically or based on interaction)
        lines_analyzed = len(current_task["code"].strip().split('\\n'))
        reward += 0.1 * lines_analyzed
        
        score = 0.0
        if self.current_difficulty == "easy":
            true_lines = current_task.get("secret_lines", [])
            score = grade_easy(action.vulnerable_lines, true_lines)
            
            true_set = set(true_lines)
            agent_set = set(action.vulnerable_lines if action.vulnerable_lines else [])
            tp = len(true_set.intersection(agent_set))
            fp = len(agent_set - true_set)
            reward += (tp * 0.5) - (fp * 0.3)
            
        elif self.current_difficulty == "medium":
            true_lines = current_task.get("vulnerable_lines", [])
            score = grade_medium(action.vulnerable_lines, true_lines)
            
            true_set = set(true_lines)
            agent_set = set(action.vulnerable_lines if action.vulnerable_lines else [])
            tp = len(true_set.intersection(agent_set))
            fp = len(agent_set - true_set)
            reward += (tp * 0.5) - (fp * 0.3)
            
        elif self.current_difficulty == "hard":
            score = grade_hard(
                current_task["id"], 
                action.fixed_code if action.fixed_code else "", 
                action.explanation if action.explanation else "", 
                current_task.get("expected_fixes", [])
            )
            if score >= 0.8:
                reward += 0.4
            elif score == 0.0 and action.fixed_code:
                reward -= 0.5
                
        self.cumulative_reward += reward
        
        # Advance state
        self.task_idx += 1
        if self.task_idx >= len(self.all_tasks[self.current_difficulty]):
            self.task_idx = 0
            if self.current_difficulty == "easy":
                self.current_difficulty = "medium"
            elif self.current_difficulty == "medium":
                self.current_difficulty = "hard"
            else:
                self.current_difficulty = None
                
        return self.state(), round(reward, 2), self.current_difficulty is None, {"score": score}

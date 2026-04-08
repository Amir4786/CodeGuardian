import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

from client import CodeGuardianClient
from models import Action

def main():
    # Standard OpenAI token prioritized natively, fallback to HF_TOKEN if running on Spaces
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = os.environ.get("HF_TOKEN", "dummy_key") 
        if api_key == "dummy_key":
            logging.warning("OPENAI_API_KEY or HF_TOKEN not found; using fallback dummy key.")

    base_url = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
    model_name = os.environ.get("MODEL_NAME", "gpt-4o-mini")

    openai_client = OpenAI(api_key=api_key, base_url=base_url)
    env_client = CodeGuardianClient()

    # Get task name from environment or use default
    task_name = os.environ.get("TASK_NAME", "codeguardian_security")
    
    # Print START line with required format
    print(f"[START] task={task_name} env=codeguardian model={model_name}")
    
    step_num = 0
    rewards_list = []
    success = True
    
    try:
        obs = env_client.reset()
    except Exception as e:
        print(f"[END] success=false steps=0 rewards=[] error=\"Connection failed: {e}\"")
        return

    while not obs.done and step_num < 50:  # Limit steps to prevent infinite loops
        step_num += 1
        
        if obs.difficulty == "easy":
            system_prompt = f"""Analyze this code for hardcoded secrets (API keys, passwords, tokens). Return ONLY valid JSON matching:
            {{ "vulnerable_lines": [integer, 1-indexed line numbers] }}
            Code:
            {obs.code_snippet}
            """
        elif obs.difficulty == "medium":
            system_prompt = f"""Analyze this code for SQL injection vulnerabilities. Return ONLY valid JSON matching:
            {{ "vulnerable_lines": [integer, 1-indexed line numbers] }}
            Code:
            {obs.code_snippet}
            """
        else:
            system_prompt = f"""{obs.instructions} Return ONLY valid JSON matching:
            {{ "fixed_code": "secure code string", "explanation": "string" }}
            Code:
            {obs.code_snippet}
            """

        error_msg = "null"
        try:
            response = openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a code security expert. Respond strictly with JSON format."},
                    {"role": "user", "content": system_prompt}
                ],
                response_format={"type": "json_object"}
            )
            raw_content = response.choices[0].message.content
            action_data = json.loads(raw_content)
            action = Action(**action_data)
            action_str = json.dumps(action_data).replace('"', '\\"')
        except Exception as e:
            # Fallback action
            action = Action()
            action_str = "{}"
            success = False
            error_msg = f"\"{str(e)}\""

        obs, reward, done, info = env_client.step(action)
        rewards_list.append(round(reward, 2))
        
        # Format the step log exactly as required
        print(f"[STEP] step={step_num} action=\"{action_str}\" reward={reward:.2f} done={str(done).lower()} error={error_msg}")

    print(f"[END] success={str(success).lower()} steps={step_num} rewards={json.dumps(rewards_list)}")

if __name__ == "__main__":
    main()

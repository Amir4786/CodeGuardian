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

    # Run exactly 3 episodes (Easy, Medium, Hard) as required by OpenEnv spec
    for _ in range(3):
        try:
            obs = env_client.reset()
        except Exception as e:
            # Emit END line on failure as per rules
            print(f"[END] success=false steps=0 rewards=0.00 error=\"Connection failed: {e}\"")
            continue

        # Format START line correctly
        print(f"[START] task={obs.difficulty}_task env=codeguardian model={model_name}")
        
        step_num = 1
        rewards_list = []
        success = True
        error_msg = "null"
        
        # Build prompt based on current difficulty
        if obs.difficulty == "easy":
            prompt = f"Analyze for secrets. Return JSON: {{\"vulnerable_lines\": [int]}}\nCode:\n{obs.code_snippet}"
        elif obs.difficulty == "medium":
            prompt = f"Analyze for SQLi. Return JSON: {{\"vulnerable_lines\": [int]}}\nCode:\n{obs.code_snippet}"
        else:
            prompt = f"{obs.instructions}\nCode:\n{obs.code_snippet}"

        try:
            response = openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a code security expert. Respond strictly with JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            raw_content = response.choices[0].message.content
            action_data = json.loads(raw_content)
            action = Action(**action_data)
            # Remove spaces from JSON for log safety
            action_str = json.dumps(action_data, separators=(',', ':'))
        except Exception as e:
            action = Action()
            action_str = "{}"
            success = False
            error_msg = f"\"{str(e)}\""

        # Step and collect reward
        obs, reward, done, info = env_client.step(action)
        rewards_list.append(reward)
        
        # Format logs correctly
        print(f"[STEP] step={step_num} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error_msg}")
        
        # Comma separated rewards string
        rewards_str = ",".join([f"{r:.2f}" for r in rewards_list])
        print(f"[END] success={str(success).lower()} steps={step_num} rewards={rewards_str}")

if __name__ == "__main__":
    main()

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def execute_scan(code_content: str, api_key: str = None, model_name: str = "gpt-4o-mini") -> dict:
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY is not configured on the server."}
        
    client = OpenAI(api_key=api_key)
    
    system_prompt = f"""You are a professional code security scanner. Analyze the following Python code for ANY vulnerabilities.
    Evaluate for:
    - Hardcoded secrets / Passwords / API tokens
    - SQL Injection vulnerabilities
    - Insecure configurations
    
    Code to Analyze:
    ```python
    {code_content}
    ```
    
    Return ONLY valid JSON matching this schema exactly:
    {{
      "vulnerabilities_found": boolean,
      "details": [
          {{
              "severity": "High/Medium/Low",
              "vulnerability_type": "string",
              "line_numbers": [integer],
              "explanation": "Brief explanation of the risk",
              "suggested_fix": "Secure code generation replacing the bad code"
          }}
      ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a senior cybersecurity engineer. Respond strictly with JSON format."},
                {"role": "user", "content": system_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Error communicating with OpenAI API: {str(e)}"}

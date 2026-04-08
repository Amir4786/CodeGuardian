import os
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def scan_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    with open(file_path, "r") as f:
        code_content = f.read()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set in .env")
        return

    model_name = os.environ.get("MODEL_NAME", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    print(f"\\n🔍 Scanning '{file_path}' with {model_name}...\\n")

    system_prompt = f"""You are a professional code security scanner. Analyze the following Python script for ANY vulnerabilities.
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
        
        result = json.loads(response.choices[0].message.content)
        
        if not result.get("vulnerabilities_found", False):
            print("✅ Great news! No major vulnerabilities were flagged in this script.")
        else:
            print(f"⚠️  WARNING: Found {len(result.get('details', []))} Vulnerabilit(ies):\\n")
            for idx, issue in enumerate(result.get("details", []), 1):
                print(f"[{idx}] {issue.get('severity', 'Unknown')} | {issue.get('vulnerability_type', 'Unclassified')}")
                print(f"    Line(s): {issue.get('line_numbers', [])}")
                print(f"    Details: {issue.get('explanation', '')}")
                formatted_fix = issue.get('suggested_fix', '').replace('\\n', '\\n        ')
                print(f"    Suggestion:\\n        {formatted_fix}\\n")
                
    except Exception as e:
        print(f"❌ Error communicating with OpenAI API: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scan_my_code.py <path_to_your_python_file.py>")
    else:
        scan_file(sys.argv[1])

---
title: CodeGuardian
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
tags:
  - openenv
  - security
---

# CodeGuardian

## What Does This Application Do?
CodeGuardian is essentially a "training gym" or benchmark test for AI agents, specifically designed to grade their cybersecurity skills!

Normally, when you ask an AI to write code, you don't know if the code is actually secure. CodeGuardian provides a standardized environment to automatically test how good a model (like GPT-4o, Llama, or Claude) is at spotting and fixing security vulnerabilities without any human intervention.

Here is the step-by-step of what it actually does when an AI connects to it via the OpenEnv API:

1. **It Serves Vulnerable Code:** It acts as a server that hands an AI agent a piece of Python code with hidden security flaws.
2. **It Tests Across Three Difficulties:**
   - **Easy:** The AI has to find where hardcoded passwords or API keys are hidden.
   - **Medium:** The AI must pinpoint the exact line numbers containing SQL Injections.
   - **Hard:** The AI must generate a rewritten, completely secure version of the codebase.
3. **It Automatically Grades Them (Zero Human Effort):** When the AI submits its answer, CodeGuardian automatically grades it. It uses programmatic rules—like verifying exact strings, precision line matching, and validating the Abstract Syntax Tree (AST)—to see if the AI successfully fixed the issue without breaking the code.
4. **It Gives Rewards:** If the AI does well, CodeGuardian hands it a positive "Reward" score (e.g., `+0.5`). If it hallucinates or writes unsafe code, it subtracts points.

By deploying this application to Hugging Face, we've created an **OpenEnv-compliant benchmark**. Because it follows the exact specifications, machine learning engineers can plug their experimental security models into the CodeGuardian URL to automatically evaluate how smart their AI is natively!

## Security Motivation
Finding vulnerabilities early in the software development lifecycle prevents large-scale data breaches. CodeGuardian simulates standard developer environments testing agents across:
1. **Easy:** Hardcoded Secrets Detection (Precision/Recall).
2. **Medium:** SQL Injection Detection (Identifying Vulnerable Line Numbers).
3. **Hard:** Secure Code Generation (Generating functional and safe code).

By giving structured rewards automatically without human-in-the-loop, it encourages the continuous learning of LLMs in secure coding practices.

## Baseline Scores
Testing across our validation set with `gpt-4o-mini`:
- **Easy:** 0.85/1.0
- **Medium:** 0.60/1.0
- **Hard:** 0.35/1.0 (Struggles with precise context reconstruction)

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the environment server:
   ```bash
   uvicorn server.app:app --port 7860
   ```
3. Run the reference inference script:
## Manual Custom Scans (New Features!)
CodeGuardian doesn't just evaluate test logic! You can now use the underlying OpenAI logic to check any personal scripts you have natively. 

1. **CLI Utility (`scan_my_code.py`):**
   Evaluate any local file by dropping it into the terminal. This provides highly detailed security reports.
   ```bash
   python3 scan_my_code.py /path/to/your/script.py
   ```

2. **API Endpoint (`/scan`):**
   The FastAPI container exposes a new `/scan` endpoint that can process files directly!
   ```bash
   curl -X POST http://localhost:7860/scan \\
        -H "Content-Type: application/json" \\
        -d '{"file_path": "/app/server", "code_content": null}'
   ```
   *Note: Passing a folder via `file_path` will recursively aggregate and scan all Python files found within.* Alternatively, you can pass `"code_content": "def test(): pass"` directly instead.

## OpenEnv Compatibility
This repository fully supports the OpenEnv standard `openenv.yaml` specification and provides HTTP methods supporting `reset`, `state`, and `step`.
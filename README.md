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

CodeGuardian is an OpenEnv-compliant reinforcement learning environment designed to train and evaluate AI agents on code security tasks.

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
   ```bash
   export HF_TOKEN="your_hf_token" # Or OPENAI_API_KEY
   python inference.py
   ```

## OpenEnv Compatibility
This repository fully supports the OpenEnv standard `openenv.yaml` specification and provides HTTP methods supporting `reset`, `state`, and `step`.
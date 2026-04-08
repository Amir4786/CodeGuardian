import logging
from utils.ast_analyzer import analyze_python_code

def grade(task_id: str, fixed_code: str, explanation: str, expected_fixes: list) -> float:
    """
    Grade the hard task by checking validity and context of the fixed code.
    """
    score = 0.0
    
    if not fixed_code:
        return score
        
    if explanation and len(explanation.strip()) > 10:
        score += 0.2
        
    ast_report = analyze_python_code(fixed_code)
    
    if not ast_report["valid_python"]:
        return 0.0  # Invalid python gets zero score
        
    score += 0.3
    
    if task_id == "hard_1":
        # SQL Injection fix
        if ast_report["has_sql_injection_pattern"]:
            return score # Code is valid but still vulnerable
        
        # Check if they parameterized
        if any(fix in fixed_code for fix in ["?", "%s", "execute(", ":"]):
            if "execute(query," in fixed_code.replace(" ", "") or "execute(q," in fixed_code.replace(" ", "") or "?" in fixed_code:
                score += 0.5
                
    elif task_id == "hard_2":
        # Secret fix
        has_env_usage = any(fix in fixed_code for fix in expected_fixes)
        if has_env_usage and "sk_test_" not in fixed_code:
            score += 0.5
            
    return min(1.0, score)

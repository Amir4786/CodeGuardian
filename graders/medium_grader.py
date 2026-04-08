def grade(agent_lines: list, true_lines: list) -> float:
    """
    Grade medium SQL injection identification based on strict line matching.
    """
    if not true_lines and not agent_lines:
        return 1.0  # Safe code, correctly flagged as safe
        
    if not true_lines and agent_lines:
        return 0.0  # False positive
        
    if true_lines and not agent_lines:
        return 0.0  # Missed vulnerability
        
    # Check if exact lines are identified
    true_set = set(true_lines)
    agent_set = set(agent_lines)
    
    if true_set == agent_set:
        return 1.0
        
    # Partial correctness
    correct_flags = len(true_set.intersection(agent_set))
    if correct_flags > 0:
        return 0.5
        
    return 0.0

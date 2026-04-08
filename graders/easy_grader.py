def grade(agent_lines: list, true_lines: list) -> float:
    """
    Calculate F1 Score for precision/recall on secret detection lines.
    """
    if not true_lines and not agent_lines:
        return 1.0  # Correctly identified no secrets
    
    if not true_lines and agent_lines:
        return 0.0  # False alarm
        
    if true_lines and not agent_lines:
        return 0.0  # Missed secrets

    true_set = set(true_lines)
    agent_set = set(agent_lines)
    
    true_positives = len(true_set.intersection(agent_set))
    false_positives = len(agent_set - true_set)
    false_negatives = len(true_set - agent_set)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    
    if precision + recall == 0:
        return 0.0
        
    f1 = 2 * (precision * recall) / (precision + recall)
    return round(f1, 2)

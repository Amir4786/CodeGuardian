import re
from typing import List

SECRET_PATTERNS = [
    re.compile(r'(api_key|apikey|token|password|secret|pwd)[\s]*=[\s]*[\'"][A-Za-z0-9\-_]+[\'"]', re.IGNORECASE),
    re.compile(r'(Bearer\s+[A-Za-z0-9\-_]+)', re.IGNORECASE)
]

def find_secrets_with_regex(code: str) -> List[str]:
    """Fallback method for finding typical secrets with regex"""
    secrets = []
    for pattern in SECRET_PATTERNS:
        secrets.extend(pattern.findall(code))
    return list(set(secrets))

def lines_with_secrets(code: str) -> List[int]:
    """Find line numbers containing typical secrets."""
    lines_found = []
    lines = code.split('\n')
    for i, line in enumerate(lines):
        for pattern in SECRET_PATTERNS:
            if pattern.search(line):
                lines_found.append(i + 1)
                break
    return lines_found

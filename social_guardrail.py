import re
from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class ScanResult:
    is_safe: bool
    text: str
    violations: List[str] = field(default_factory=list)
    redacted_text: str = ""

class SocialMediaGuardrail:
    def __init__(self, unapproved_keywords: Set[str] = None):
        self.secret_patterns = {
            "OpenAI API Key": r"sk-[a-zA-Z0-9]{32,}",
            "Google AI Key": r"AIzaSy[a-zA-Z0-9_-]{33}",
            "GitHub Token": r"(ghp|gho|ghu|ghs|ghr|github_pat)_[a-zA-Z0-9]{36,255}",
            "AWS Access Key": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
        }
        self.path_patterns = {
            "Windows Path": r"(?:[a-zA-Z]:\\(?:[^\s\\/:*?\"<>|]+\\)+[^\s\\/:*?\"<>|]+)",
            "Linux/Mac Path": r"(?:/(?:home|Users|var|etc)/[a-zA-Z0-9_-]+(?:/[^\s/]+)+)",
        }
        self.unapproved_keywords = unapproved_keywords or {"internal build", "unreleased hardware"}

    def scan(self, text: str) -> ScanResult:
        violations, redacted_text = [], text
        for secret_name, pattern in self.secret_patterns.items():
            if re.search(pattern, text):
                violations.append(f"Exposed Secret ({secret_name})")
                redacted_text = re.sub(pattern, "[REDACTED_SECRET]", redacted_text)
        for path_name, pattern in self.path_patterns.items():
            if re.search(pattern, text):
                violations.append(f"Internal Path ({path_name})")
                redacted_text = re.sub(pattern, "[REDACTED_PATH]", redacted_text)
        for kw in self.unapproved_keywords:
            kw_pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(kw_pattern, text, re.IGNORECASE):
                violations.append(f"Restricted Keyword: '{kw}'")
                redacted_text = re.sub(kw_pattern, "[REDACTED_KW]", redacted_text, flags=re.IGNORECASE)
        return ScanResult(len(violations) == 0, text, violations, redacted_text)

if __name__ == "__main__":
    guard = SocialMediaGuardrail()
    test_post = "Testing GVF Orchestrator build at C:\\Users\\17722\\Desktop\\config.json with key sk-proj1234567890abcdef1234567890abcdef"
    res = guard.scan(test_post)
    print("\n--- GUARDRAIL SCAN RESULT ---")
    print(f"Is Safe: {res.is_safe}")
    print("Violations:", res.violations)
    print("Sanitized Output:\n", res.redacted_text)

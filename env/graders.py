from typing import List
from .models import Finding

MIN_STRICT_SCORE = 0.000001
MAX_STRICT_SCORE = 0.999999


def sanitize_score(score: float) -> float:
    """Clamp scores to the validator-safe open interval (0, 1)."""
    return max(MIN_STRICT_SCORE, min(MAX_STRICT_SCORE, round(score, 2)))


def grade_finding(finding: Finding, expected: dict) -> bool:
    line_match = abs(finding.line_number - expected["line"]) <= 1
    category_match = finding.category == expected["category"]
    keyword_match = any(
        kw.lower() in finding.description.lower()
        for kw in expected["keywords"]
    )
    return line_match and category_match and keyword_match


def grade(findings: List[Finding], expected_findings: list) -> float:
    matched = 0
    total = len(expected_findings)

    for expected in expected_findings:
        for finding in findings:
            if grade_finding(finding, expected):
                matched += 1
                break

    false_positives = len(findings) - matched
    base_score = matched / total if total > 0 else MIN_STRICT_SCORE
    final_score = base_score - (0.2 * false_positives)
    return sanitize_score(final_score)

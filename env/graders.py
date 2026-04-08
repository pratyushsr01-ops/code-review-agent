from typing import List
from .models import Finding


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
    base_score = matched / total if total > 0 else 0.0
    final_score = base_score - (0.2 * false_positives)
    return max(0.01, min(0.99, round(final_score, 2)))
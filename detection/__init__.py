"""Source-code preprocessing, AST structural analysis, similarity, and heuristic pattern analysis."""

from detection.ai_pattern_analysis import analyze_ai_patterns
from detection.ast_analysis import analyze_ast
from detection.code_preprocessor import extract_comments_and_docstrings, preprocess_code
from detection.code_quality import audit_code_quality
from detection.code_similarity import compare_multiple_files, compare_two_files

__all__ = [
    "preprocess_code",
    "extract_comments_and_docstrings",
    "analyze_ast",
    "compare_two_files",
    "compare_multiple_files",
    "analyze_ai_patterns",
    "audit_code_quality",
]


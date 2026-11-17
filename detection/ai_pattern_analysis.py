"""
Module 6: Explainable Heuristic AI-Associated Code Pattern Analysis.

IMPORTANT:
- Does NOT claim to prove AI authorship.
- Does NOT output a validated probability of AI generation.
- Explicitly distinguishes AI-associated patterns from clean human coding practices.
"""

from __future__ import annotations

import re
import statistics
from typing import Any

from config import AI_DETECTION_DISCLAIMER, HEURISTIC_LABELS, HEURISTIC_THRESHOLDS
from detection.ast_analysis import analyze_ast
from detection.code_preprocessor import extract_comments_and_docstrings, preprocess_code
from detection.code_similarity import compare_two_files
from utils.helpers import compute_code_hash

GENERIC_AI_IDENTIFIERS: set[str] = {
    "result",
    "output",
    "data",
    "temp",
    "value",
    "values",
    "item",
    "items",
    "helper",
    "current",
    "target",
    "input_data",
    "response",
    "numbers",
    "elements",
}

STEP_COMMENT_PATTERN = re.compile(
    r"#\s*(step\s*\d+|initialize|iterate|check if|return|create|define|loop|calculate|handle|edge case)\b",
    re.IGNORECASE,
)

SNAKE_CASE_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")


def _score_naming_uniformity(identifiers: list[str]) -> dict[str, Any]:
    """Evaluate identifier naming consistency and presence of generic textbook names."""
    unique_ids = [ident for ident in set(identifiers) if len(ident) > 1]
    if not unique_ids:
        return {
            "name": "Naming Uniformity",
            "score": 15.0,
            "weight": 0.22,
            "observation": "Very few multi-character identifiers present.",
            "explanation": "Short snippets with single-letter variables do not exhibit strong naming uniformity.",
            "normal_practice_note": "Consistent snake_case naming is standard PEP 8 practice among experienced Python developers.",
            "evidence": [],
        }

    snake_ratio = sum(1 for i in unique_ids if SNAKE_CASE_PATTERN.match(i)) / len(unique_ids)
    generic_hits = sorted([i for i in unique_ids if i.lower() in GENERIC_AI_IDENTIFIERS])
    generic_ratio = len(generic_hits) / len(unique_ids)
    long_descriptive_ratio = sum(1 for i in unique_ids if "_" in i and len(i) >= 10) / len(unique_ids)

    raw_score = (snake_ratio * 45.0) + (min(generic_ratio * 180.0, 35.0)) + (long_descriptive_ratio * 20.0)
    score = round(min(100.0, max(0.0, raw_score)), 1)

    evidence = [
        f"Snake-case identifier ratio: {snake_ratio * 100:.0f}% ({len(unique_ids)} unique multi-char identifiers).",
    ]
    if generic_hits:
        evidence.append(f"Generic textbook identifiers found: {', '.join(generic_hits[:8])}.")

    return {
        "name": "Naming Uniformity",
        "score": score,
        "weight": 0.22,
        "observation": f"{snake_ratio * 100:.0f}% snake_case adherence; {len(generic_hits)} generic identifier(s).",
        "explanation": (
            "LLM-generated snippets frequently use uniform, verbose snake_case names and "
            "generic placeholders such as 'result', 'data', or 'current_value'."
        ),
        "normal_practice_note": (
            "Readable descriptive snake_case names are also recommended by PEP 8 and taught "
            "in software engineering courses."
        ),
        "evidence": evidence,
    }


def _score_formatting_consistency(code: str) -> dict[str, Any]:
    """Evaluate indentation, blank-line spacing, and line-length uniformity."""
    lines = code.splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    if len(non_empty) < 4:
        return {
            "name": "Formatting Consistency",
            "score": 20.0,
            "weight": 0.18,
            "observation": "File is too short to measure meaningful formatting variance.",
            "explanation": "Formatting heuristics require multi-line structure.",
            "normal_practice_note": "Auto-formatters like Black or Ruff produce equally consistent formatting.",
            "evidence": [],
        }

    indents = [len(ln) - len(ln.lstrip(" ")) for ln in non_empty if ln.startswith(" ")]
    four_space_ratio = (
        sum(1 for ind in indents if ind % 4 == 0) / len(indents)
        if indents
        else 1.0
    )

    trailing_ws_count = sum(1 for ln in lines if ln != ln.rstrip())
    lengths = [len(ln) for ln in non_empty]
    stdev_len = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    # Moderate, clean line lengths without trailing spaces increase uniformity score
    clean_trailing = 1.0 if trailing_ws_count == 0 else max(0.0, 1.0 - (trailing_ws_count / len(lines)))
    compact_variance = 1.0 if stdev_len < 22 else max(0.2, 1.0 - ((stdev_len - 22) / 50.0))

    score = round(min(100.0, (four_space_ratio * 45.0) + (clean_trailing * 30.0) + (compact_variance * 25.0)), 1)

    return {
        "name": "Formatting Consistency",
        "score": score,
        "weight": 0.18,
        "observation": (
            f"4-space indent alignment: {four_space_ratio * 100:.0f}%, "
            f"trailing-whitespace lines: {trailing_ws_count}, line-length stdev: {stdev_len:.1f}."
        ),
        "explanation": (
            "AI assistants typically emit uniformly indented code with zero trailing whitespace "
            "and narrow line-length variation."
        ),
        "normal_practice_note": (
            "IDEs (VS Code, PyCharm) and formatters (Black, Prettier, isort) automatically produce "
            "identical formatting cleanliness on human-written code."
        ),
        "evidence": [
            f"Trailing whitespace lines: {trailing_ws_count} / {len(lines)}",
            f"Indentation 4-space multiples: {four_space_ratio * 100:.0f}%",
        ],
    }


def _score_comment_patterns(code: str, ast_data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate density of step-by-step instructional comments and uniform docstrings."""
    comment_info = extract_comments_and_docstrings(code)
    total_lines = max(1, comment_info["total_lines"])
    comments = comment_info["comments"]
    comment_texts = [c["text"] for c in comments]

    step_matches = [txt for txt in comment_texts if STEP_COMMENT_PATTERN.search(txt)]
    comment_density = len(comments) / total_lines

    funcs = ast_data.get("function_definitions") or []
    docstring_ratio = (
        sum(1 for f in funcs if f.get("has_docstring")) / len(funcs)
        if funcs
        else 0.0
    )

    # Check repeated phrasing prefixes across comments
    prefixes = [" ".join(txt.lstrip("# ").lower().split()[:2]) for txt in comment_texts if len(txt.split()) >= 3]
    repeated_prefixes = len(prefixes) - len(set(prefixes))

    score_raw = (
        min(len(step_matches) * 18.0, 45.0)
        + min(comment_density * 180.0, 25.0)
        + (docstring_ratio * 20.0)
        + min(repeated_prefixes * 10.0, 10.0)
    )
    score = round(min(100.0, max(0.0, score_raw)), 1)

    evidence = [
        f"Comments found: {len(comments)} across {total_lines} lines ({comment_density * 100:.1f}%).",
        f"Instructional/step-style comments: {len(step_matches)}.",
    ]
    if funcs:
        evidence.append(f"Functions with docstrings: {docstring_ratio * 100:.0f}% ({len(funcs)} total).")

    return {
        "name": "Explanatory Comment & Docstring Patterns",
        "score": score,
        "weight": 0.25,
        "observation": f"{len(step_matches)} step/instructional comment(s); {docstring_ratio * 100:.0f}% function docstring coverage.",
        "explanation": (
            "AI-generated solutions often include sequential '# Step 1:', '# Initialize...', or "
            "narrated comments explaining trivial lines alongside complete Args/Returns docstrings."
        ),
        "normal_practice_note": (
            "Thorough documentation and docstrings are best practices in production software and "
            "academic submissions where grading rubrics reward comments."
        ),
        "evidence": evidence,
    }


def _score_structural_regularity(ast_data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate template-like structure, type annotations, and defensive boilerplate."""
    if not ast_data.get("syntax_valid"):
        return {
            "name": "Structural & Template Regularity",
            "score": 10.0,
            "weight": 0.20,
            "observation": "Syntax error prevented full AST structural evaluation.",
            "explanation": "Syntax errors are less typical of complete LLM outputs unless truncated.",
            "normal_practice_note": "Incomplete drafts are common during active human development.",
            "evidence": [],
        }

    funcs = ast_data.get("function_definitions") or []
    annotated_ratio = (
        sum(1 for f in funcs if f.get("has_return_annotation")) / len(funcs)
        if funcs
        else 0.0
    )
    has_doc = bool(ast_data.get("has_module_docstring"))
    has_try = ast_data.get("num_try_except", 0) > 0
    moderate_nesting = 1 <= ast_data.get("max_nesting_depth", 0) <= 4
    low_complexity_per_func = (
        (ast_data.get("approx_cyclomatic_complexity", 1) / max(1, len(funcs))) <= 4.0
        if funcs
        else False
    )

    score_raw = (
        (annotated_ratio * 35.0)
        + (20.0 if has_doc else 0.0)
        + (15.0 if has_try else 0.0)
        + (15.0 if moderate_nesting else 0.0)
        + (15.0 if low_complexity_per_func else 0.0)
    )
    score = round(min(100.0, score_raw), 1)

    return {
        "name": "Structural & Template Regularity",
        "score": score,
        "weight": 0.20,
        "observation": (
            f"Return type annotations: {annotated_ratio * 100:.0f}%, "
            f"module docstring: {'Yes' if has_doc else 'No'}, "
            f"max nesting: {ast_data.get('max_nesting_depth', 0)}."
        ),
        "explanation": (
            "AI assistants frequently structure solutions as modular typed functions with module "
            "docstrings, guard clauses, and balanced shallow nesting."
        ),
        "normal_practice_note": (
            "Clean modular decomposition and Python type hints are standard modern Python habits, "
            "not proof of AI generation."
        ),
        "evidence": [
            f"Functions defined: {len(funcs)}",
            f"Module docstring present: {has_doc}",
            f"Approx. cyclomatic complexity: {ast_data.get('approx_cyclomatic_complexity', 1)}",
        ],
    }


def _score_peer_similarity(
    code: str,
    filename: str,
    peer_codes: list[tuple[str, str]] | None,
) -> dict[str, Any]:
    """Optional indicator comparing against other submitted reference files."""
    if not peer_codes:
        return {
            "name": "Cross-Submission Similarity",
            "score": 0.0,
            "weight": 0.15,
            "observation": "No comparison files provided for cross-submission check.",
            "explanation": "Evaluates structural and token similarity when multiple submissions are supplied.",
            "normal_practice_note": "Independent solutions to the same prompt can naturally share common algorithms.",
            "evidence": [],
        }

    max_sim = 0.0
    top_peer = ""
    for peer_name, peer_code in peer_codes:
        if peer_name == filename and peer_code == code:
            continue
        res = compare_two_files(code, peer_code, name_a=filename, name_b=peer_name, normalize_identifiers=True)
        if res["overall_similarity"] > max_sim:
            max_sim = res["overall_similarity"]
            top_peer = peer_name

    return {
        "name": "Cross-Submission Similarity",
        "score": round(max_sim, 1),
        "weight": 0.15,
        "observation": (
            f"Highest normalized similarity: {max_sim:.1f}% (against '{top_peer}')."
            if top_peer
            else "No distinct peer files compared."
        ),
        "explanation": (
            "Multiple submissions generated from similar prompts often share high structural "
            "and token similarity even with renamed variables."
        ),
        "normal_practice_note": (
            "Standard textbook algorithms (e.g., Kadane's algorithm, binary search) also yield "
            "high similarity across independent human programmers."
        ),
        "evidence": [f"Top peer match: {top_peer} ({max_sim:.1f}%)"] if top_peer else [],
    }


def analyze_ai_patterns(
    code: str,
    filename: str = "<input>",
    peer_codes: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Run explainable heuristic AI-associated code pattern analysis.
    Returns a transparent breakdown with non-probabilistic labels and explicit limitations.
    """
    prep = preprocess_code(code, remove_comments=False, normalize_whitespace=False)
    ast_data = analyze_ast(code, filename=filename)

    ind_naming = _score_naming_uniformity(prep["identifiers"])
    ind_format = _score_formatting_consistency(code)
    ind_comments = _score_comment_patterns(code, ast_data)
    ind_structure = _score_structural_regularity(ast_data)
    ind_similarity = _score_peer_similarity(code, filename, peer_codes)

    active_indicators = [ind_naming, ind_format, ind_comments, ind_structure]
    if peer_codes:
        active_indicators.append(ind_similarity)

    total_weight = sum(ind["weight"] for ind in active_indicators)
    weighted_sum = sum(ind["score"] * ind["weight"] for ind in active_indicators)
    overall_score = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0.0

    if overall_score >= HEURISTIC_THRESHOLDS["several_min"]:
        label = HEURISTIC_LABELS["several"]
    elif overall_score >= HEURISTIC_THRESHOLDS["some_min"]:
        label = HEURISTIC_LABELS["some"]
    else:
        label = HEURISTIC_LABELS["few"]

    all_indicators = [ind_naming, ind_format, ind_comments, ind_structure, ind_similarity]
    influencing = [
        f"{ind['name']} ({ind['score']:.1f}/100): {ind['observation']}"
        for ind in active_indicators
        if ind["score"] >= 35.0
    ]
    if not influencing:
        influencing = ["No strong individual stylistic or structural heuristic indicators exceeded 35/100."]

    limitations = [
        "Heuristic scores measure stylistic and structural traits—not authorship.",
        "Well-formatted human code using PEP 8, type hints, and Black/Ruff can trigger higher indicator scores (false positives).",
        "AI-generated code that has been edited, condensed, or prompted for terse style can yield low scores (false negatives).",
        "This score is NOT a validated probability and must never be used alone for academic or disciplinary decisions.",
    ]

    return {
        "filename": filename,
        "code_hash": compute_code_hash(code),
        "indicator_score": overall_score,
        "classification_label": label,
        "indicators": all_indicators,
        "influencing_characteristics": influencing,
        "ast_summary": ast_data,
        "limitations": limitations,
        "limitations_text": " ".join(limitations),
        "disclaimer": AI_DETECTION_DISCLAIMER,
    }


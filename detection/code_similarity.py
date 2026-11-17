"""
Module 4B: Source-Code Similarity Analysis.
Combines token similarity, TF-IDF cosine similarity, SequenceMatcher ratio,
and AST structural comparison. Explicitly notes that similarity is not proof
of plagiarism.
"""

from __future__ import annotations

import difflib
import math
from collections import Counter
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import SIMILARITY_DISCLAIMER
from detection.ast_analysis import analyze_ast
from detection.code_preprocessor import preprocess_code


def _cosine_from_counters(c1: Counter[str], c2: Counter[str]) -> float:
    """Compute cosine similarity between two frequency counters (0.0 to 1.0)."""
    if not c1 or not c2:
        return 0.0
    common = set(c1.keys()) & set(c2.keys())
    dot = sum(c1[k] * c2[k] for k in common)
    mag1 = math.sqrt(sum(v * v for v in c1.values()))
    mag2 = math.sqrt(sum(v * v for v in c2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def _compute_token_similarity(tokens_a: list[str], tokens_b: list[str]) -> float:
    """Compute blended Jaccard and frequency-cosine token similarity (0-100%)."""
    if not tokens_a or not tokens_b:
        return 0.0
    set_a, set_b = set(tokens_a), set(tokens_b)
    union_len = len(set_a | set_b)
    jaccard = len(set_a & set_b) / union_len if union_len else 0.0
    freq_cos = _cosine_from_counters(Counter(tokens_a), Counter(tokens_b))
    return round(((jaccard + freq_cos) / 2.0) * 100.0, 2)


def _compute_tfidf_similarity(tokens_a: list[str], tokens_b: list[str]) -> float:
    """Compute TF-IDF cosine similarity using scikit-learn (0-100%)."""
    doc_a = " ".join(tokens_a)
    doc_b = " ".join(tokens_b)
    if not doc_a.strip() or not doc_b.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(
            token_pattern=r"(?u)\b\w+\b|[^\w\s]",
            lowercase=False,
        )
        matrix = vectorizer.fit_transform([doc_a, doc_b])
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        return round(max(0.0, min(1.0, score)) * 100.0, 2)
    except ValueError:
        return 0.0


def _compute_sequence_similarity(norm_a: str, norm_b: str) -> tuple[float, list[str]]:
    """Compute difflib SequenceMatcher ratio (0-100%) and matching snippet blocks."""
    if not norm_a or not norm_b:
        return 0.0, []
    matcher = difflib.SequenceMatcher(None, norm_a, norm_b)
    ratio_pct = round(matcher.ratio() * 100.0, 2)

    matching_snippets: list[str] = []
    for block in matcher.get_matching_blocks():
        if block.size >= 24:
            snippet = norm_a[block.a : block.a + block.size].strip()
            if snippet and snippet not in matching_snippets:
                matching_snippets.append(snippet[:260])
        if len(matching_snippets) >= 6:
            break

    return ratio_pct, matching_snippets


def _compute_ast_similarity(ast_a: dict[str, Any], ast_b: dict[str, Any]) -> tuple[float, list[str], list[str]]:
    """
    Compare AST node-type distributions and high-level structural counts.
    Returns (similarity_pct, structural_similarities, structural_differences).
    """
    if not ast_a.get("syntax_valid") or not ast_b.get("syntax_valid"):
        return 0.0, [], ["AST comparison skipped because one or both files contain syntax errors."]

    counts_a = Counter(ast_a.get("node_type_counts") or {})
    counts_b = Counter(ast_b.get("node_type_counts") or {})
    node_cos = _cosine_from_counters(counts_a, counts_b)

    feature_keys = [
        ("num_functions", "Functions"),
        ("num_classes", "Classes"),
        ("num_loops", "Loops"),
        ("num_conditionals", "Conditionals"),
        ("num_imports", "Imports"),
        ("num_assignments", "Assignments"),
        ("max_nesting_depth", "Max Nesting Depth"),
    ]
    vec_sim_parts: list[float] = []
    similarities: list[str] = []
    differences: list[str] = []

    for key, label in feature_keys:
        va = int(ast_a.get(key, 0))
        vb = int(ast_b.get(key, 0))
        if va == vb:
            vec_sim_parts.append(1.0)
            if va > 0:
                similarities.append(f"Both files have {va} {label.lower()}.")
        else:
            denom = max(va, vb, 1)
            vec_sim_parts.append(1.0 - (abs(va - vb) / denom))
            differences.append(f"{label}: {ast_a['filename']} has {va}, while {ast_b['filename']} has {vb}.")

    feature_sim = sum(vec_sim_parts) / len(vec_sim_parts) if vec_sim_parts else 0.0
    blended = ((0.65 * node_cos) + (0.35 * feature_sim)) * 100.0
    return round(blended, 2), similarities, differences


def compare_two_files(
    code_a: str,
    code_b: str,
    name_a: str = "file_1.py",
    name_b: str = "file_2.py",
    normalize_identifiers: bool = False,
) -> dict[str, Any]:
    """
    Perform a comprehensive multi-metric similarity analysis between two Python files.
    """
    prep_a = preprocess_code(
        code_a,
        remove_comments=True,
        normalize_whitespace=True,
        normalize_identifiers=normalize_identifiers,
    )
    prep_b = preprocess_code(
        code_b,
        remove_comments=True,
        normalize_whitespace=True,
        normalize_identifiers=normalize_identifiers,
    )

    ast_a = analyze_ast(code_a, filename=name_a)
    ast_b = analyze_ast(code_b, filename=name_b)

    token_sim = _compute_token_similarity(prep_a["tokens"], prep_b["tokens"])
    tfidf_sim = _compute_tfidf_similarity(prep_a["tokens"], prep_b["tokens"])
    seq_sim, matching_blocks = _compute_sequence_similarity(
        prep_a["normalized_code"], prep_b["normalized_code"]
    )
    ast_sim, struct_similarities, struct_differences = _compute_ast_similarity(ast_a, ast_b)

    if ast_a["syntax_valid"] and ast_b["syntax_valid"]:
        overall = round(
            0.25 * token_sim + 0.25 * tfidf_sim + 0.20 * seq_sim + 0.30 * ast_sim,
            2,
        )
    else:
        overall = round(
            0.35 * token_sim + 0.35 * tfidf_sim + 0.30 * seq_sim,
            2,
        )

    diff_lines = list(
        difflib.unified_diff(
            code_a.splitlines(),
            code_b.splitlines(),
            fromfile=name_a,
            tofile=name_b,
            lineterm="",
            n=2,
        )
    )[:120]

    if overall >= 75:
        band = "High similarity"
    elif overall >= 45:
        band = "Moderate similarity"
    else:
        band = "Low similarity"

    mode_note = (
        "with identifier normalization enabled"
        if normalize_identifiers
        else "using original identifier names"
    )
    summary_text = (
        f"{band} ({overall:.1f}%) between '{name_a}' and '{name_b}' ({mode_note}). "
        f"Token: {token_sim:.1f}%, TF-IDF: {tfidf_sim:.1f}%, "
        f"Sequence: {seq_sim:.1f}%, AST Structure: {ast_sim:.1f}%."
    )

    return {
        "file_a": name_a,
        "file_b": name_b,
        "overall_similarity": overall,
        "similarity_band": band,
        "token_similarity": token_sim,
        "tfidf_similarity": tfidf_sim,
        "sequence_similarity": seq_sim,
        "ast_similarity": ast_sim,
        "normalized_var_mode": normalize_identifiers,
        "summary_text": summary_text,
        "matching_sections": matching_blocks,
        "structural_similarities": struct_similarities,
        "structural_differences": struct_differences,
        "diff_lines": diff_lines,
        "ast_a": ast_a,
        "ast_b": ast_b,
        "disclaimer": SIMILARITY_DISCLAIMER,
    }


def compare_multiple_files(
    files: list[tuple[str, str]],
    normalize_identifiers: bool = False,
) -> dict[str, Any]:
    """
    Compare 2 or more (filename, code) pairs, returning pairwise results
    and an NxN similarity matrix.
    """
    names = [name for name, _ in files]
    n = len(files)
    matrix: list[list[float]] = [[100.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    pair_results: list[dict[str, Any]] = []

    for i in range(n):
        for j in range(i + 1, n):
            res = compare_two_files(
                files[i][1],
                files[j][1],
                name_a=files[i][0],
                name_b=files[j][0],
                normalize_identifiers=normalize_identifiers,
            )
            matrix[i][j] = res["overall_similarity"]
            matrix[j][i] = res["overall_similarity"]
            pair_results.append(res)

    return {
        "filenames": names,
        "similarity_matrix": matrix,
        "pair_results": pair_results,
        "disclaimer": SIMILARITY_DISCLAIMER,
    }


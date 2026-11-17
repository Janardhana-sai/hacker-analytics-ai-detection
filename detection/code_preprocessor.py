"""
Module 4A: Python Source-Code Preprocessing.
Handles comment removal, whitespace normalization, tokenization, and optional
identifier normalization while preserving Python keywords and built-in names.
"""

from __future__ import annotations

import builtins
import io
import keyword
import re
import tokenize
from typing import Any

PYTHON_KEYWORDS: set[str] = set(keyword.kwlist)
PYTHON_BUILTINS: set[str] = set(dir(builtins))


def extract_comments_and_docstrings(code: str) -> dict[str, Any]:
    """Extract inline/block comments and line statistics from Python source code."""
    lines = code.splitlines()
    comment_lines: list[dict[str, Any]] = []
    blank_lines = 0

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            blank_lines += 1
        elif stripped.startswith("#"):
            comment_lines.append({"line": idx, "text": stripped})

    # Also catch inline trailing comments safely via tokenize
    inline_comments: list[dict[str, Any]] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        for tok_type, tok_str, start, _, _ in tokens:
            if tok_type == tokenize.COMMENT:
                inline_comments.append({"line": start[0], "text": tok_str.strip()})
    except (tokenize.TokenError, IndentationError):
        pass

    return {
        "total_lines": len(lines),
        "blank_lines": blank_lines,
        "comment_count": len(inline_comments) if inline_comments else len(comment_lines),
        "comments": inline_comments if inline_comments else comment_lines,
    }


def preprocess_code(
    code: str,
    remove_comments: bool = True,
    normalize_whitespace: bool = True,
    normalize_identifiers: bool = False,
) -> dict[str, Any]:
    """
    Clean and tokenize Python source code for similarity and pattern analysis.
    Falls back to regex tokenization if the code contains syntax/token errors.
    """
    working_code = code.replace("\r\n", "\n").replace("\r", "\n")
    tokens_list: list[str] = []
    identifiers: list[str] = []
    var_map: dict[str, str] = {}
    var_counter = 1

    try:
        tok_stream = list(tokenize.generate_tokens(io.StringIO(working_code).readline))
        rebuilt_parts: list[str] = []

        for tok_type, tok_str, _, _, _ in tok_stream:
            if tok_type in (tokenize.ENCODING, tokenize.ENDMARKER):
                continue
            if tok_type == tokenize.COMMENT and remove_comments:
                continue
            if tok_type in (tokenize.NL, tokenize.NEWLINE):
                if not normalize_whitespace:
                    rebuilt_parts.append("\n")
                elif rebuilt_parts and rebuilt_parts[-1] != "\n":
                    rebuilt_parts.append("\n")
                continue
            if tok_type in (tokenize.INDENT, tokenize.DEDENT):
                continue

            token_value = tok_str
            if tok_type == tokenize.NAME:
                if tok_str not in PYTHON_KEYWORDS and tok_str not in PYTHON_BUILTINS:
                    identifiers.append(tok_str)
                    if normalize_identifiers:
                        if tok_str not in var_map:
                            var_map[tok_str] = f"VAR_{var_counter}"
                            var_counter += 1
                        token_value = var_map[tok_str]

            tokens_list.append(token_value)
            rebuilt_parts.append(token_value)

        normalized_text = " ".join(rebuilt_parts)
        if normalize_whitespace:
            normalized_text = re.sub(r"[ \t]+", " ", normalized_text)
            normalized_text = re.sub(r" *\n *", "\n", normalized_text).strip()

    except (tokenize.TokenError, IndentationError):
        # Graceful fallback for incomplete/invalid snippets
        fallback = working_code
        if remove_comments:
            fallback = re.sub(r"#.*", "", fallback)
        if normalize_whitespace:
            fallback = "\n".join(
                re.sub(r"[ \t]+", " ", ln).strip()
                for ln in fallback.splitlines()
                if ln.strip()
            )
        raw_tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|[^\sA-Za-z0-9_]", fallback)
        for tok in raw_tokens:
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", tok):
                if tok not in PYTHON_KEYWORDS and tok not in PYTHON_BUILTINS:
                    identifiers.append(tok)
                    if normalize_identifiers:
                        if tok not in var_map:
                            var_map[tok] = f"VAR_{var_counter}"
                            var_counter += 1
                        tok = var_map[tok]
            tokens_list.append(tok)
        normalized_text = fallback

    return {
        "normalized_code": normalized_text,
        "tokens": tokens_list,
        "token_count": len(tokens_list),
        "identifiers": identifiers,
        "unique_identifiers": sorted(set(identifiers)),
        "identifier_map": var_map,
    }


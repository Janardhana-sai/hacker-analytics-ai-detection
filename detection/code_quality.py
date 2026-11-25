"""
Module: Code Quality, Cyclomatic Complexity, Halstead Metrics & Static Security Audit.
Performs AST-driven software engineering metrics calculation, maintainability indexing,
and security vulnerability pattern detection on Python source code.
"""

from __future__ import annotations

import ast
import math
import re
from typing import Any


class CodeQualityAuditor(ast.NodeVisitor):
    """AST visitor to compute McCabe's Cyclomatic Complexity and detect code smells."""

    DECISION_NODES = (
        ast.If,
        ast.While,
        ast.For,
        ast.AsyncFor,
        ast.ExceptHandler,
        ast.With,
        ast.AsyncWith,
        ast.Assert,
    )

    COMPREHENSION_NODES = (
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
    )

    DANGEROUS_FUNCTIONS = {
        "eval": "High risk of arbitrary code execution.",
        "exec": "Dynamic code execution can lead to severe security compromise.",
        "os.system": "Command injection vulnerability. Prefer subprocess with shell=False.",
        "subprocess.Popen": "Verify shell=False to prevent shell command injection.",
        "__import__": "Dynamic import manipulation vulnerability.",
        "pickle.loads": "Insecure deserialization risk from untrusted input.",
    }

    def __init__(self) -> None:
        self.overall_complexity: int = 1
        self.functions: list[dict[str, Any]] = []
        self.security_issues: list[dict[str, Any]] = []
        self.code_smells: list[dict[str, Any]] = []
        self.total_operators: int = 0
        self.total_operands: int = 0
        self.unique_operators: set[str] = set()
        self.unique_operands: set[str] = set()
        self.max_nesting_depth: int = 0
        self._current_nesting: int = 0

    def generic_visit(self, node: ast.AST) -> None:
        is_nest = isinstance(node, (ast.If, ast.While, ast.For, ast.FunctionDef, ast.ClassDef, ast.Try))
        if is_nest:
            self._current_nesting += 1
            if self._current_nesting > self.max_nesting_depth:
                self.max_nesting_depth = self._current_nesting

        # McCabe Decision points
        if isinstance(node, self.DECISION_NODES):
            self.overall_complexity += 1
        elif isinstance(node, ast.BoolOp):
            # and / or add complexity
            self.overall_complexity += len(node.values) - 1
        elif isinstance(node, self.COMPREHENSION_NODES):
            self.overall_complexity += len(node.generators)

        # Halstead Operators
        if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
            self.total_operators += 1
            self.unique_operators.add(type(node).__name__)
        elif isinstance(node, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn)):
            self.total_operators += 1
            self.unique_operators.add(type(node).__name__)

        # Halstead Operands
        if isinstance(node, ast.Name):
            self.total_operands += 1
            self.unique_operands.add(node.id)
        elif isinstance(node, ast.Constant):
            self.total_operands += 1
            self.unique_operands.add(str(node.value))

        super().generic_visit(node)

        if is_nest:
            self._current_nesting -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._inspect_function(node, is_async=False)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._inspect_function(node, is_async=True)
        self.generic_visit(node)

    def _inspect_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool) -> None:
        fn_complexity = 1
        for sub in ast.walk(node):
            if sub is not node and isinstance(sub, self.DECISION_NODES):
                fn_complexity += 1
            elif isinstance(sub, ast.BoolOp):
                fn_complexity += len(sub.values) - 1
            elif isinstance(sub, self.COMPREHENSION_NODES):
                fn_complexity += len(sub.generators)

        # Lines count
        lines_count = getattr(node, "end_lineno", node.lineno) - node.lineno + 1

        self.functions.append(
            {
                "name": node.name,
                "line_number": node.lineno,
                "lines_count": lines_count,
                "complexity": fn_complexity,
                "args_count": len(node.args.args),
                "is_async": is_async,
                "has_docstring": ast.get_docstring(node) is not None,
                "risk_rating": "Low" if fn_complexity <= 5 else ("Medium" if fn_complexity <= 10 else "High"),
            }
        )

    def visit_Call(self, node: ast.Call) -> None:
        fn_name = ""
        if isinstance(node.func, ast.Name):
            fn_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                fn_name = f"{node.func.value.id}.{node.func.attr}"
            else:
                fn_name = node.func.attr

        if fn_name in self.DANGEROUS_FUNCTIONS:
            self.security_issues.append(
                {
                    "type": "Dangerous Function Call",
                    "target": fn_name,
                    "line": getattr(node, "lineno", 1),
                    "severity": "High" if "eval" in fn_name or "exec" in fn_name else "Medium",
                    "description": self.DANGEROUS_FUNCTIONS[fn_name],
                }
            )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is None:
            self.code_smells.append(
                {
                    "type": "Bare Except Clause",
                    "line": getattr(node, "lineno", 1),
                    "severity": "Medium",
                    "description": "Catching all exceptions with bare 'except:' masks KeyboardInterrupt and SystemExit.",
                }
            )
        self.generic_visit(node)


def audit_code_quality(source_code: str) -> dict[str, Any]:
    """
    Perform deep static analysis, McCabe Cyclomatic Complexity, Halstead volume,
    Maintainability Index (MI), and security risk detection.
    """
    if not source_code or not source_code.strip():
        return {
            "syntax_valid": False,
            "error_message": "Source code is empty.",
            "maintainability_index": 0.0,
            "overall_complexity": 0,
            "functions": [],
            "security_issues": [],
            "code_smells": [],
            "halstead": {},
        }

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {
            "syntax_valid": False,
            "error_message": f"Syntax error at line {e.lineno}: {e.msg}",
            "maintainability_index": 0.0,
            "overall_complexity": 0,
            "functions": [],
            "security_issues": [],
            "code_smells": [],
            "halstead": {},
        }

    auditor = CodeQualityAuditor()
    auditor.visit(tree)

    # Line counts
    lines = source_code.splitlines()
    loc = len(lines)
    sloc = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
    blank_lines = len([l for l in lines if not l.strip()])
    comment_lines = len([l for l in lines if l.strip().startswith("#")])

    # Halstead Metrics
    n1 = max(1, len(auditor.unique_operators))
    n2 = max(1, len(auditor.unique_operands))
    N1 = max(1, auditor.total_operators)
    N2 = max(1, auditor.total_operands)

    vocabulary = n1 + n2
    length = N1 + N2
    # Volume V = N * log2(n)
    volume = length * math.log2(vocabulary) if vocabulary > 1 else 10.0
    difficulty = (n1 / 2.0) * (N2 / float(n2)) if n2 > 0 else 1.0
    effort = difficulty * volume

    # Maintainability Index (Coleman-Oman standard formula normalized 0-100)
    # MI = 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(LOC)
    safe_loc = max(1, sloc)
    safe_vol = max(1.0, volume)
    raw_mi = 171.0 - 5.2 * math.log(safe_vol) - 0.23 * auditor.overall_complexity - 16.2 * math.log(safe_loc)
    mi_score = max(0.0, min(100.0, (raw_mi * 100.0) / 171.0))

    # Detect hardcoded secret patterns
    secret_pattern = re.compile(
        r"(?i)(api[_-]?key|secret|password|passwd|auth[_-]?token|bearer)\s*=\s*['\"][A-Za-z0-9_\-]{8,}['\"]"
    )
    for idx, line in enumerate(lines, start=1):
        if secret_pattern.search(line):
            auditor.security_issues.append(
                {
                    "type": "Possible Hardcoded Credential / Secret",
                    "target": "Secret String",
                    "line": idx,
                    "severity": "High",
                    "description": "Detected hardcoded key or password token. Use environment variables instead.",
                }
            )

    # Check excessive nesting
    if auditor.max_nesting_depth > 4:
        auditor.code_smells.append(
            {
                "type": "Excessive Control Nesting",
                "line": 1,
                "severity": "Low",
                "description": f"Maximum control flow nesting depth is {auditor.max_nesting_depth} (> 4). Consider early returns or helper functions.",
            }
        )

    # Maintainability Grade
    if mi_score >= 80.0:
        mi_grade = "A (Highly Maintainable)"
        mi_color = "#10B981"
    elif mi_score >= 60.0:
        mi_grade = "B (Moderately Maintainable)"
        mi_color = "#3B82F6"
    elif mi_score >= 40.0:
        mi_grade = "C (Needs Refactoring)"
        mi_color = "#F59E0B"
    else:
        mi_grade = "D (Difficult to Maintain)"
        mi_color = "#EF4444"

    return {
        "syntax_valid": True,
        "error_message": None,
        "maintainability_index": round(mi_score, 1),
        "maintainability_grade": mi_grade,
        "maintainability_color": mi_color,
        "overall_complexity": auditor.overall_complexity,
        "max_nesting_depth": auditor.max_nesting_depth,
        "lines_of_code": loc,
        "source_lines": sloc,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "functions": auditor.functions,
        "security_issues": auditor.security_issues,
        "code_smells": auditor.code_smells,
        "halstead": {
            "vocabulary": vocabulary,
            "length": length,
            "volume": round(volume, 1),
            "difficulty": round(difficulty, 1),
            "effort": round(effort, 1),
        },
    }

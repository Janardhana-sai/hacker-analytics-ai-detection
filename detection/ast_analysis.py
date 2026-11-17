"""
Module 5: AST-Based Python Source-Code Structural Analysis.
Extracts functions, classes, loops, conditionals, imports, variable assignments,
nesting depth, and complexity indicators while handling SyntaxErrors gracefully.
"""

from __future__ import annotations

import ast
from collections import Counter
from typing import Any

from detection.code_preprocessor import extract_comments_and_docstrings
from utils.helpers import compute_code_hash


class _ASTMetricsVisitor(ast.NodeVisitor):
    """Walks a Python AST to collect structural features and nesting depth."""

    CONTROL_NODES = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.With,
        ast.AsyncWith,
        ast.Try,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
    )

    def __init__(self) -> None:
        self.num_functions = 0
        self.num_async_functions = 0
        self.num_classes = 0
        self.num_loops = 0
        self.num_conditionals = 0
        self.num_imports = 0
        self.num_assignments = 0
        self.num_try_except = 0
        self.num_comprehensions = 0
        self.branch_points = 0
        self.current_depth = 0
        self.max_nesting_depth = 0
        self.function_definitions: list[dict[str, Any]] = []
        self.class_definitions: list[dict[str, Any]] = []
        self.imported_modules: list[str] = []
        self.node_type_counts: Counter[str] = Counter()

    def generic_visit(self, node: ast.AST) -> None:
        self.node_type_counts[type(node).__name__] += 1
        is_nested = isinstance(node, self.CONTROL_NODES)
        if is_nested:
            self.current_depth += 1
            if self.current_depth > self.max_nesting_depth:
                self.max_nesting_depth = self.current_depth

        super().generic_visit(node)

        if is_nested:
            self.current_depth -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.num_functions += 1
        self.function_definitions.append(
            {
                "name": node.name,
                "args_count": len(node.args.args) + len(node.args.kwonlyargs),
                "line_number": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None,
                "has_return_annotation": node.returns is not None,
                "is_async": False,
            }
        )
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.num_functions += 1
        self.num_async_functions += 1
        self.function_definitions.append(
            {
                "name": node.name,
                "args_count": len(node.args.args) + len(node.args.kwonlyargs),
                "line_number": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None,
                "has_return_annotation": node.returns is not None,
                "is_async": True,
            }
        )
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.num_classes += 1
        self.class_definitions.append(
            {
                "name": node.name,
                "line_number": node.lineno,
                "bases_count": len(node.bases),
                "has_docstring": ast.get_docstring(node) is not None,
            }
        )
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.num_loops += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.num_loops += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.num_loops += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.num_conditionals += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.num_conditionals += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        self.num_imports += len(node.names)
        for alias in node.names:
            self.imported_modules.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.num_imports += len(node.names)
        mod = node.module or ""
        for alias in node.names:
            self.imported_modules.append(f"{mod}.{alias.name}".strip("."))
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        self.num_assignments += 1
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.num_assignments += 1
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.num_assignments += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        self.num_try_except += 1
        self.branch_points += max(1, len(node.handlers))
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.branch_points += max(0, len(node.values) - 1)
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)


def analyze_ast(code: str, filename: str = "<input>") -> dict[str, Any]:
    """
    Parse Python source code into an AST and extract structural metrics.
    Gracefully handles SyntaxError without raising.
    """
    line_stats = extract_comments_and_docstrings(code)
    code_hash = compute_code_hash(code)

    base_result: dict[str, Any] = {
        "filename": filename,
        "code_hash": code_hash,
        "syntax_valid": True,
        "syntax_error": None,
        "lines_of_code": line_stats["total_lines"],
        "blank_lines": line_stats["blank_lines"],
        "comment_lines": line_stats["comment_count"],
        "num_functions": 0,
        "num_async_functions": 0,
        "num_classes": 0,
        "num_loops": 0,
        "num_conditionals": 0,
        "num_imports": 0,
        "num_assignments": 0,
        "num_try_except": 0,
        "num_comprehensions": 0,
        "max_nesting_depth": 0,
        "approx_cyclomatic_complexity": 1,
        "complexity_level": "Low",
        "function_definitions": [],
        "class_definitions": [],
        "imported_modules": [],
        "has_module_docstring": False,
        "node_type_counts": {},
    }

    try:
        tree = ast.parse(code, filename=filename)
    except SyntaxError as exc:
        base_result["syntax_valid"] = False
        base_result["syntax_error"] = {
            "message": exc.msg,
            "line": exc.lineno,
            "offset": exc.offset,
            "text": (exc.text or "").strip(),
        }
        return base_result

    visitor = _ASTMetricsVisitor()
    visitor.visit(tree)

    complexity = 1 + visitor.branch_points
    if complexity <= 5:
        level = "Low"
    elif complexity <= 12:
        level = "Moderate"
    else:
        level = "High"

    base_result.update(
        {
            "num_functions": visitor.num_functions,
            "num_async_functions": visitor.num_async_functions,
            "num_classes": visitor.num_classes,
            "num_loops": visitor.num_loops,
            "num_conditionals": visitor.num_conditionals,
            "num_imports": visitor.num_imports,
            "num_assignments": visitor.num_assignments,
            "num_try_except": visitor.num_try_except,
            "num_comprehensions": visitor.num_comprehensions,
            "max_nesting_depth": visitor.max_nesting_depth,
            "approx_cyclomatic_complexity": complexity,
            "complexity_level": level,
            "function_definitions": visitor.function_definitions,
            "class_definitions": visitor.class_definitions,
            "imported_modules": visitor.imported_modules,
            "has_module_docstring": ast.get_docstring(tree) is not None,
            "node_type_counts": dict(visitor.node_type_counts),
        }
    )
    return base_result


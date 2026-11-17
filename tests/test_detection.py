"""Unit tests for code preprocessing, AST analysis, similarity, and heuristic AI patterns."""

from __future__ import annotations

import unittest

from config import SAMPLE_DATA_DIR
from detection.ai_pattern_analysis import analyze_ai_patterns
from detection.ast_analysis import analyze_ast
from detection.code_preprocessor import preprocess_code
from detection.code_similarity import compare_multiple_files, compare_two_files


class TestDetectionModules(unittest.TestCase):
    def setUp(self) -> None:
        self.code1 = (SAMPLE_DATA_DIR / "sample_code_1.py").read_text(encoding="utf-8")
        self.code2 = (SAMPLE_DATA_DIR / "sample_code_2.py").read_text(encoding="utf-8")

    def test_preprocessor_and_identifier_normalization(self) -> None:
        raw = "# A comment\ndef add_nums(alpha, beta):\n    total = alpha + beta\n    return total\n"
        res_plain = preprocess_code(raw, remove_comments=True, normalize_identifiers=False)
        self.assertNotIn("comment", res_plain["normalized_code"])
        self.assertIn("alpha", res_plain["tokens"])

        res_norm = preprocess_code(raw, remove_comments=True, normalize_identifiers=True)
        self.assertNotIn("alpha", res_norm["tokens"])
        self.assertIn("VAR_1", res_norm["tokens"])

    def test_ast_analysis_valid_and_invalid_syntax(self) -> None:
        ast_ok = analyze_ast(self.code1, filename="sample_code_1.py")
        self.assertTrue(ast_ok["syntax_valid"])
        self.assertEqual(ast_ok["num_functions"], 2)
        self.assertGreaterEqual(ast_ok["num_loops"], 2)
        self.assertGreaterEqual(ast_ok["num_conditionals"], 2)

        ast_bad = analyze_ast("def broken(:\n    pass\n", filename="broken.py")
        self.assertFalse(ast_bad["syntax_valid"])
        self.assertIsNotNone(ast_bad["syntax_error"])

    def test_code_similarity_metrics(self) -> None:
        identical = compare_two_files(self.code1, self.code1, "f1.py", "f1_copy.py")
        self.assertGreaterEqual(identical["overall_similarity"], 99.0)

        diff_pair = compare_two_files(
            self.code1, self.code2, "sample_code_1.py", "sample_code_2.py", normalize_identifiers=True
        )
        self.assertGreater(diff_pair["overall_similarity"], 20.0)
        self.assertIn("NOT proof of plagiarism", diff_pair["disclaimer"])

        multi = compare_multiple_files(
            [("sample_code_1.py", self.code1), ("sample_code_2.py", self.code2)]
        )
        self.assertEqual(len(multi["pair_results"]), 1)
        self.assertEqual(len(multi["similarity_matrix"]), 2)

    def test_heuristic_ai_pattern_analysis(self) -> None:
        res1 = analyze_ai_patterns(
            self.code1,
            filename="sample_code_1.py",
            peer_codes=[("sample_code_2.py", self.code2)],
        )
        self.assertGreaterEqual(res1["indicator_score"], 0.0)
        self.assertLessEqual(res1["indicator_score"], 100.0)
        self.assertIn(
            res1["classification_label"],
            {
                "Few indicators observed",
                "Some indicators observed",
                "Several indicators observed",
            },
        )
        self.assertGreaterEqual(len(res1["indicators"]), 4)
        self.assertGreater(len(res1["limitations"]), 0)


if __name__ == "__main__":
    unittest.main()


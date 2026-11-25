"""
Unit tests for detection/code_quality.py: Cyclomatic Complexity, Maintainability Index,
Halstead Software Science, and security pattern audits.
"""

import unittest
from detection.code_quality import audit_code_quality


class TestCodeQuality(unittest.TestCase):

    def test_clean_function(self):
        code = '''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''
        res = audit_code_quality(code)
        self.assertTrue(res["syntax_valid"])
        self.assertGreaterEqual(res["maintainability_index"], 80.0)
        self.assertEqual(res["overall_complexity"], 1)
        self.assertEqual(len(res["functions"]), 1)
        self.assertEqual(res["functions"][0]["name"], "add")
        self.assertEqual(res["functions"][0]["complexity"], 1)
        self.assertEqual(len(res["security_issues"]), 0)

    def test_complex_and_dangerous_code(self):
        code = '''
def dangerous_runner(payload, cmd, items):
    # Decision points
    if payload:
        for x in items:
            while x > 0:
                if x % 2 == 0:
                    x -= 1
    try:
        res = eval(payload)
        password = "super_secret_password_12345"
    except:
        pass
    return None
'''
        res = audit_code_quality(code)
        self.assertTrue(res["syntax_valid"])
        self.assertGreater(res["overall_complexity"], 4)
        
        # Check security issue detected (eval)
        sec_types = [s["type"] for s in res["security_issues"]]
        self.assertIn("Dangerous Function Call", sec_types)
        
        # Check hardcoded credential detected
        self.assertIn("Possible Hardcoded Credential / Secret", sec_types)
        
        # Check bare except detected
        smell_types = [s["type"] for s in res["code_smells"]]
        self.assertIn("Bare Except Clause", smell_types)

    def test_syntax_error_handling(self):
        bad_code = "def invalid_syntax(:"
        res = audit_code_quality(bad_code)
        self.assertFalse(res["syntax_valid"])
        self.assertIn("Syntax error", res["error_message"])


if __name__ == "__main__":
    unittest.main()

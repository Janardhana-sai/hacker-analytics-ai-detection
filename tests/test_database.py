"""Unit tests for the SQLite database layer."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from database.db_manager import DatabaseManager
from database.schema import ALL_TABLES


class TestDatabaseManager(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "test_hackerrank.db"
        self.db = DatabaseManager(self.db_path)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_all_tables_created(self) -> None:
        with self.db.get_connection() as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            table_names = {r["name"] for r in rows}
        for required in ALL_TABLES:
            self.assertIn(required, table_names)

    def test_profile_upsert_and_duplicate_handling(self) -> None:
        profile_v1 = {
            "username": "test_coder",
            "display_name": "Test Coder",
            "profile_url": "https://www.hackerrank.com/profile/test_coder",
            "description": "Initial bio",
            "country": "India",
            "is_sample": False,
            "programming_languages": [{"language_name": "Python", "problems_solved": 40}],
            "skills": [{"skill_name": "Python (Basic)", "verified": True}],
            "badges": [{"title": "Python", "level_or_stars": "4 Stars"}],
            "certificates": [],
            "statistics": [{"stat_name": "Total Badges", "stat_value": "1"}],
        }
        pid1 = self.db.upsert_profile(profile_v1)

        # Upsert same username (different case) -> should update, not duplicate
        profile_v2 = dict(profile_v1)
        profile_v2["username"] = "TEST_CODER"
        profile_v2["description"] = "Updated bio"
        profile_v2["programming_languages"] = [
            {"language_name": "Python", "problems_solved": 55},
            {"language_name": "SQL", "problems_solved": 20},
        ]
        pid2 = self.db.upsert_profile(profile_v2)

        self.assertEqual(pid1, pid2)
        fetched = self.db.get_profile_by_username("test_coder")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["description"], "Updated bio")
        self.assertEqual(len(fetched["programming_languages"]), 2)

    def test_scraping_history_and_code_analysis_storage(self) -> None:
        self.db.log_scraping_attempt(
            username="nonexistent_user",
            status="not_found",
            source_mode="live",
            fields_collected=0,
            error_message="404 Not Found",
            duration_seconds=1.25,
        )
        history = self.db.get_scraping_history(status_filter="not_found")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["username"], "nonexistent_user")

        self.db.save_code_analysis(
            {
                "filename": "example.py",
                "code_hash": "abc123",
                "lines_of_code": 20,
                "num_functions": 2,
                "syntax_valid": True,
            }
        )
        self.db.save_similarity_result(
            {
                "file_a": "a.py",
                "file_b": "b.py",
                "overall_similarity": 72.5,
                "token_similarity": 70.0,
                "tfidf_similarity": 75.0,
                "sequence_similarity": 68.0,
                "ast_similarity": 76.0,
            }
        )
        self.db.save_ai_pattern_result(
            {
                "filename": "a.py",
                "indicator_score": 45.0,
                "classification_label": "Some indicators observed",
            }
        )

        counts = self.db.get_dashboard_counts()
        self.assertEqual(counts["total_scrapes"], 1)
        self.assertEqual(counts["total_code_analyses"], 1)
        self.assertEqual(counts["total_similarities"], 1)
        self.assertEqual(counts["total_ai_analyses"], 1)


if __name__ == "__main__":
    unittest.main()


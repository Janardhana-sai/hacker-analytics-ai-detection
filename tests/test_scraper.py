"""Unit tests for URL validation, response classification, JSON/CSV uploads, and scraper workflow."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from database.db_manager import DatabaseManager
from scraper.hackerrank_scraper import HackerRankScraper
from scraper.scraper_utils import (
    build_sample_csv_template,
    build_sample_json_template,
    classify_page_response,
    parse_uploaded_profile_csv,
    parse_uploaded_profile_json,
)
from utils.validators import validate_and_parse_profile_input


class TestScraperImprovements(unittest.TestCase):
    def test_url_and_username_validation(self) -> None:
        ok, info = validate_and_parse_profile_input(
            "https://www.hackerrank.com/profile/sample_coder_123/?hr_r=1"
        )
        self.assertTrue(ok)
        self.assertEqual(info["username"], "sample_coder_123")
        self.assertEqual(
            info["profile_url"], "https://www.hackerrank.com/profile/sample_coder_123"
        )

        ok2, info2 = validate_and_parse_profile_input("hackerrank.com/profile/alice_dev")
        self.assertTrue(ok2)
        self.assertEqual(info2["username"], "alice_dev")

        bad_host, err_host = validate_and_parse_profile_input("https://example.com/profile/alice")
        self.assertFalse(bad_host)
        self.assertIn("Invalid profile URL host", err_host["error"])

        bad_reserved, err_res = validate_and_parse_profile_input("https://www.hackerrank.com/login")
        self.assertFalse(bad_reserved)
        self.assertIn("valid HackerRank user profile", err_res["error"])

    def test_response_classification_distinguishes_errors(self) -> None:
        # 1. Network error page
        st_net, _ = classify_page_response(
            "<html><body>This site can't be reached ERR_NAME_NOT_RESOLVED</body></html>",
            current_url="chrome-error://chromewebdata/",
            page_title="www.hackerrank.com",
        )
        self.assertEqual(st_net, "network_error")

        # 2. Genuine access denied
        st_res, _ = classify_page_response(
            "<html><head><title>Access Denied</title></head><body>You don't have permission to access.</body></html>",
            current_url="https://www.hackerrank.com/profile/foo",
            page_title="Access Denied",
        )
        self.assertEqual(st_res, "restricted")

        # 3. 404 Not Found
        st_404, _ = classify_page_response(
            "<html><head><title>Page Not Found | HackerRank</title></head><body>We could not find the page you were looking for.</body></html>",
            current_url="https://www.hackerrank.com/profile/missing_user",
            page_title="Page Not Found | HackerRank",
        )
        self.assertEqual(st_404, "not_found")

        # 4. Normal page that happens to mention 'access denied' inside inline JS must NOT be marked restricted
        large_body = " ".join(["profile content"] * 300)
        st_ok, _ = classify_page_response(
            f"<html><head><title>Alice | HackerRank</title><script>var msg='access denied';</script></head><body><h1>Alice</h1><p>{large_body}</p></body></html>",
            current_url="https://www.hackerrank.com/profile/alice",
            page_title="Alice | HackerRank",
        )
        self.assertEqual(st_ok, "ok")

    def test_json_and_csv_profile_uploads(self) -> None:
        json_profiles = parse_uploaded_profile_json(build_sample_json_template())
        self.assertEqual(len(json_profiles), 1)
        self.assertEqual(json_profiles[0]["username"], "example_public_user")
        self.assertEqual(json_profiles[0]["source_label"], "uploaded")
        self.assertFalse(json_profiles[0]["is_sample"])

        csv_profiles = parse_uploaded_profile_csv(build_sample_csv_template())
        self.assertEqual(len(csv_profiles), 1)
        self.assertEqual(csv_profiles[0]["username"], "example_public_user")
        self.assertEqual(len(csv_profiles[0]["programming_languages"]), 2)
        self.assertEqual(csv_profiles[0]["programming_languages"][0]["problems_solved"], 85)

    def test_offline_sample_workflow_and_last_success_timestamp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = DatabaseManager(Path(tmp) / "test.db")
            self.assertIsNone(db.get_last_successful_scrape_time())

            res = HackerRankScraper.load_sample_profile("aarav_py_dev")
            self.assertTrue(res.success)
            pid = db.upsert_profile(res.profile_data)
            db.log_scraping_attempt(
                username=res.username,
                status="success",
                source_mode="sample",
                profile_id=pid,
                fields_collected=res.fields_collected,
                scraped_at=res.scraped_at,
            )
            self.assertIsNotNone(db.get_last_successful_scrape_time())
            self.assertIsNone(db.get_last_successful_scrape_time(source_mode="live"))


if __name__ == "__main__":
    unittest.main()


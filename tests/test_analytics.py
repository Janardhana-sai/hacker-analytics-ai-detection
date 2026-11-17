"""Unit tests for profile analytics, coding charts, and scraper utilities."""

from __future__ import annotations

import unittest

from analytics.coding_analytics import (
    build_badge_and_achievement_summary,
    build_language_distribution,
    build_profile_comparison_df,
    build_skill_distribution,
    create_comparison_chart,
    create_language_bar_chart,
    create_language_pie_chart,
    create_matplotlib_language_summary,
)
from analytics.profile_analysis import analyze_single_profile
from scraper.hackerrank_scraper import HackerRankScraper
from scraper.scraper_utils import (
    detect_access_restriction,
    detect_profile_not_found,
    load_sample_profiles,
    parse_profile_html,
)
from utils.validators import validate_hackerrank_username


class TestAnalyticsAndScraperUtils(unittest.TestCase):
    def test_sample_profiles_and_single_profile_analysis(self) -> None:
        samples = load_sample_profiles()
        self.assertGreaterEqual(len(samples), 3)

        report = analyze_single_profile(samples[0])
        self.assertTrue(report["is_sample"])
        self.assertGreater(report["summary_counts"]["languages_count"], 0)
        self.assertGreater(len(report["insights"]), 0)

        # Verify minimal profile does not fabricate missing fields
        minimal_res = HackerRankScraper.load_sample_profile("elena_minimal_public")
        self.assertTrue(minimal_res.success)
        minimal_report = analyze_single_profile(minimal_res.profile_data)
        self.assertEqual(minimal_report["summary_counts"]["certificates_count"], 0)

    def test_coding_analytics_dataframes_and_charts(self) -> None:
        samples = load_sample_profiles()
        lang_df = build_language_distribution(samples)
        skill_df = build_skill_distribution(samples)
        ach_df = build_badge_and_achievement_summary(samples)
        comp_df = build_profile_comparison_df(samples)

        self.assertFalse(lang_df.empty)
        self.assertFalse(skill_df.empty)
        self.assertFalse(ach_df.empty)
        self.assertEqual(len(comp_df), len(samples))

        fig_bar = create_language_bar_chart(lang_df)
        fig_pie = create_language_pie_chart(lang_df)
        fig_comp = create_comparison_chart(comp_df)
        mpl_fig = create_matplotlib_language_summary(lang_df)

        self.assertGreater(len(fig_bar.data), 0)
        self.assertGreater(len(fig_pie.data), 0)
        self.assertGreater(len(fig_comp.data), 0)
        self.assertIsNotNone(mpl_fig)

    def test_username_validation_and_html_parsing(self) -> None:
        ok, name = validate_hackerrank_username("https://www.hackerrank.com/profile/valid_user_1")
        self.assertTrue(ok)
        self.assertEqual(name, "valid_user_1")

        bad, _ = validate_hackerrank_username("invalid user with spaces!")
        self.assertFalse(bad)

        restricted, msg = detect_access_restriction("<html>Please verify you are human</html>")
        self.assertTrue(restricted)
        self.assertIn("CAPTCHA", msg)

        not_found, nf_msg = detect_profile_not_found("<h1>404 - Page Not Found</h1>")
        self.assertTrue(not_found)
        self.assertIn("404", nf_msg)

        mock_html = """
        <html>
          <body>
            <h1 class="profile-heading">Jane Doe</h1>
            <div class="profile-about-section"><p>Python developer</p></div>
            <div class="hacker-badge"><h3 class="badge-title">Python</h3><span class="star-filled"></span></div>
            <div class="skill-chip">Python (Basic) Verified</div>
          </body>
        </html>
        """
        parsed = parse_profile_html(mock_html, username="jane_doe")
        self.assertEqual(parsed["display_name"], "Jane Doe")
        self.assertEqual(parsed["description"], "Python developer")
        self.assertEqual(len(parsed["badges"]), 1)
        self.assertEqual(len(parsed["skills"]), 1)
        self.assertIsNone(parsed["country"])


if __name__ == "__main__":
    unittest.main()


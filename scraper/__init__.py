"""Selenium web scraper, response classifier, and JSON/CSV profile importer package."""

from scraper.browser_manager import BrowserManager, BrowserStartupError
from scraper.hackerrank_scraper import HackerRankScraper, ScrapeResult
from scraper.scraper_utils import (
    HACKERRANK_SELECTORS,
    build_sample_csv_template,
    build_sample_json_template,
    classify_page_response,
    detect_access_restriction,
    detect_network_error_page,
    detect_profile_not_found,
    load_sample_profiles,
    parse_profile_html,
    parse_uploaded_profile_csv,
    parse_uploaded_profile_json,
)

__all__ = [
    "BrowserManager",
    "BrowserStartupError",
    "HackerRankScraper",
    "ScrapeResult",
    "HACKERRANK_SELECTORS",
    "parse_profile_html",
    "detect_access_restriction",
    "detect_network_error_page",
    "detect_profile_not_found",
    "classify_page_response",
    "load_sample_profiles",
    "parse_uploaded_profile_json",
    "parse_uploaded_profile_csv",
    "build_sample_json_template",
    "build_sample_csv_template",
]

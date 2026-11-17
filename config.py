"""
Central configuration settings for the Hacker Analytics and AI Code Detection System.
"""

from pathlib import Path

# Project directories
BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
SAMPLE_DATA_DIR: Path = BASE_DIR / "sample_data"
DB_PATH: Path = DATA_DIR / "hackerrank.db"

# Application metadata
APP_TITLE: str = "Hacker Analytics & AI Code Detection System"
APP_SHORT_TITLE: str = "Hacker Analytics"
APP_VERSION: str = "1.0.0"
APP_DESCRIPTION: str = (
    "A modular Python web application for public HackerRank profile scraping, "
    "coding performance analytics, source-code similarity analysis, AST structural "
    "inspection, and explainable heuristic AI-pattern analysis."
)

# HackerRank scraping configuration
HACKERRANK_PROFILE_BASE_URL: str = "https://www.hackerrank.com/profile/"
SCRAPER_PAGE_LOAD_TIMEOUT: int = 25
SCRAPER_ELEMENT_WAIT_TIMEOUT: int = 12
SCRAPER_RENDER_DELAY_SECONDS: float = 2.0

# Code analysis limits
MAX_CODE_FILE_BYTES: int = 512 * 1024  # 512 KB per uploaded file

# Heuristic AI-associated pattern labels (non-probabilistic)
HEURISTIC_LABELS = {
    "few": "Few indicators observed",
    "some": "Some indicators observed",
    "several": "Several indicators observed",
}

HEURISTIC_THRESHOLDS = {
    "some_min": 35.0,
    "several_min": 65.0,
}

# Important ethical and analytical disclaimers
AI_DETECTION_DISCLAIMER: str = (
    "Heuristic analysis identifies stylistic and structural patterns sometimes associated "
    "with AI-assisted coding. It does NOT prove AI authorship, does NOT output a validated "
    "probability, and cannot distinguish well-formatted human code from AI-assisted code "
    "with certainty. False positives and false negatives are always possible."
)

SIMILARITY_DISCLAIMER: str = (
    "A high similarity score is NOT proof of plagiarism. Common algorithms, standard "
    "library idioms, shared starter templates, and identical problem constraints frequently "
    "produce structural and textual similarity between independent submissions."
)

SCRAPING_DISCLAIMER: str = (
    "This tool only accesses publicly visible HackerRank profile pages without bypassing "
    "CAPTCHAs, logins, or access controls. Live availability depends on HackerRank's "
    "public page structure and network access. Use Sample Data Mode for offline demos."
)


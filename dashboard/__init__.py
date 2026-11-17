"""Streamlit dashboard pages and navigation components."""

from dashboard.ai_detection_page import render_ai_detection_page
from dashboard.coding_page import render_coding_page
from dashboard.history_page import render_history_page
from dashboard.home import render_home_page
from dashboard.profile_page import render_profile_page
from dashboard.scraper_page import render_scraper_page
from dashboard.sidebar import PAGES, render_sidebar
from dashboard.similarity_page import render_similarity_page

__all__ = [
    "PAGES",
    "render_sidebar",
    "render_home_page",
    "render_scraper_page",
    "render_profile_page",
    "render_coding_page",
    "render_similarity_page",
    "render_ai_detection_page",
    "render_history_page",
]


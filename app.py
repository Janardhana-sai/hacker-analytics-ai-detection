"""
Main Streamlit entry point for the Hacker Analytics and AI Code Detection System.
Initializes the SQLite database and routes between the 7 dashboard pages.
"""

from __future__ import annotations

import streamlit as st

from config import APP_TITLE, DB_PATH
from dashboard.ai_detection_page import render_ai_detection_page
from dashboard.coding_page import render_coding_page
from dashboard.history_page import render_history_page
from dashboard.home import render_home_page
from dashboard.profile_page import render_profile_page
from dashboard.quality_page import render_quality_page
from dashboard.scraper_page import render_scraper_page
from dashboard.sidebar import render_sidebar
from dashboard.similarity_page import render_similarity_page
from database.db_manager import DatabaseManager


def get_database() -> DatabaseManager:
    """Create or reuse a DatabaseManager instance stored in session state."""
    if "db_manager" not in st.session_state:
        st.session_state["db_manager"] = DatabaseManager(DB_PATH)
    return st.session_state["db_manager"]


def apply_custom_styling() -> None:
    """Apply clean, modern dashboard styling with sleek visuals."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }
        [data-testid="stMetric"] {
            background-color: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            padding: 14px 18px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
        }
        [data-testid="stButton"] button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_custom_styling()

    db = get_database()
    active_page = render_sidebar(db)

    page_routes = {
        "Home Dashboard": render_home_page,
        "Selenium Web Scraper": render_scraper_page,
        "Profile Analytics": render_profile_page,
        "Coding Performance Analytics": render_coding_page,
        "Source-Code Similarity": render_similarity_page,
        "AI-Associated Code Pattern Analysis": render_ai_detection_page,
        "Code Quality & Security Audit": render_quality_page,
        "Analysis History": render_history_page,
    }

    renderer = page_routes.get(active_page, render_home_page)
    renderer(db)


if __name__ == "__main__":
    main()


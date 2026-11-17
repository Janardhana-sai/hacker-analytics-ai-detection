"""
Sidebar navigation and live database status summary for the Streamlit dashboard.
"""

from __future__ import annotations

import streamlit as st

from config import APP_SHORT_TITLE, APP_VERSION
from database.db_manager import DatabaseManager

PAGES: list[str] = [
    "Home Dashboard",
    "Selenium Web Scraper",
    "Profile Analytics",
    "Coding Performance Analytics",
    "Source-Code Similarity",
    "AI-Associated Code Pattern Analysis",
    "Analysis History",
]

PAGE_LABELS: dict[str, str] = {
    "Home Dashboard": "🏠 Home Dashboard",
    "Selenium Web Scraper": "🕸️ Selenium Web Scraper",
    "Profile Analytics": "📊 Profile Analytics",
    "Coding Performance Analytics": "📈 Coding Analytics",
    "Source-Code Similarity": "📐 Code Similarity",
    "AI-Associated Code Pattern Analysis": "🤖 AI Pattern Check",
    "Analysis History": "📋 Analysis History",
}


def render_sidebar(db: DatabaseManager) -> str:
    """Render sidebar navigation and summary indicators, returning the selected page."""
    if "current_page" not in st.session_state or st.session_state["current_page"] not in PAGES:
        st.session_state["current_page"] = PAGES[0]

    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 8px 0 16px 0; border-bottom: 1px solid rgba(148, 163, 184, 0.2); margin-bottom: 16px;">
                <div style="font-size: 1.25rem; font-weight: 800; background: linear-gradient(90deg, #60A5FA, #38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    🛡️ {APP_SHORT_TITLE}
                </div>
                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 2px;">
                    v{APP_VERSION} • Intelligence & Analytics
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        current_idx = PAGES.index(st.session_state["current_page"])
        selected = st.radio(
            "Navigation",
            options=PAGES,
            index=current_idx,
            format_func=lambda p: PAGE_LABELS.get(p, p),
            label_visibility="collapsed",
        )
        if selected != st.session_state["current_page"]:
            st.session_state["current_page"] = selected
            st.rerun()

        st.divider()
        counts = db.get_dashboard_counts()
        st.markdown("#### ⚡ Workspace Vault")
        col1, col2 = st.columns(2)
        col1.metric("Profiles", counts["total_profiles"])
        col2.metric("Scrapes", counts["total_scrapes"])
        col3, col4 = st.columns(2)
        col3.metric("Similarities", counts["total_similarities"])
        col4.metric("AI Checks", counts["total_ai_analyses"])

        st.caption(
            f"Live: {counts['live_profiles']} | Sample: {counts['sample_profiles']}"
        )
        st.info(
            "💡 Tip: Click **Home Dashboard** above to see the new graphics & visual analytics overview.",
            icon="ℹ️",
        )

    return st.session_state["current_page"]

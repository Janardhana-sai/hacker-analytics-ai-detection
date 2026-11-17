"""
Page 4: Coding Performance Analytics.
Interactive Plotly visualizations (and optional Matplotlib view) for language
distribution, skills, badges, profile comparison, and historical activity trends.
"""

from __future__ import annotations

import streamlit as st

from analytics.coding_analytics import (
    build_activity_trend_df,
    build_badge_and_achievement_summary,
    build_language_distribution,
    build_profile_comparison_df,
    build_skill_distribution,
    create_activity_trend_chart,
    create_badge_chart,
    create_comparison_chart,
    create_language_bar_chart,
    create_language_pie_chart,
    create_matplotlib_language_summary,
    create_skill_chart,
)
from database.db_manager import DatabaseManager


def render_coding_page(db: DatabaseManager) -> None:
    """Render the Coding Performance Analytics dashboard page."""
    st.title("Coding Performance Analytics")

    all_profiles = db.get_all_profiles(include_sample=True)
    if not all_profiles:
        st.info(
            "No profiles available for analytics. Scrape a public profile or load sample data "
            "from **Selenium Web Scraper** first."
        )
        return

    source_choice = st.radio(
        "Dataset Scope",
        options=["All Stored Profiles", "Live Scraped Only", "Demonstration Sample Data Only"],
        horizontal=True,
    )
    if source_choice == "Live Scraped Only":
        filtered_profiles = [p for p in all_profiles if not p.get("is_sample")]
    elif source_choice == "Demonstration Sample Data Only":
        filtered_profiles = [p for p in all_profiles if p.get("is_sample")]
    else:
        filtered_profiles = all_profiles

    if not filtered_profiles:
        st.warning(f"No profiles found under '{source_choice}'.")
        return

    has_sample = any(p.get("is_sample") for p in filtered_profiles)
    has_live = any(not p.get("is_sample") for p in filtered_profiles)
    if has_sample and has_live:
        st.info(
            "Note: Selection currently includes both **Live** and **Demonstration Sample** profiles. "
            "Use the Dataset Scope filter above to isolate live vs sample records.",
            icon="ℹ️",
        )
    elif has_sample:
        st.warning("Charts below display **Demonstration Sample Data**.", icon="🧪")

    profile_names = [p["username"] for p in filtered_profiles]
    selected_names = st.multiselect(
        "Select Profiles to Include",
        options=profile_names,
        default=profile_names,
    )
    selected_profiles = [p for p in filtered_profiles if p["username"] in selected_names]
    if not selected_profiles:
        st.warning("Select at least one profile to generate charts.")
        return

    lang_df = build_language_distribution(selected_profiles)
    skill_df = build_skill_distribution(selected_profiles)
    ach_df = build_badge_and_achievement_summary(selected_profiles)
    comp_df = build_profile_comparison_df(selected_profiles)

    # Row 1: Language distribution (Bar + Pie)
    st.subheader("1. Programming Language Distribution")
    if lang_df.empty:
        st.info(
            "No publicly visible programming language breakdown was collected for the selected profile(s). "
            "Select additional profiles or Demonstration Sample Data above to view language distribution charts."
        )
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                create_language_bar_chart(lang_df),
                width="stretch",
                key="coding_lang_bar_chart",
            )
        with c2:
            st.plotly_chart(
                create_language_pie_chart(lang_df),
                width="stretch",
                key="coding_lang_pie_chart",
            )

        with st.expander("View Matplotlib Static Language Summary"):
            mpl_fig = create_matplotlib_language_summary(lang_df)
            st.pyplot(mpl_fig, clear_figure=True)

    # Row 2: Skills & Badges
    st.subheader("2. Skill & Badge Analysis")
    c3, c4 = st.columns(2)
    with c3:
        if skill_df.empty:
            st.info("No publicly listed skill records available for the selected profile(s).")
        else:
            st.plotly_chart(
                create_skill_chart(skill_df),
                width="stretch",
                key="coding_skill_chart",
            )
    with c4:
        if ach_df.empty:
            st.info("No publicly listed badge or certificate records available for the selected profile(s).")
        else:
            st.plotly_chart(
                create_badge_chart(ach_df),
                width="stretch",
                key="coding_badge_chart",
            )

    # Row 3: Multi-profile comparison
    st.subheader("3. Profile Comparison")
    if len(selected_profiles) >= 2:
        st.plotly_chart(
            create_comparison_chart(comp_df),
            width="stretch",
            key="coding_comparison_chart",
        )
        st.dataframe(comp_df, width="stretch", hide_index=True)
    else:
        st.info("Select 2 or more profiles above to view multi-profile comparison charts.")
        st.dataframe(comp_df, width="stretch", hide_index=True)

    # Row 4: Historical activity trends
    st.subheader("4. Historical Activity & Metric Trends")
    time_range = st.radio(
        "Time Window",
        options=["3M", "6M", "1Y", "3Y", "All"],
        index=0,
        horizontal=True,
        key="coding_trend_time_range",
    )
    scraping_hist = db.get_scraping_history(limit=200)
    stats_hist = [
        s
        for s in db.get_all_statistics_history()
        if s.get("username") in selected_names
    ]
    trend_df = build_activity_trend_df(scraping_hist, stats_hist)
    if not trend_df.empty:
        st.plotly_chart(
            create_activity_trend_chart(trend_df, time_range=time_range),
            width="stretch",
            key="coding_activity_trend_chart",
        )
    else:
        st.info(
            "No historical trend records exist yet. Re-scraping profiles over time builds historical snapshots."
        )


"""
Page 3: HackerRank Profile Analytics.
Displays structured profile overview, languages, skills, badges, certificates,
available statistics, and factual Pandas-derived insights.
"""

from __future__ import annotations

import streamlit as st

from analytics.profile_analysis import analyze_single_profile
from database.db_manager import DatabaseManager
from utils.helpers import format_timestamp


def render_profile_page(db: DatabaseManager) -> None:
    """Render the Profile Analytics page."""
    st.title("HackerRank Profile Analytics")

    profiles = db.get_all_profiles(include_sample=True)
    if not profiles:
        st.info(
            "No profiles found in the database yet. Visit **Selenium Web Scraper** to scrape "
            "a public profile or load demonstration sample data."
        )
        return

    filter_mode = st.radio(
        "Data Source Filter",
        options=["All Profiles", "Live Profiles Only", "Sample Data Only"],
        horizontal=True,
    )
    if filter_mode == "Live Profiles Only":
        profiles = [p for p in profiles if not p.get("is_sample")]
    elif filter_mode == "Sample Data Only":
        profiles = [p for p in profiles if p.get("is_sample")]

    if not profiles:
        st.warning(f"No profiles match the filter '{filter_mode}'.")
        return

    username_map = {p["username"]: p for p in profiles}
    usernames = list(username_map.keys())
    preselected = st.session_state.get("selected_profile_username")
    default_idx = usernames.index(preselected) if preselected in usernames else 0

    selected_username = st.selectbox(
        "Select Profile to Analyse",
        options=usernames,
        index=default_idx,
        format_func=lambda u: (
            f"{u} {'[SAMPLE DATA]' if username_map[u].get('is_sample') else ('[UPLOADED]' if username_map[u].get('source_label') == 'uploaded' else '[LIVE]')}"
        ),
    )
    st.session_state["selected_profile_username"] = selected_username

    profile = username_map[selected_username]
    report = analyze_single_profile(profile)
    counts = report["summary_counts"]

    if profile.get("is_sample"):
        st.warning(
            "**Demonstration Sample Data**: Insights below reflect sample profile data, not live HackerRank records.",
            icon="🧪",
        )
    elif profile.get("source_label") == "uploaded":
        st.info(
            "**Uploaded Public Profile**: Insights below reflect user-uploaded JSON/CSV profile data.",
            icon="📤",
        )
    else:
        st.success("**Live Scraped Profile**: Insights below reflect publicly collected profile data.", icon="🌐")

    st.subheader(profile.get("display_name") or profile["username"])
    meta_parts = [f"**Username:** `{profile['username']}`"]
    if profile.get("country"):
        meta_parts.append(f"**Country:** {profile['country']}")
    if profile.get("profile_url"):
        meta_parts.append(f"**URL:** [{profile['profile_url']}]({profile['profile_url']})")
    meta_parts.append(f"**Last Scraped:** {format_timestamp(profile.get('last_scraped_at'))}")
    st.markdown(" • ".join(meta_parts))

    if profile.get("description"):
        st.markdown(f"> {profile['description']}")
    else:
        st.caption("Profile description: Not publicly available.")

    st.divider()
    total_stars = 0
    for b in profile.get("badges") or []:
        stars_txt = str(b.get("level_or_stars") or "")
        digits = "".join(ch for ch in stars_txt if ch.isdigit())
        if digits:
            total_stars += int(digits)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Languages", counts["languages_count"])
    m2.metric("Skills", counts["skills_count"], delta=f"{counts['verified_skills_count']} Verified")
    m3.metric(
        "Badges",
        counts["badges_count"],
        delta=f"{total_stars} ★ Total" if total_stars > 0 else None,
    )
    m4.metric("Certificates", counts["certificates_count"])
    m5.metric(
        "Problems Solved",
        counts["total_listed_problems"] if counts["total_listed_problems"] is not None else "Not Exposed",
        help=(
            "HackerRank does not publicly expose total problems-solved counts on live profile pages. "
            "Values are shown only when explicitly present (never fabricated)."
        ),
    )

    st.divider()
    st.subheader("Data-Backed Profile Insights")
    for insight in report["insights"]:
        st.markdown(f"- {insight}")

    if report["unavailable_fields"]:
        st.caption(
            f"Unexposed / NULL fields for this profile: {', '.join(report['unavailable_fields'])}"
        )

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Programming Languages")
        if not report["languages_df"].empty:
            st.dataframe(report["languages_df"], use_container_width=True, hide_index=True)
        else:
            st.info("No public programming language records available.")

    with c2:
        st.markdown("#### Skills")
        if not report["skills_df"].empty:
            st.dataframe(report["skills_df"], use_container_width=True, hide_index=True)
        else:
            st.info("No public skill records available.")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### Badges")
        if not report["badges_df"].empty:
            st.dataframe(report["badges_df"], use_container_width=True, hide_index=True)
        else:
            st.info("No public badges available.")

    with c4:
        st.markdown("#### Certificates")
        if not report["certificates_df"].empty:
            st.dataframe(report["certificates_df"], use_container_width=True, hide_index=True)
        else:
            st.info("No public certificates available.")

    c5, c6 = st.columns(2)
    with c5:
        st.markdown("#### Available Problem-Solving Statistics")
        if not report["statistics_df"].empty:
            display_stats = report["statistics_df"][
                [col for col in ["stat_name", "stat_value", "stat_category", "recorded_at"] if col in report["statistics_df"].columns]
            ]
            st.dataframe(display_stats, use_container_width=True, hide_index=True)
        else:
            st.info("No public numeric statistics available.")

    with c6:
        st.markdown("#### Publicly Visible Activity")
        if not report["activity_df"].empty:
            st.dataframe(report["activity_df"], use_container_width=True, hide_index=True)
        else:
            st.info("No public activity records available.")


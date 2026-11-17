"""
Page 2: Selenium Web Scraper, Offline Sample Data Mode, and JSON/CSV Profile Upload.
Displays live scraping status, error classifications, diagnostic logs, last successful
collection timestamp, and offline sample/upload workflows.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import SCRAPING_DISCLAIMER
from database.db_manager import DatabaseManager
from scraper.hackerrank_scraper import HackerRankScraper, ScrapeResult
from scraper.scraper_utils import (
    build_sample_csv_template,
    build_sample_json_template,
    parse_uploaded_profile_csv,
    parse_uploaded_profile_json,
)
from utils.helpers import format_timestamp, utc_now_iso
from utils.validators import validate_and_parse_profile_input


def _load_all_sample_profiles(db: DatabaseManager) -> int:
    """Load all offline demonstration profiles into SQLite and update session state."""
    loaded = 0
    for uname in HackerRankScraper.get_available_sample_usernames():
        res = HackerRankScraper.load_sample_profile(uname)
        if res.success and res.profile_data:
            pid = db.upsert_profile(res.profile_data)
            db.log_scraping_attempt(
                username=res.username,
                status="success",
                source_mode="sample",
                profile_id=pid,
                fields_collected=res.fields_collected,
                duration_seconds=res.duration_seconds,
                scraped_at=res.scraped_at,
            )
            st.session_state["last_scrape_result"] = res
            st.session_state["selected_profile_username"] = res.username
            loaded += 1
    return loaded


def _display_collected_profile_preview(profile: dict, result: ScrapeResult) -> None:
    """Render collected profile details and quick action to open Profile Analytics."""
    source_label = profile.get("source_label") or ("sample" if profile.get("is_sample") else "live")
    if source_label == "sample" or profile.get("is_sample"):
        st.warning(
            "**OFFLINE SAMPLE DATA MODE** — This demonstration record was loaded locally from "
            "`sample_data/sample_profiles.json` and is clearly tagged as sample data.",
            icon="🧪",
        )
    elif source_label == "uploaded":
        st.success(
            "Public profile data imported from uploaded JSON/CSV file and saved to SQLite.",
            icon="📤",
        )
    else:
        st.success("Live public HackerRank profile data extracted and saved to SQLite.", icon="✅")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Username", profile.get("username") or "N/A")
    m2.metric("Fields Collected", result.fields_collected)
    m3.metric("Duration (s)", f"{result.duration_seconds:.2f}")
    m4.metric("Collected At", format_timestamp(profile.get("last_scraped_at")))

    if profile.get("display_name"):
        st.markdown(f"**Display Name:** {profile['display_name']}")
    if profile.get("profile_url"):
        st.markdown(f"**Profile URL:** [{profile['profile_url']}]({profile['profile_url']})")
    if profile.get("country"):
        st.markdown(f"**Country:** {profile['country']}")
    if profile.get("description"):
        st.markdown(f"**Profile Description:** {profile['description']}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Programming Languages")
        langs = profile.get("programming_languages") or []
        if langs:
            st.dataframe(pd.DataFrame(langs), use_container_width=True, hide_index=True)
        else:
            st.caption("No public programming languages exposed.")

    with c2:
        st.markdown("##### Skills")
        skills = profile.get("skills") or []
        if skills:
            st.dataframe(pd.DataFrame(skills), use_container_width=True, hide_index=True)
        else:
            st.caption("No public skills exposed.")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("##### Badges & Certificates")
        ach = (profile.get("badges") or []) + (profile.get("certificates") or [])
        if ach:
            st.dataframe(pd.DataFrame(ach), use_container_width=True, hide_index=True)
        else:
            st.caption("No public badges or certificates exposed.")

    with c4:
        st.markdown("##### Public Statistics")
        stats = profile.get("statistics") or []
        if stats:
            st.dataframe(pd.DataFrame(stats), use_container_width=True, hide_index=True)
        else:
            st.caption("No public numeric statistics exposed.")

    unavailable = profile.get("unavailable_fields") or []
    if unavailable:
        st.info(f"Unavailable / unexposed fields (stored as NULL/empty): {', '.join(unavailable)}")

    if st.button("Analyse This Profile →", type="primary"):
        st.session_state["selected_profile_username"] = profile.get("username")
        st.session_state["current_page"] = "Profile Analytics"
        st.rerun()


def render_scraper_page(db: DatabaseManager) -> None:
    """Render the Selenium HackerRank Web Scraper page."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 138, 0.45) 50%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-radius: 16px;
            padding: 22px 28px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.4);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); padding: 3px 12px; border-radius: 9999px; margin-bottom: 8px;">
                        <span style="font-size: 0.75rem; font-weight: 700; color: #93C5FD; letter-spacing: 0.04em;">MODULE 1 • BROWSER ENGINE</span>
                    </div>
                    <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF, #93C5FD); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        🕸️ Selenium HackerRank Web Scraper
                    </h1>
                    <p style="color: #94A3B8; font-size: 0.92rem; margin: 4px 0 0 0;">
                        Automated Selenium browser ingestion, offline demonstration repository, and custom JSON/CSV profile upload.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(SCRAPING_DISCLAIMER, icon="🛡️")

    # Persistent collection status summary bar
    last_success_any = db.get_last_successful_scrape_time()
    last_success_live = db.get_last_successful_scrape_time(source_mode="live")
    recent_scrapes = db.get_scraping_history(limit=1)
    last_status = recent_scrapes[0]["status"] if recent_scrapes else "idle"
    counts = db.get_dashboard_counts()

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Latest Collection Status", str(last_status).replace("_", " ").title())
    s2.metric(
        "Last Successful Collection",
        format_timestamp(last_success_any) if last_success_any else "None Yet",
    )
    s3.metric(
        "Last Live Scrape Success",
        format_timestamp(last_success_live) if last_success_live else "None Yet",
    )
    s4.metric("Stored Profiles", counts["total_profiles"])

    # Always-visible Offline Sample Data Mode quick banner
    with st.container(border=True):
        b_col1, b_col2 = st.columns([3, 1])
        with b_col1:
            st.markdown(
                "**🧪 Offline Sample Data Mode Available** — Works without internet access or live "
                "HackerRank availability. Load demonstration profiles immediately or upload your own "
                "publicly obtained JSON/CSV profile file."
            )
        with b_col2:
            if st.button("Quick-Load Sample Data", use_container_width=True):
                loaded_n = _load_all_sample_profiles(db)
                st.success(f"Loaded {loaded_n} offline sample profile(s) into SQLite.")
                st.rerun()

    live_tab, sample_tab, upload_tab = st.tabs(
        [
            "🌐 Live Selenium Profile Scraper",
            "🧪 Sample Data Mode (Offline)",
            "📤 Upload Profile Data (JSON / CSV)",
        ]
    )

    with live_tab:
        st.markdown(
            "Enter a HackerRank username (e.g. `sample_user`) or full profile URL "
            "(e.g. `https://www.hackerrank.com/profile/sample_user`)."
        )
        with st.form("live_scrape_form"):
            username_input = st.text_input(
                "HackerRank Username or Profile URL",
                placeholder="e.g., https://www.hackerrank.com/profile/sample_username",
                help="Validates host, path, and username before opening Selenium in standard visible Chrome/Edge mode.",
            )
            submitted = st.form_submit_button("Start Live Scraping", type="primary")

        if username_input.strip():
            ok_preview, parsed_preview = validate_and_parse_profile_input(username_input)
            if ok_preview:
                st.caption(
                    f"Parsed Username: `{parsed_preview['username']}` • "
                    f"Canonical Profile URL: `{parsed_preview['profile_url']}`"
                )
            else:
                st.caption(f"Input check: {parsed_preview['error']}")

        if submitted:
            progress_bar = st.progress(0, text="Initializing scraper...")
            status_box = st.empty()

            def _on_progress(pct: int, msg: str) -> None:
                progress_bar.progress(min(max(pct, 0), 100), text=msg)
                status_box.caption(f"Status: **{msg}**")

            scraper = HackerRankScraper(headless=False)
            result = scraper.scrape_profile(username_input, progress_callback=_on_progress)
            st.session_state["last_scrape_attempt"] = result

            profile_id: int | None = None
            if result.success and result.profile_data:
                profile_id = db.upsert_profile(result.profile_data)
                st.session_state["last_scrape_result"] = result
                st.session_state["selected_profile_username"] = result.username

            db.log_scraping_attempt(
                username=result.username or username_input.strip(),
                status=result.status,
                source_mode="live",
                profile_id=profile_id,
                fields_collected=result.fields_collected,
                error_message=result.error_message,
                duration_seconds=result.duration_seconds,
                scraped_at=result.scraped_at,
            )

            if not result.success:
                progress_bar.progress(100, text=f"Finished with status: {result.status}")
                status_descriptions = {
                    "validation_error": "Invalid Username or Profile URL",
                    "not_found": "Profile Not Found (404)",
                    "network_error": "Network / Page-Load Error",
                    "missing_elements": "Page Loaded — Public Elements Missing",
                    "restricted": "Access Denied / Anti-Bot Protection",
                    "browser_error": "Selenium Browser Driver Error",
                }
                title_label = status_descriptions.get(result.status, result.status)
                st.error(
                    f"**{title_label} (`{result.status}`)**: {result.error_message}\n\n"
                    "You can use **Quick-Load Sample Data** above or upload a **JSON/CSV** "
                    "profile file to continue analyzing profiles offline."
                )

        last_attempt: ScrapeResult | None = st.session_state.get("last_scrape_attempt")
        if last_attempt and last_attempt.debug_info:
            with st.expander("Scraper Diagnostic Details & Debug Logs"):
                st.json(last_attempt.debug_info)
                recent_logs = HackerRankScraper.read_recent_logs(20)
                if recent_logs:
                    st.markdown("##### Recent `data/scraper.log` Entries")
                    st.code("\n".join(recent_logs), language="text")

    with sample_tab:
        st.warning(
            "Sample Data Mode loads realistic demonstration profiles stored locally in "
            "`sample_data/sample_profiles.json` with zero internet required. All sample records "
            "are flagged as `sample` so they never mix silently with live or uploaded records.",
            icon="🧪",
        )
        sample_usernames = HackerRankScraper.get_available_sample_usernames()
        if not sample_usernames:
            st.error("No sample profiles found in `sample_data/sample_profiles.json`.")
        else:
            col_s1, col_s2 = st.columns([3, 1])
            with col_s1:
                chosen_sample = st.selectbox(
                    "Select a Demonstration Profile",
                    options=sample_usernames,
                    format_func=lambda u: f"{u} (Offline Sample)",
                )
            with col_s2:
                st.write("")
                st.write("")
                load_one = st.button("Load Sample Profile", type="primary", use_container_width=True)

            load_all = st.button("Load All Demonstration Profiles into Database")

            if load_one and chosen_sample:
                res = HackerRankScraper.load_sample_profile(chosen_sample)
                if res.success and res.profile_data:
                    pid = db.upsert_profile(res.profile_data)
                    db.log_scraping_attempt(
                        username=res.username,
                        status="success",
                        source_mode="sample",
                        profile_id=pid,
                        fields_collected=res.fields_collected,
                        duration_seconds=res.duration_seconds,
                        scraped_at=res.scraped_at,
                    )
                    st.session_state["last_scrape_result"] = res
                    st.session_state["selected_profile_username"] = res.username

            if load_all:
                loaded_count = _load_all_sample_profiles(db)
                st.success(f"Loaded {loaded_count} offline demonstration profile(s) into SQLite.")

    with upload_tab:
        st.markdown(
            "Upload publicly obtained HackerRank profile data in **JSON** or **CSV** format to "
            "store it in SQLite and analyze it across all dashboard charts."
        )
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.download_button(
                "Download Sample JSON Template",
                data=build_sample_json_template(),
                file_name="hackerrank_profile_template.json",
                mime="application/json",
                use_container_width=True,
            )
        with t_col2:
            st.download_button(
                "Download Sample CSV Template",
                data=build_sample_csv_template(),
                file_name="hackerrank_profile_template.csv",
                mime="text/csv",
                use_container_width=True,
            )

        uploaded_profile_file = st.file_uploader(
            "Upload Public Profile Data (.json or .csv)",
            type=["json", "csv"],
            key="profile_json_csv_uploader",
        )
        if uploaded_profile_file is not None and st.button(
            "Import Uploaded Profile Data", type="primary"
        ):
            raw_content = uploaded_profile_file.getvalue().decode("utf-8", errors="replace")
            fname_lower = uploaded_profile_file.name.lower()
            try:
                if fname_lower.endswith(".json"):
                    imported_profiles = parse_uploaded_profile_json(raw_content)
                else:
                    imported_profiles = parse_uploaded_profile_csv(raw_content)

                imported_count = 0
                for prof in imported_profiles:
                    pid = db.upsert_profile(prof)
                    now_ts = utc_now_iso()
                    db.log_scraping_attempt(
                        username=prof["username"],
                        status="success",
                        source_mode="uploaded",
                        profile_id=pid,
                        fields_collected=int(prof.get("fields_collected", 0)),
                        duration_seconds=0.0,
                        scraped_at=now_ts,
                    )
                    last_res_obj = ScrapeResult(
                        success=True,
                        username=prof["username"],
                        status="success",
                        source_mode="uploaded",
                        profile_data=prof,
                        fields_collected=int(prof.get("fields_collected", 0)),
                        unavailable_fields=prof.get("unavailable_fields", []),
                        duration_seconds=0.0,
                        scraped_at=now_ts,
                    )
                    st.session_state["last_scrape_result"] = last_res_obj
                    st.session_state["selected_profile_username"] = prof["username"]
                    imported_count += 1

                st.success(
                    f"Successfully imported {imported_count} profile(s) from `{uploaded_profile_file.name}`."
                )
            except ValueError as val_exc:
                st.error(f"Upload validation error: {val_exc}")

    # Show latest successful result preview if present
    last_res: ScrapeResult | None = st.session_state.get("last_scrape_result")
    if last_res and last_res.success and last_res.profile_data:
        st.divider()
        st.subheader("Latest Collected / Loaded Profile")
        _display_collected_profile_preview(last_res.profile_data, last_res)

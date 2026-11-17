"""
Page 7: Analysis History.
Search, filter, inspect, export, and manage historical scraping, profile,
similarity, and heuristic pattern records stored in SQLite.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from database.db_manager import DatabaseManager
from utils.helpers import format_timestamp


def render_history_page(db: DatabaseManager) -> None:
    """Render the Analysis History browser page."""
    st.title("Analysis History & Stored Records")

    tab_scrape, tab_profiles, tab_sim, tab_ai = st.tabs(
        [
            "Scraping History",
            "Stored Profiles",
            "Code Similarity History",
            "AI Pattern Analysis History",
        ]
    )

    with tab_scrape:
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search_q = st.text_input("Search username or error", key="hist_scrape_search")
        with c2:
            status_f = st.selectbox(
                "Status",
                options=[
                    "All",
                    "success",
                    "not_found",
                    "restricted",
                    "missing_elements",
                    "network_error",
                    "browser_error",
                    "validation_error",
                    "empty",
                    "error",
                ],
                key="hist_scrape_status",
            )
        with c3:
            source_f = st.selectbox(
                "Source", options=["All", "live", "sample", "uploaded"], key="hist_scrape_source"
            )

        rows = db.get_scraping_history(
            limit=200,
            status_filter=status_f,
            source_filter=source_f,
            search=search_q,
        )
        if rows:
            df = pd.DataFrame(rows)
            df["scraped_at"] = df["scraped_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Scraping History CSV",
                data=csv_bytes,
                file_name="scraping_history.csv",
                mime="text/csv",
            )
        else:
            st.info("No scraping history records match your filters.")

    with tab_profiles:
        c1, c2 = st.columns([3, 1])
        with c1:
            prof_search = st.text_input("Search stored profiles", key="hist_prof_search")
        with c2:
            include_sample = st.checkbox("Include Sample Profiles", value=True, key="hist_prof_sample")

        profiles = db.get_all_profiles(include_sample=include_sample, search=prof_search)
        if profiles:
            summary_rows = [
                {
                    "id": p["id"],
                    "username": p["username"],
                    "display_name": p.get("display_name") or "N/A",
                    "source": "Sample" if p.get("is_sample") else "Live",
                    "fields_collected": p.get("fields_collected", 0),
                    "languages": len(p.get("programming_languages") or []),
                    "skills": len(p.get("skills") or []),
                    "badges": len(p.get("badges") or []),
                    "last_scraped_at": format_timestamp(p.get("last_scraped_at")),
                }
                for p in profiles
            ]
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

            col_act1, col_act2 = st.columns([3, 1])
            with col_act1:
                target_user = st.selectbox(
                    "Select a Profile for Action",
                    options=[p["username"] for p in profiles],
                    key="hist_prof_select",
                )
            with col_act2:
                st.write("")
                st.write("")
                if st.button("Open in Analytics", use_container_width=True):
                    st.session_state["selected_profile_username"] = target_user
                    st.session_state["current_page"] = "Profile Analytics"
                    st.rerun()

            with st.expander("Delete a Stored Profile"):
                del_id = st.number_input("Profile ID to delete", min_value=1, step=1, key="del_prof_id")
                if st.button("Delete Selected Profile", type="secondary"):
                    if db.delete_profile(int(del_id)):
                        st.success(f"Deleted profile ID {int(del_id)}.")
                        st.rerun()
                    else:
                        st.warning(f"Profile ID {int(del_id)} not found.")
        else:
            st.info("No stored profiles match your filter.")

    with tab_sim:
        sim_search = st.text_input("Search filenames or summary", key="hist_sim_search")
        sim_rows = db.get_similarity_history(limit=200, search=sim_search)
        if sim_rows:
            df = pd.DataFrame(sim_rows)[
                [
                    "id",
                    "file_a",
                    "file_b",
                    "overall_similarity",
                    "token_similarity",
                    "tfidf_similarity",
                    "sequence_similarity",
                    "ast_similarity",
                    "normalized_var_mode",
                    "analyzed_at",
                ]
            ].copy()
            df["analyzed_at"] = df["analyzed_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button(
                "Download Similarity History CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="similarity_history.csv",
                mime="text/csv",
            )
        else:
            st.info("No code similarity comparison records found.")

    with tab_ai:
        c1, c2 = st.columns([2, 1])
        with c1:
            ai_search = st.text_input("Search filename", key="hist_ai_search")
        with c2:
            ai_label = st.selectbox(
                "Label Filter",
                options=[
                    "All",
                    "Few indicators observed",
                    "Some indicators observed",
                    "Several indicators observed",
                ],
                key="hist_ai_label",
            )
        ai_rows = db.get_ai_pattern_history(limit=200, search=ai_search, label_filter=ai_label)
        if ai_rows:
            df = pd.DataFrame(ai_rows)[
                ["id", "filename", "indicator_score", "classification_label", "analyzed_at"]
            ].copy()
            df["analyzed_at"] = df["analyzed_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button(
                "Download Heuristic AI Analysis CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="ai_pattern_history.csv",
                mime="text/csv",
            )
        else:
            st.info("No heuristic AI-pattern analysis records found.")


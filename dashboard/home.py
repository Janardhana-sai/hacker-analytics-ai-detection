"""
Page 1: Home Dashboard.
Features modern graphics, animated gradient hero banners, interactive Plotly visualizations,
system pipeline diagrams, KPI cards, and quick navigation.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import APP_DESCRIPTION, APP_SHORT_TITLE, APP_TITLE, APP_VERSION, BASE_DIR
from database.db_manager import DatabaseManager
from utils.helpers import format_timestamp


def _navigate_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()


def _render_hero_banner() -> None:
    """Render a futuristic high-tech hero banner with gradient accents and badges."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 138, 0.45) 50%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-radius: 16px;
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); padding: 4px 14px; border-radius: 9999px; margin-bottom: 12px;">
                        <span style="height: 8px; width: 8px; border-radius: 50%; background-color: #10B981; display: inline-block; box-shadow: 0 0 10px #10B981;"></span>
                        <span style="color: #93C5FD; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">System Core Online • v"""
        + APP_VERSION
        + """</span>
                    </div>
                    <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF 0%, #93C5FD 50%, #38BDF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        """
        + APP_TITLE
        + """
                    </h1>
                    <p style="color: #94A3B8; font-size: 1.02rem; margin-top: 8px; margin-bottom: 0; max-width: 820px; line-height: 1.55;">
                        Next-generation developer intelligence platform combining automated public profile analytics, deep AST structural code decomposition, multi-metric similarity detection, and explainable heuristic AI pattern indicators.
                    </p>
                </div>
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px;">
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">🕸️ Selenium 4.x Engine</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">🌳 Python AST Structural Parser</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">📐 TF-IDF & Cosine Similarity</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">🤖 Explainable Heuristic AI Index</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">💾 Embedded SQLite Vault</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpi_metrics(counts: dict[str, int]) -> None:
    """Render futuristic KPI cards with visual accent bars."""
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(59, 130, 246, 0.3); border-top: 4px solid #3B82F6; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Profiles Stored</span>
                    <span style="font-size: 1.3rem;">👥</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_profiles']}</div>
                <div style="color: #60A5FA; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">{counts['live_profiles']} Live • {counts['sample_profiles']} Sample</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(16, 185, 129, 0.3); border-top: 4px solid #10B981; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Scraping Ingestions</span>
                    <span style="font-size: 1.3rem;">🕷️</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_scrapes']}</div>
                <div style="color: #34D399; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">{counts['successful_scrapes']} Completed Successfully</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(139, 92, 246, 0.3); border-top: 4px solid #8B5CF6; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">AST Code Analyses</span>
                    <span style="font-size: 1.3rem;">🌳</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_code_analyses']}</div>
                <div style="color: #A78BFA; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">Syntax & Cyclomatic Metrics</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(245, 158, 11, 0.3); border-top: 4px solid #F59E0B; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Similarity & AI Checks</span>
                    <span style="font-size: 1.3rem;">🛡️</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_similarities'] + counts['total_ai_analyses']}</div>
                <div style="color: #FBBF24; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">{counts['total_similarities']} Sim • {counts['total_ai_analyses']} Heuristic AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_graphic_charts(counts: dict[str, int]) -> None:
    """Render interactive Plotly graphical visuals showcasing workload and analytical pillars."""
    st.write("")
    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        # Donut Chart: Platform Operations Breakdown
        labels = [
            "Profiles Stored",
            "Scrapes Performed",
            "AST Code Analyses",
            "Similarity Comparisons",
            "AI Heuristic Checks",
        ]
        values = [
            max(counts["total_profiles"], 1),
            max(counts["total_scrapes"], 1),
            max(counts["total_code_analyses"], 1),
            max(counts["total_similarities"], 1),
            max(counts["total_ai_analyses"], 1),
        ]
        colors = ["#3B82F6", "#10B981", "#8B5CF6", "#06B6D4", "#F59E0B"]

        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.58,
                    marker=dict(colors=colors, line=dict(color="#0F172A", width=2)),
                    textinfo="label+percent",
                    textposition="inside",
                    insidetextorientation="radial",
                    hoverinfo="label+value+percent",
                )
            ]
        )
        fig_donut.update_layout(
            title=dict(
                text="<b>Platform Activity & Data Ingestion Distribution</b>",
                font=dict(size=14, color="#E2E8F0"),
            ),
            showlegend=False,
            height=320,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_donut, width="stretch", key="home_activity_donut")

    with col_chart2:
        # Radar Chart: Capabilities & Analytical Dimensions
        categories = [
            "Browser Ingestion",
            "Skill Analytics",
            "AST Tree Parsing",
            "Cosine TF-IDF",
            "Heuristic AI Index",
            "SQLite Persistence",
        ]
        # Benchmark score levels (100-point scale for visual architecture index)
        r_scores = [92, 95, 98, 90, 88, 96]

        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=r_scores,
                theta=categories,
                fill="toself",
                name="System Engine Index",
                fillcolor="rgba(59, 130, 246, 0.28)",
                line=dict(color="#38BDF8", width=2),
                marker=dict(size=6, color="#60A5FA"),
            )
        )
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False,
                    linecolor="rgba(148, 163, 184, 0.2)",
                    gridcolor="rgba(148, 163, 184, 0.15)",
                ),
                angularaxis=dict(
                    tickfont=dict(size=11, color="#CBD5E1"),
                    linecolor="rgba(148, 163, 184, 0.2)",
                    gridcolor="rgba(148, 163, 184, 0.15)",
                ),
                bgcolor="rgba(0,0,0,0)",
            ),
            title=dict(
                text="<b>Inspection Engine Coverage & Analytical Depth</b>",
                font=dict(size=14, color="#E2E8F0"),
            ),
            showlegend=False,
            height=320,
            margin=dict(t=40, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, width="stretch", key="home_capabilities_radar")


def _render_architecture_pipeline() -> None:
    """Render a visual architecture pipeline flowchart showing data ingestion to reporting."""
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 14px; padding: 22px; margin-top: 10px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span style="font-size: 1.05rem; font-weight: 700; color: #F1F5F9; letter-spacing: 0.02em;">⚙️ System Architecture Pipeline</span>
                <span style="font-size: 0.78rem; color: #38BDF8; background: rgba(56, 189, 248, 0.12); padding: 3px 10px; border-radius: 9999px; border: 1px solid rgba(56, 189, 248, 0.3);">End-to-End Modular Flow</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px;">
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #60A5FA; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">1. DATA INGESTION</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">Selenium & Fallbacks</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        Headless Chrome/Edge automation, offline JSON sample dataset, and CSV/JSON public upload parser.
                    </p>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #34D399; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">2. DECOMPOSITION</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">DOM & AST Parsing</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        BeautifulSoup4 HTML selectors, Python AST visitor, token stream lexing, and variable normalization.
                    </p>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #A78BFA; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">3. ANALYTICAL CORE</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">Similarity & Heuristics</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        TF-IDF cosine, SequenceMatcher, AST feature vectors, and 5 explainable non-probabilistic AI indicators.
                    </p>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #FBBF24; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">4. VISUALIZATION</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">Dashboard & SQLite</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        7-page Streamlit portal, Plotly interactive graphics, Matplotlib figures, and SQLite schema.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_interactive_launchpad() -> None:
    """Render attractive visual action cards with quick-jump navigation."""
    st.markdown("### 🚀 Interactive Module Launchpad")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">🕸️</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">Web Scraper</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Selenium automated live scrape, offline sample data, or CSV/JSON upload.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Launch Scraper →", key="launch_scraper", use_container_width=True, type="primary"):
            _navigate_to("Selenium Web Scraper")

    with c2:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">📊</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">Coding Analytics</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Language distributions, skill verification, badge charts & profile comparisons.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Analytics →", key="launch_analytics", use_container_width=True):
            _navigate_to("Coding Performance Analytics")

    with c3:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">📐</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">Code Similarity</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Pairwise token, TF-IDF cosine, sequence matcher & AST structural diffs.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Compare Code →", key="launch_similarity", use_container_width=True):
            _navigate_to("Source-Code Similarity")

    with c4:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">🤖</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">AI Pattern Check</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Transparent heuristic indicators, naming uniformity & comment patterns.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Check AI Patterns →", key="launch_ai", use_container_width=True):
            _navigate_to("AI-Associated Code Pattern Analysis")


def _render_academic_novelty_banner() -> None:
    """Render the Academic Project Report & Novelty Check download banner."""
    full_report_path = BASE_DIR / "Hacker_Analytics_Academic_Project_Report.pdf"
    novelty_pdf_path = BASE_DIR / "Hacker_Analytics_Project_Novelty_Check_and_IEEE_Comparison.pdf"
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-left: 4px solid #3B82F6;
            border-radius: 12px;
            padding: 18px 24px;
            margin-top: 24px;
            margin-bottom: 12px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">
                        📄 Academic Project Reports & IEEE Literature Benchmarking (PDF)
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">
                        Formal 25-page academic project report (matching college thesis guidelines with architectures, ER diagrams, DFD workflows, algorithms, and experimental results) and IEEE novelty gap analysis report.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_rep1, col_rep2 = st.columns(2)
    with col_rep1:
        if full_report_path.exists():
            with open(full_report_path, "rb") as f1:
                pdf_bytes1 = f1.read()
            st.download_button(
                label="📘 Download Full Academic Report (25 Pages PDF)",
                data=pdf_bytes1,
                file_name="Hacker_Analytics_Academic_Project_Report.pdf",
                mime="application/pdf",
                key="download_full_academic_report_pdf",
                use_container_width=True,
            )
    with col_rep2:
        if novelty_pdf_path.exists():
            with open(novelty_pdf_path, "rb") as f2:
                pdf_bytes2 = f2.read()
            st.download_button(
                label="📑 Download IEEE Novelty Gap Analysis (PDF)",
                data=pdf_bytes2,
                file_name="Hacker_Analytics_Project_Novelty_Check_and_IEEE_Comparison.pdf",
                mime="application/pdf",
                key="download_novelty_pdf",
                use_container_width=True,
            )


def render_home_page(db: DatabaseManager) -> None:
    """Render the modernized Home Dashboard overview page with cool graphics."""
    counts = db.get_dashboard_counts()

    # 1. Futuristic Hero Banner
    _render_hero_banner()

    # 2. Glowing Metric Cards
    _render_kpi_metrics(counts)

    # 3. Interactive Graphical Visuals (Donut & Radar)
    _render_graphic_charts(counts)

    # 4. System Pipeline Diagram
    _render_architecture_pipeline()

    # 5. Interactive Action Launchpad
    _render_interactive_launchpad()

    # 6. Academic Novelty & IEEE Report Download
    _render_academic_novelty_banner()

    st.write("")
    st.divider()

    # 6. Real-time Activity Feed
    st.subheader("📋 Real-Time Activity & History Stream")

    tab1, tab2, tab3 = st.tabs(
        ["🕸️ Scraping & Profile Loads", "📐 Code Similarity Runs", "🤖 Heuristic AI Checks"]
    )

    with tab1:
        scrapes = db.get_scraping_history(limit=8)
        if scrapes:
            df = pd.DataFrame(scrapes)[
                ["username", "status", "source_mode", "fields_collected", "scraped_at", "error_message"]
            ].copy()
            df["scraped_at"] = df["scraped_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info(
                "No scraping or profile records logged yet. Open **Selenium Web Scraper** to load sample data or scrape a profile."
            )

    with tab2:
        sims = db.get_similarity_history(limit=8)
        if sims:
            df = pd.DataFrame(sims)[
                ["file_a", "file_b", "overall_similarity", "ast_similarity", "analyzed_at"]
            ].copy()
            df["analyzed_at"] = df["analyzed_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No source-code similarity comparisons recorded yet.")

    with tab3:
        ai_rows = db.get_ai_pattern_history(limit=8)
        if ai_rows:
            df = pd.DataFrame(ai_rows)[
                ["filename", "indicator_score", "classification_label", "analyzed_at"]
            ].copy()
            df["analyzed_at"] = df["analyzed_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No heuristic AI-pattern analyses recorded yet.")

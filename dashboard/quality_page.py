"""
Page 8: Code Quality, Cyclomatic Complexity & Static Security Audit.
Calculates McCabe Cyclomatic Complexity, Maintainability Index (MI), Halstead Software Metrics,
and audits for security vulnerabilities and code smells.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import SAMPLE_DATA_DIR
from database.db_manager import DatabaseManager
from detection.code_quality import audit_code_quality
from utils.validators import validate_python_code


def _get_benchmark_files() -> list[tuple[str, str]]:
    files: list[tuple[str, str]] = []
    if SAMPLE_DATA_DIR.exists():
        for p in sorted(SAMPLE_DATA_DIR.glob("*.py")):
            try:
                files.append((p.name, p.read_text(encoding="utf-8")))
            except OSError:
                pass
    return files


def render_quality_page(db: DatabaseManager) -> None:
    """Render the Code Quality & Security Audit page."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(13, 148, 136, 0.35) 50%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(20, 184, 166, 0.35);
            border-radius: 16px;
            padding: 22px 28px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.4);
        ">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(20, 184, 166, 0.15); border: 1px solid rgba(20, 184, 166, 0.4); padding: 3px 12px; border-radius: 9999px; margin-bottom: 8px;">
                <span style="font-size: 0.75rem; font-weight: 700; color: #5EEAD4; letter-spacing: 0.04em;">NEW MODULE • SOFTWARE ENGINEERING AUDIT</span>
            </div>
            <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF, #5EEAD4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🛡️ Code Quality, Cyclomatic Complexity & Security Audit
            </h1>
            <p style="color: #94A3B8; font-size: 0.92rem; margin: 4px 0 0 0;">
                Calculates McCabe's Cyclomatic Complexity V(G), Coleman-Oman Maintainability Index (MI), Halstead Software Science, and static security risk patterns.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    benchmarks = _get_benchmark_files()
    tab_bench, tab_custom = st.tabs(["🧪 Select Benchmark Python File", "📝 Paste or Upload Custom Code"])

    active_code: str = ""
    active_filename: str = "custom_code.py"

    with tab_bench:
        if benchmarks:
            bench_names = [b[0] for b in benchmarks]
            selected_bench = st.selectbox(
                "Choose Benchmark File to Audit",
                options=bench_names,
                index=0,
            )
            for name, code in benchmarks:
                if name == selected_bench:
                    active_code = code
                    active_filename = name
                    break

            with st.expander("Preview Selected Source Code", expanded=False):
                st.code(active_code, language="python")

    with tab_custom:
        custom_upload = st.file_uploader("Upload Python (.py) File", type=["py"], key="quality_file_uploader")
        if custom_upload:
            active_code = custom_upload.getvalue().decode("utf-8", errors="replace")
            active_filename = custom_upload.name
        else:
            pasted = st.text_area(
                "Or Paste Python Code",
                height=180,
                placeholder="def example():\n    pass",
                key="quality_pasted_code",
            )
            if pasted.strip():
                active_code = pasted
                active_filename = "pasted_snippet.py"

    if not active_code.strip():
        st.info("Select a benchmark file or paste code above to run the Code Quality & Security Audit.")
        return

    st.write("")
    if st.button("🚀 Run Deep Code Quality & Security Audit", type="primary", use_container_width=True):
        st.session_state["quality_audit_run"] = True

    if not st.session_state.get("quality_audit_run", True):
        return

    report = audit_code_quality(active_code)

    if not report["syntax_valid"]:
        st.error(f"❌ Syntax Error: {report['error_message']}")
        return

    st.divider()
    st.subheader(f"📊 Audit Results for `{active_filename}`")

    # 1. KPI Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Maintainability Index", f"{report['maintainability_index']}/100", report['maintainability_grade'])
    with k2:
        st.metric("Total Complexity V(G)", str(report['overall_complexity']))
    with k3:
        st.metric("Lines of Code (LOC)", str(report['lines_of_code']), f"{report['source_lines']} SLOC")
    with k4:
        st.metric("Max Nesting Depth", str(report['max_nesting_depth']), "Levels")
    with k5:
        issues_count = len(report['security_issues']) + len(report['code_smells'])
        st.metric("Detected Issues", str(issues_count), "Alerts" if issues_count > 0 else "Clean")

    # 2. Visual Charts: Maintainability Gauge & Complexity Distribution
    c_chart1, c_chart2 = st.columns([1, 1.3])

    with c_chart1:
        gauge_fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=report["maintainability_index"],
                title={"text": "Maintainability Score (MI)", "font": {"size": 15}},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": report["maintainability_color"]},
                    "steps": [
                        {"range": [0, 40], "color": "rgba(239, 68, 68, 0.2)"},
                        {"range": [40, 60], "color": "rgba(245, 158, 11, 0.2)"},
                        {"range": [60, 80], "color": "rgba(59, 130, 246, 0.2)"},
                        {"range": [80, 100], "color": "rgba(16, 185, 129, 0.2)"},
                    ],
                },
            )
        )
        gauge_fig.update_layout(height=280, margin=dict(t=30, b=10, l=20, r=20))
        st.plotly_chart(gauge_fig, width="stretch", key="quality_mi_gauge")

    with c_chart2:
        if report["functions"]:
            fn_df = pd.DataFrame(report["functions"])
            bar_fig = px.bar(
                fn_df,
                x="name",
                y="complexity",
                color="risk_rating",
                color_discrete_map={"Low": "#10B981", "Medium": "#F59E0B", "High": "#EF4444"},
                title="Function-Level Cyclomatic Complexity V(G)",
                labels={"name": "Function Name", "complexity": "Complexity V(G)"},
            )
            bar_fig.add_hline(y=5, line_dash="dot", line_color="#F59E0B", annotation_text="Moderate Risk (5)")
            bar_fig.add_hline(y=10, line_dash="dash", line_color="#EF4444", annotation_text="High Risk (10)")
            bar_fig.update_layout(height=280, margin=dict(t=35, b=20, l=20, r=20))
            st.plotly_chart(bar_fig, width="stretch", key="quality_fn_complexity_chart")
        else:
            st.info("No standalone function definitions detected in this module.")

    # 3. Security & Code Smells Alerts
    st.subheader("🚨 Security & Static Code Smell Alerts")
    sec_col1, sec_col2 = st.columns(2)

    with sec_col1:
        st.markdown("#### Security Vulnerability Checks")
        if report["security_issues"]:
            for issue in report["security_issues"]:
                st.error(
                    f"**[{issue['severity']}] {issue['type']}** at Line {issue['line']}:  \n"
                    f"`{issue['target']}` — {issue['description']}"
                )
        else:
            st.success("✅ No dangerous functions (eval, exec, command injection, insecure deserialization) detected.")

    with sec_col2:
        st.markdown("#### Anti-Patterns & Code Smells")
        if report["code_smells"]:
            for smell in report["code_smells"]:
                st.warning(
                    f"**[{smell['severity']}] {smell['type']}** at Line {smell['line']}:  \n"
                    f"{smell['description']}"
                )
        else:
            st.success("✅ No bare except clauses or excessive nesting anti-patterns detected.")

    # 4. Halstead Software Science Breakdown
    st.subheader("📐 Halstead Software Science Metrics")
    h = report["halstead"]
    hc1, hc2, hc3, hc4 = st.columns(4)
    hc1.metric("Vocabulary (n)", str(h.get("vocabulary", 0)))
    hc2.metric("Program Length (N)", str(h.get("length", 0)))
    hc3.metric("Volume (V)", f"{h.get('volume', 0)} bits")
    hc4.metric("Difficulty (D)", str(h.get("difficulty", 0)))

    # 5. Functions Table
    if report["functions"]:
        st.subheader("📋 Function-Level Granular Breakdown")
        f_display = pd.DataFrame(report["functions"])[
            ["name", "line_number", "lines_count", "complexity", "risk_rating", "has_docstring", "args_count"]
        ]
        st.dataframe(f_display, use_container_width=True, hide_index=True)

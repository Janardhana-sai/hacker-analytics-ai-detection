"""
Page 6: Heuristic AI-Associated Code Pattern Analysis & AST Inspection.
Displays explainable heuristic indicator scores, non-probabilistic labels,
individual indicator rationales, AST structural summary, cross-submission analysis,
and explicit limitations.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import AI_DETECTION_DISCLAIMER, SAMPLE_DATA_DIR
from database.db_manager import DatabaseManager
from detection.ai_pattern_analysis import analyze_ai_patterns
from utils.validators import validate_python_code

SAMPLE_DESCRIPTIONS: dict[str, str] = {
    "sample_code_ai_assistant.py": "🤖 AI Assistant Style (Step-by-step comments, full docstrings, typing)",
    "sample_code_ai_plagiarized.py": "🪞 AI Paraphrased Clone (Identical AST logic, renamed variables)",
    "sample_code_human_expert.py": "🧑‍💻 Human Senior Engineer (Idiomatic, clean generator & dict logic)",
    "sample_code_student_messy.py": "🎒 Student Scratchpad (Manual loops, informal comments, quirks)",
    "sample_code_ai_oop_pattern.py": "🏗️ AI Interview Wrapper (Class boilerplate, method typing)",
    "sample_code_lru_cache_ai.py": "⚡ LRU Cache AI Doubly-Linked (Exhaustive methods & docstrings)",
    "sample_code_lru_cache_human.py": "🐍 LRU Cache Human (Idiomatic OrderedDict standard library)",
    "sample_code_1.py": "📘 Two-Sum & Subarray Baseline 1 (Structured with type hints)",
    "sample_code_2.py": "📙 Two-Sum & Subarray Baseline 2 (Terse competitive style)",
}


def _get_all_sample_files() -> list[tuple[str, str]]:
    """Return all available sample Python files from sample_data/."""
    files: list[tuple[str, str]] = []
    if SAMPLE_DATA_DIR.exists():
        for path in sorted(SAMPLE_DATA_DIR.glob("*.py")):
            try:
                content = path.read_text(encoding="utf-8")
                files.append((path.name, content))
            except OSError:
                pass
    return files


def _render_indicator_gauge(score: float, label: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 100", "font": {"color": "#F8FAFC", "size": 34}},
            title={
                "text": f"<b>Heuristic Indicator Index</b><br><span style='font-size:0.85em;color:#93C5FD'>{label}</span>",
                "font": {"color": "#E2E8F0"},
            },
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                "bar": {"color": "#3B82F6", "thickness": 0.28},
                "bgcolor": "rgba(30, 41, 59, 0.5)",
                "borderwidth": 1,
                "bordercolor": "rgba(148, 163, 184, 0.2)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(16, 185, 129, 0.25)"},
                    {"range": [35, 65], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [65, 100], "color": "rgba(239, 68, 68, 0.25)"},
                ],
            },
        )
    )
    fig.update_layout(
        height=280,
        margin=dict(t=60, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def render_ai_detection_page(db: DatabaseManager) -> None:
    """Render the Heuristic AI-Associated Code Pattern Analysis page."""
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
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); padding: 3px 12px; border-radius: 9999px; margin-bottom: 8px;">
                <span style="font-size: 0.75rem; font-weight: 700; color: #93C5FD; letter-spacing: 0.04em;">MODULE 6 • HEURISTIC PATTERNS</span>
            </div>
            <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF, #93C5FD); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🤖 AI-Associated Code Pattern Analysis (Heuristic)
            </h1>
            <p style="color: #94A3B8; font-size: 0.92rem; margin: 4px 0 0 0;">
                Transparent, explainable structural evaluation examining naming conventions, formatting symmetry, comment narration, and AST scaffolding.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.warning(AI_DETECTION_DISCLAIMER, icon="⚠️")

    input_mode = st.radio(
        "Source Code Input Method",
        options=["Load Curated Benchmark Code", "Upload Python File", "Paste Python Code"],
        horizontal=True,
    )

    filename = "pasted_snippet.py"
    code_text = ""
    all_samples = _get_all_sample_files()
    sample_names = [f[0] for f in all_samples]

    if input_mode == "Load Curated Benchmark Code":
        st.markdown(
            "Select any of our **9 benchmark files** representing classic AI assistant outputs, "
            "paraphrased clones, human expert solutions, or student scratchpad drafts:"
        )
        sample_choice = st.selectbox(
            "Select Benchmark Code File",
            options=sample_names,
            format_func=lambda s: SAMPLE_DESCRIPTIONS.get(s, s),
        )
        for s_name, s_content in all_samples:
            if s_name == sample_choice:
                filename = s_name
                code_text = s_content
                break

        with st.expander(f"Preview `{filename}`"):
            st.code(code_text, language="python")

    elif input_mode == "Upload Python File":
        uf = st.file_uploader("Upload a Python (.py) File", type=["py"], key="ai_single_upload")
        if uf is not None:
            filename = uf.name
            code_text = uf.getvalue().decode("utf-8", errors="replace")
    else:
        filename = st.text_input("Snippet Filename Label", value="submitted_solution.py")
        code_text = st.text_area(
            "Paste Python Source Code",
            height=220,
            placeholder="def solve(nums):\n    ...",
        )

    st.write("")
    col_p1, col_p2 = st.columns([2.5, 1.5])
    with col_p1:
        auto_peers = st.checkbox(
            "Include other benchmark files as cross-submission peers",
            value=True,
            help="Automatically evaluates the 5th indicator (Cross-Submission Similarity) against other benchmark solutions.",
        )
    with col_p2:
        custom_peer_files = st.file_uploader(
            "Or upload custom peer submissions (.py)",
            type=["py"],
            accept_multiple_files=True,
            key="ai_peer_uploads",
        )

    peer_codes: list[tuple[str, str]] = []
    if auto_peers:
        for s_name, s_content in all_samples:
            if s_name != filename:
                peer_codes.append((s_name, s_content))

    if custom_peer_files:
        for pf in custom_peer_files:
            p_raw = pf.getvalue().decode("utf-8", errors="replace")
            ok, _ = validate_python_code(p_raw, pf.name)
            if ok and pf.name != filename:
                peer_codes.append((pf.name, p_raw))

    if st.button("Analyse Code Patterns", type="primary"):
        ok, msg = validate_python_code(code_text, filename if filename.endswith(".py") else "")
        if not ok:
            st.error(msg)
            return

        with st.spinner("Running AST inspection and heuristic pattern evaluation..."):
            result = analyze_ai_patterns(
                code=code_text,
                filename=filename,
                peer_codes=peer_codes if peer_codes else None,
            )
            ast_sum = result["ast_summary"]
            db.save_code_analysis(ast_sum)
            db.save_ai_pattern_result(result)
            st.session_state["last_ai_pattern_result"] = result
            st.success("Heuristic pattern analysis complete and saved to history.")

    res = st.session_state.get("last_ai_pattern_result")
    if not res:
        st.info("Choose or upload a Python file above and click **Analyse Code Patterns**.")
        return

    st.divider()
    col_gauge, col_summary = st.columns([1.2, 1.8])
    with col_gauge:
        st.plotly_chart(
            _render_indicator_gauge(res["indicator_score"], res["classification_label"]),
            width="stretch",
            key="ai_indicator_gauge_chart",
        )
    with col_summary:
        st.subheader(f"Classification: {res['classification_label']}")
        st.metric(
            "Overall Heuristic Indicator Index (Not a Probability)",
            f"{res['indicator_score']:.1f} / 100",
        )
        st.markdown(f"**Target Analyzed:** `{res['filename']}`")
        st.markdown("##### Key Characteristics Influencing This Score")
        for char_item in res["influencing_characteristics"]:
            st.markdown(f"- {char_item}")

    st.divider()
    st.subheader("Individual Heuristic Indicators & Normal Practice Distinction")
    for ind in res["indicators"]:
        with st.expander(
            f"{ind['name']} — {ind['score']:.1f}/100 ({ind['observation']})", expanded=True
        ):
            st.progress(min(max(int(ind["score"]), 0), 100))
            st.markdown(f"**Why this is examined:** {ind['explanation']}")
            st.markdown(f"**Distinction from normal programming:** {ind['normal_practice_note']}")
            if ind["evidence"]:
                st.caption("Observed evidence: " + " | ".join(ind["evidence"]))

    st.divider()
    st.subheader("AST Structural Breakdown")
    ast_sum = res["ast_summary"]
    if not ast_sum.get("syntax_valid"):
        err = ast_sum.get("syntax_error") or {}
        st.error(
            f"Python SyntaxError at line {err.get('line')}: {err.get('message')} (`{err.get('text')}`)"
        )
    else:
        a1, a2, a3, a4, a5 = st.columns(5)
        a1.metric("Lines of Code", ast_sum["lines_of_code"])
        a2.metric("Functions", ast_sum["num_functions"])
        a3.metric("Classes", ast_sum["num_classes"])
        a4.metric("Loops / Conds", f"{ast_sum['num_loops']} / {ast_sum['num_conditionals']}")
        a5.metric(
            "Complexity",
            f"{ast_sum['approx_cyclomatic_complexity']} ({ast_sum['complexity_level']})",
        )

        if ast_sum.get("function_definitions"):
            st.markdown("##### Extracted Function Definitions")
            st.dataframe(
                pd.DataFrame(ast_sum["function_definitions"]),
                use_container_width=True,
                hide_index=True,
            )

    st.divider()
    st.subheader("Analysis Limitations & Ethical Guidelines (Important)")
    for lim in res["limitations"]:
        st.markdown(f"- {lim}")

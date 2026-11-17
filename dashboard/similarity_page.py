"""
Page 5: Source-Code Similarity & AST Structural Comparison.
Supports uploading custom Python files or choosing from a rich curated benchmark
library of 9 sample Python files (AI-generated, paraphrased clones, human expert,
OOP wrappers, and student draft implementations).
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from config import SAMPLE_DATA_DIR, SIMILARITY_DISCLAIMER
from database.db_manager import DatabaseManager
from detection.code_similarity import compare_multiple_files
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


def render_similarity_page(db: DatabaseManager) -> None:
    """Render the Source-Code Similarity Analysis page."""
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
                <span style="font-size: 0.75rem; font-weight: 700; color: #93C5FD; letter-spacing: 0.04em;">MODULE 4 & 5 • CODE INSPECTION</span>
            </div>
            <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF, #93C5FD); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                📐 Source-Code Similarity & AST Structural Comparison
            </h1>
            <p style="color: #94A3B8; font-size: 0.92rem; margin: 4px 0 0 0;">
                Multi-metric pairwise comparison using token Jaccard/cosine, TF-IDF, SequenceMatcher, and AST node distribution.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.warning(SIMILARITY_DISCLAIMER, icon="⚖️")

    tab_library, tab_upload = st.tabs(
        ["🧪 Curated Benchmark Code Library (9 Files)", "📁 Upload Custom Python Files"]
    )

    all_samples = _get_all_sample_files()
    sample_names = [f[0] for f in all_samples]

    files_to_compare: list[tuple[str, str]] = []

    with tab_library:
        st.markdown(
            "Select from our curated set of **9 benchmark Python files** showcasing different "
            "author archetypes (AI Assistant, Paraphrased Clones, Senior Python, Student Scratchpad, OOP Wrapper, and LRU Cache pairs)."
        )

        c_lib1, c_lib2 = st.columns([3, 1])
        with c_lib1:
            selected_samples = st.multiselect(
                "Choose Benchmark Files to Compare",
                options=sample_names,
                default=[
                    "sample_code_ai_assistant.py",
                    "sample_code_ai_plagiarized.py",
                    "sample_code_human_expert.py",
                ],
                format_func=lambda s: SAMPLE_DESCRIPTIONS.get(s, s),
            )
        with c_lib2:
            st.write("")
            st.write("")
            load_all_btn = st.button("Select All 9 Files", use_container_width=True)
            if load_all_btn:
                selected_samples = sample_names

        with st.expander("Preview Selected Benchmark Code Snippets"):
            if selected_samples:
                prev_choice = st.selectbox("Inspect Code", options=selected_samples, format_func=lambda s: SAMPLE_DESCRIPTIONS.get(s, s))
                for name, content in all_samples:
                    if name == prev_choice:
                        st.code(content, language="python")

        if st.button("Load Selected Benchmark Files", type="primary"):
            st.session_state["similarity_active_files"] = [
                (name, content) for name, content in all_samples if name in selected_samples
            ]
            st.session_state["similarity_source_mode"] = "benchmark"
            st.success(f"Loaded {len(selected_samples)} benchmark files ready for comparison!")

    with tab_upload:
        st.markdown("Upload two or more custom Python files (`.py`) for pairwise similarity analysis.")
        uploaded_files = st.file_uploader(
            "Upload Python Files",
            type=["py"],
            accept_multiple_files=True,
            key="similarity_custom_uploader",
        )
        if uploaded_files and st.button("Load Uploaded Files", type="primary"):
            valid_uploads: list[tuple[str, str]] = []
            for uf in uploaded_files:
                raw_text = uf.getvalue().decode("utf-8", errors="replace")
                ok, msg = validate_python_code(raw_text, uf.name)
                if ok:
                    valid_uploads.append((uf.name, raw_text))
                else:
                    st.error(msg)
            if len(valid_uploads) >= 2:
                st.session_state["similarity_active_files"] = valid_uploads
                st.session_state["similarity_source_mode"] = "upload"
                st.success(f"Loaded {len(valid_uploads)} uploaded files ready for comparison!")
            else:
                st.warning("Please upload at least 2 valid Python (.py) files.")

    # Active file pool
    active_files: list[tuple[str, str]] = st.session_state.get("similarity_active_files") or [
        (name, content) for name, content in all_samples if name in [
            "sample_code_ai_assistant.py",
            "sample_code_ai_plagiarized.py",
            "sample_code_human_expert.py",
        ]
    ]

    st.divider()
    st.subheader(f"Active Comparison Pool ({len(active_files)} Files)")

    col_opt1, col_opt2 = st.columns([2.5, 1.5])
    with col_opt1:
        current_names = [n for n, _ in active_files]
        chosen_names = st.multiselect(
            "Active Files Included in Similarity Analysis",
            options=current_names,
            default=current_names,
            format_func=lambda s: SAMPLE_DESCRIPTIONS.get(s, s),
        )
    with col_opt2:
        st.write("")
        normalize_vars = st.checkbox(
            "Normalise Identifiers (VAR_1, VAR_2, ...)",
            value=False,
            help="Normalizes variable and function names. Excellent for detecting paraphrased / renamed clones!",
        )

    chosen_files = [(n, c) for n, c in active_files if n in chosen_names]

    if len(chosen_files) < 2:
        st.warning("Select at least 2 files to run similarity comparison.")
        return

    if st.button("Run Multi-Metric Similarity Analysis", type="primary", use_container_width=False):
        with st.spinner("Tokenizing, building AST trees, computing TF-IDF and sequence matches..."):
            multi_result = compare_multiple_files(chosen_files, normalize_identifiers=normalize_vars)
            for pair in multi_result["pair_results"]:
                db.save_similarity_result(
                    {
                        "file_a": pair["file_a"],
                        "file_b": pair["file_b"],
                        "overall_similarity": pair["overall_similarity"],
                        "token_similarity": pair["token_similarity"],
                        "tfidf_similarity": pair["tfidf_similarity"],
                        "sequence_similarity": pair["sequence_similarity"],
                        "ast_similarity": pair["ast_similarity"],
                        "normalized_var_mode": pair["normalized_var_mode"],
                        "summary_text": pair["summary_text"],
                        "details": {
                            "structural_similarities": pair["structural_similarities"],
                            "structural_differences": pair["structural_differences"],
                        },
                    }
                )
            st.session_state["last_similarity_multi"] = multi_result
            st.success(f"Analysis complete across {len(multi_result['pair_results'])} pairwise combinations!")

    multi = st.session_state.get("last_similarity_multi")
    if not multi:
        return

    st.divider()
    st.subheader("Pairwise Similarity Matrix (%)")
    matrix_df = pd.DataFrame(
        multi["similarity_matrix"],
        index=multi["filenames"],
        columns=multi["filenames"],
    )
    fig = px.imshow(
        matrix_df,
        text_auto=".1f",
        color_continuous_scale="Blues",
        zmin=0,
        zmax=100,
        title="Cross-File Overall Similarity Heatmap (%)",
    )
    fig.update_layout(height=420, margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, width="stretch", key="similarity_heatmap_chart")

    pairs = multi["pair_results"]
    pair_labels = [f"{p['file_a']}  vs  {p['file_b']} ({p['overall_similarity']:.1f}%)" for p in pairs]
    selected_idx = st.selectbox(
        "Inspect Detailed Pair Comparison & AST Structural Diff",
        options=list(range(len(pairs))),
        format_func=lambda i: pair_labels[i],
    )
    pair = pairs[selected_idx]

    st.markdown(f"**Analysis Summary:** {pair['summary_text']}")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Overall Score", f"{pair['overall_similarity']:.1f}%")
    m2.metric("Token Match", f"{pair['token_similarity']:.1f}%")
    m3.metric("TF-IDF Cosine", f"{pair['tfidf_similarity']:.1f}%")
    m4.metric("Sequence Ratio", f"{pair['sequence_similarity']:.1f}%")
    m5.metric("AST Structure", f"{pair['ast_similarity']:.1f}%")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Structural Similarities")
        if pair["structural_similarities"]:
            for item in pair["structural_similarities"]:
                st.markdown(f"- {item}")
        else:
            st.caption("No identical high-level structural counts observed.")
    with c2:
        st.markdown("#### Structural Differences")
        if pair["structural_differences"]:
            for item in pair["structural_differences"]:
                st.markdown(f"- {item}")
        else:
            st.caption("No structural count differences observed.")

    st.markdown("#### AST Structural Feature Comparison")
    ast_a, ast_b = pair["ast_a"], pair["ast_b"]
    ast_comp_df = pd.DataFrame(
        [
            {"Feature": "Syntax Valid", pair["file_a"]: ast_a["syntax_valid"], pair["file_b"]: ast_b["syntax_valid"]},
            {"Feature": "Lines of Code", pair["file_a"]: ast_a["lines_of_code"], pair["file_b"]: ast_b["lines_of_code"]},
            {"Feature": "Functions", pair["file_a"]: ast_a["num_functions"], pair["file_b"]: ast_b["num_functions"]},
            {"Feature": "Classes", pair["file_a"]: ast_a["num_classes"], pair["file_b"]: ast_b["num_classes"]},
            {"Feature": "Loops", pair["file_a"]: ast_a["num_loops"], pair["file_b"]: ast_b["num_loops"]},
            {"Feature": "Conditionals", pair["file_a"]: ast_a["num_conditionals"], pair["file_b"]: ast_b["num_conditionals"]},
            {"Feature": "Imports", pair["file_a"]: ast_a["num_imports"], pair["file_b"]: ast_b["num_imports"]},
            {"Feature": "Assignments", pair["file_a"]: ast_a["num_assignments"], pair["file_b"]: ast_b["num_assignments"]},
            {"Feature": "Max Nesting Depth", pair["file_a"]: ast_a["max_nesting_depth"], pair["file_b"]: ast_b["max_nesting_depth"]},
            {"Feature": "Approx. Complexity", pair["file_a"]: ast_a["approx_cyclomatic_complexity"], pair["file_b"]: ast_b["approx_cyclomatic_complexity"]},
        ]
    )
    st.dataframe(ast_comp_df, use_container_width=True, hide_index=True)

    if pair["matching_sections"]:
        with st.expander("Matching Normalized Code Sections"):
            for idx, snippet in enumerate(pair["matching_sections"], start=1):
                st.caption(f"Section {idx}")
                st.code(snippet, language="python")

    if pair["diff_lines"]:
        with st.expander("Unified Source Diff"):
            st.code("\n".join(pair["diff_lines"]), language="diff")

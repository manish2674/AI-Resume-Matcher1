
import json

import pandas as pd
import streamlit as st

from core.matching_pipeline import run_matching_pipeline


st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide"
)


# ---------- Dashboard Styling ----------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero {
        padding: 1.5rem 1.7rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 14px;
        margin-bottom: 1.5rem;
        background: linear-gradient(
            120deg,
            rgba(49, 105, 190, 0.10),
            rgba(49, 105, 190, 0.025)
        );
    }

    .hero h1 {
        margin: 0 0 0.35rem 0;
        font-size: 2rem;
        font-weight: 750;
    }

    .hero p {
        margin: 0;
        color: var(--text-color);
        opacity: 0.78;
        font-size: 1rem;
    }

    .section-heading {
        margin: 1.7rem 0 0.35rem 0;
        padding-bottom: 0.55rem;
        border-bottom: 2px solid rgba(49, 105, 190, 0.55);
        font-size: 1.25rem;
        font-weight: 700;
    }

    .section-caption {
        margin: 0 0 0.85rem 0;
        color: var(--text-color);
        opacity: 0.7;
        font-size: 0.9rem;
    }

    div[data-testid="stMetric"] {
        padding: 0.85rem 1rem;
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 10px;
        background: rgba(128, 128, 128, 0.035);
    }

    div.stButton > button,
    div[data-testid="stDownloadButton"] button {
        border-radius: 8px;
        font-weight: 650;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------- Reusable Section Heading ----------
def section_heading(title, subtitle=None):
    """Render a consistent heading with an underline."""

    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True
    )

    if subtitle:
        st.markdown(
            f'<div class="section-caption">{subtitle}</div>',
            unsafe_allow_html=True
        )


# ---------- Ranking Table ----------
def prepare_ranking_table(candidates):
    """Prepare candidate data for the ranking dashboard."""

    rows = []

    for candidate in candidates:

        experience = candidate.get("experience", {})
        skills = candidate.get("skills", {})

        rows.append({
            "Rank": candidate.get("rank"),

            "Candidate": candidate.get(
                "candidate_name", "Unknown"
            ),

            "Match Score (%)": candidate.get(
                "final_score", 0
            ),

            "Experience (Years)": experience.get(
                "total_experience_years"
            ),

            "Email": candidate.get("email") or "Not found",

            "Matched Required Skills": ", ".join(
                skills.get("matched_required", [])
            ),
        })

    return pd.DataFrame(rows)


# ---------- Skill Display ----------
def display_skill_list(title, skills):
    """Display matched or missing skills."""

    st.write(f"**{title}**")

    if skills:
        st.write(", ".join(skills))
    else:
        st.write("None")


# ==========================================================
# MAIN DASHBOARD
# ==========================================================

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>📄 AI-Based Resume Matching System</h1>
        <p>
            Intelligent resume screening, semantic matching,
            and candidate ranking
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- 01. Job Description ----------
section_heading(
    "01 · Job Description",
    "Paste the complete job description to define candidate requirements."
)

jd_text = st.text_area(
    "Paste the complete Job Description here",
    height=220,
    placeholder="Paste the complete job description..."
)


# ---------- 02. Resume Upload ----------
section_heading(
    "02 · Upload Candidate Resumes",
    "Upload multiple PDF or DOCX resumes for evaluation."
)

uploaded_files = st.file_uploader(
    "Upload PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(
        f"{len(uploaded_files)} resume(s) selected."
    )

st.caption(
    "Upload multiple PDF and DOCX resumes in one batch. "
    "Ten synthetic resumes are available for demonstration."
)

st.divider()


# ---------- 03. Analyze Candidates ----------
if st.button(
    "Analyze and Rank Candidates",
    type="primary",
    width="stretch"
):

    if not jd_text.strip():

        st.error("Please enter a Job Description.")

    elif not uploaded_files:

        st.error("Please upload at least one resume.")

    else:

        resume_files = [
            (file.name, file.getvalue())
            for file in uploaded_files
        ]

        with st.spinner(
            "Analyzing resumes and calculating matching scores..."
        ):

            try:

                results = run_matching_pipeline(
                    jd_text,
                    resume_files
                )

                st.session_state["matching_results"] = results

            except Exception as error:

                st.error(
                    f"An unexpected error occurred: {error}"
                )


# ==========================================================
# RESULTS DASHBOARD
# ==========================================================

if "matching_results" in st.session_state:

    results = st.session_state["matching_results"]

    candidates = results.get("ranked_candidates", [])

    st.divider()

    st.header("03 · Candidate Ranking Dashboard")


    # ---------- Summary Metrics ----------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Resumes",
        results.get("total_resumes", 0)
    )

    col2.metric(
        "Successfully Processed",
        results.get("successfully_processed", 0)
    )

    col3.metric(
        "Failed Resumes",
        results.get("failed_resumes", 0)
    )


    if candidates:

        # ---------- Candidate Rankings ----------
        ranking_df = prepare_ranking_table(candidates)

        section_heading(
            "Candidate Rankings",
            "Candidates are ordered by their overall matching score."
        )

        st.dataframe(
            ranking_df,
            width="stretch",
            hide_index=True
        )


        # ---------- Individual Candidate Analysis ----------
        section_heading(
            "04 · Individual Candidate Analysis",
            "Select a candidate to inspect matching evidence and score breakdown."
        )

        candidate_options = {
            (
                f"Rank {candidate.get('rank')} - "
                f"{candidate.get('candidate_name', 'Unknown')}"
            ): candidate

            for candidate in candidates
        }

        selected_name = st.selectbox(
            "Select a candidate",
            list(candidate_options.keys())
        )

        selected_candidate = candidate_options[selected_name]

        st.divider()

        st.markdown(
            f"### {selected_candidate.get('candidate_name', 'Candidate')}"
        )


        # ---------- Candidate Summary ----------
        score_col1, score_col2 = st.columns(2)

        score_col1.metric(
            "Overall Match Score",
            f"{selected_candidate.get('final_score', 0):.2f}%"
        )

        score_col2.metric(
            "Candidate Rank",
            f"#{selected_candidate.get('rank', '-')}"
        )

        st.write(
            "**Email:**",
            selected_candidate.get("email") or "Not found"
        )

        st.write(
            "**Phone:**",
            selected_candidate.get("phone") or "Not found"
        )

        st.write(
            "**Resume:**",
            selected_candidate.get("filename", "Unknown")
        )


        # ---------- Experience Analysis ----------
        section_heading("Experience Analysis")

        experience = selected_candidate.get("experience", {})

        experience_col1, experience_col2 = st.columns(2)

        candidate_years = experience.get(
            "total_experience_years"
        )

        required_years = experience.get(
            "required_experience_years"
        )

        experience_col1.metric(
            "Candidate Experience",
            (
                f"{candidate_years} years"
                if candidate_years is not None
                else "Not detected"
            )
        )

        experience_col2.metric(
            "Required Experience",
            (
                f"{required_years} years"
                if required_years is not None
                else "Not specified"
            )
        )

        st.info(
            experience.get(
                "status",
                "Experience analysis unavailable."
            )
        )


        # ---------- Skill Analysis ----------
        section_heading("Skill Analysis")

        skills = selected_candidate.get("skills", {})

        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:

            display_skill_list(
                "Matched Required Skills",
                skills.get("matched_required", [])
            )

            display_skill_list(
                "Matched Preferred Skills",
                skills.get("matched_preferred", [])
            )

        with skill_col2:

            display_skill_list(
                "Missing Required Skills",
                skills.get("missing_required", [])
            )

            display_skill_list(
                "Missing Preferred Skills",
                skills.get("missing_preferred", [])
            )

        st.info(
            skills.get(
                "status",
                "Skill analysis unavailable."
            )
        )


        # ---------- Score Breakdown ----------
        section_heading("Score Breakdown")

        component_scores = selected_candidate.get(
            "component_scores", {}
        )

        score_labels = {
            "skills": "Skills",
            "semantic": "Semantic Similarity",
            "experience": "Experience",
            "qualification": "Qualification",
        }

        score_columns = st.columns(4)

        for index, (key, label) in enumerate(
            score_labels.items()
        ):

            score = component_scores.get(key)

            with score_columns[index]:

                st.metric(
                    label,
                    (
                        f"{score:.2f}%"
                        if score is not None
                        else "N/A"
                    )
                )


        # ---------- Qualification Analysis ----------
        section_heading("Qualification Analysis")

        qualifications = selected_candidate.get(
            "qualifications", {}
        )

        st.write(
            "**Detected Qualifications:**",

            ", ".join(
                qualifications.get(
                    "detected_qualifications", []
                )
            ) or "None"
        )

        display_skill_list(
            "Matched Required Qualifications",
            qualifications.get("matched", [])
        )

        display_skill_list(
            "Matched Preferred Qualifications",
            qualifications.get("matched_preferred", [])
        )

        st.write(
            "**Qualification Status:**",
            qualifications.get("status", "Unavailable")
        )

        st.write(
            "**Explanation:**",
            qualifications.get(
                "match_reason",
                "No explanation available."
            )
        )


        # ---------- Candidate Explanation ----------
        section_heading(
            "Why This Candidate Received This Score"
        )

        reasons = selected_candidate.get("reasons", [])

        if reasons:

            for reason in reasons:
                st.write(f"- {reason}")

        else:

            st.info("No additional explanation available.")


        st.divider()


        # ---------- Download Reports ----------
        section_heading(
            "05 · Download Reports",
            "Export the ranked results for further review."
        )

        json_data = json.dumps(
            results,
            indent=4,
            default=str
        )

        csv_data = ranking_df.to_csv(
            index=False
        ).encode("utf-8")

        download_col1, download_col2 = st.columns(2)

        download_col1.download_button(
            label="Download JSON Report",
            data=json_data,
            file_name="candidate_report.json",
            mime="application/json",
            width="stretch"
        )

        download_col2.download_button(
            label="Download CSV Rankings",
            data=csv_data,
            file_name="candidate_rankings.csv",
            mime="text/csv",
            width="stretch"
        )


    else:

        st.warning(
            "No candidates were successfully processed."
        )


    # ---------- Processing Errors ----------
    errors = results.get("processing_errors", [])

    if errors:

        with st.expander("View Processing Errors"):

            st.json(errors)

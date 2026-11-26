def analyze_candidate(
    jd_data: dict,
    resume_data: dict,
    scoring_result: dict
) -> dict:
    """Create a structured and explainable candidate report."""

    candidate_info = resume_data.get("candidate_info", {})
    raw_experience = resume_data.get("experience", {})

    skill_analysis = scoring_result.get("skill_analysis", {})
    qualification_analysis = scoring_result.get(
        "qualification_analysis"
    )

    component_scores = scoring_result.get("component_scores", {})

    reasons = []

    candidate_name = (
        candidate_info.get("name") or "Unknown Candidate"
    )

    email = candidate_info.get("email")
    phone = candidate_info.get("phone")

    # Skill analysis
    matched_required = skill_analysis.get(
        "matched_required", []
    )

    missing_required = skill_analysis.get(
        "missing_required", []
    )

    matched_preferred = skill_analysis.get(
        "matched_preferred", []
    )

    missing_preferred = skill_analysis.get(
        "missing_preferred", []
    )

    required_skill_count = (
        len(matched_required) + len(missing_required)
    )

    if required_skill_count == 0:
        skill_status = (
            "No required skills were identified in the JD."
        )

    elif not missing_required:
        skill_status = (
            "All required skills were matched."
        )

    else:
        skill_status = (
            f"Matched {len(matched_required)} of "
            f"{required_skill_count} required skills."
        )

    reasons.append(skill_status)

    if matched_preferred:
        reasons.append(
            f"Matched {len(matched_preferred)} preferred skill(s)."
        )

    if missing_preferred:
        reasons.append(
            f"Missing {len(missing_preferred)} preferred skill(s)."
        )

    skills_report = {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "status": skill_status,
    }

    # Experience analysis
    candidate_years = raw_experience.get(
        "total_experience_years"
    )

    candidate_months = raw_experience.get(
        "total_experience_months"
    )

    required_years = jd_data.get(
        "minimum_experience_years"
    )

    if required_years is None:
        experience_status = (
            "No minimum experience requirement specified."
        )

    elif candidate_years is None:
        experience_status = (
            "Experience could not be determined from the resume."
        )

    elif candidate_years >= required_years:
        experience_status = (
            "Meets the minimum experience requirement."
        )

    else:
        experience_status = (
            "Below the minimum experience requirement."
        )

    experience_report = {
        "total_experience_years": candidate_years,
        "total_experience_months": candidate_months,
        "required_experience_years": required_years,
        "extraction_method": raw_experience.get(
            "extraction_method"
        ),
        "status": experience_status,
    }

    reasons.append(experience_status)

    # Qualification analysis
    if qualification_analysis is None:

        qualification_report = {
            "matched": [],
            "matched_preferred": [],
            "score": None,
            "detected_qualifications": [],
            "candidate_fields": [],
            "match_reason": None,
            "status": "No required qualification specified.",
        }

    else:

        matched_qualifications = qualification_analysis.get(
            "matched", []
        )

        matched_preferred_qualifications = (
            qualification_analysis.get("matched_preferred", [])
        )

        detected_qualifications = qualification_analysis.get(
            "detected",
            qualification_analysis.get(
                "detected_qualifications", []
            )
        )

        qualification_reason = qualification_analysis.get(
            "match_reason"
        )

        if not qualification_reason:

            if matched_qualifications:
                qualification_reason = (
                    "Required educational qualification matched."
                )
            else:
                qualification_reason = (
                    "Required educational qualification not matched."
                )

        qualification_status = qualification_analysis.get(
            "status"
        )

        if not qualification_status:

            if matched_qualifications:
                qualification_status = (
                    "Required qualification matched."
                )
            else:
                qualification_status = (
                    "Required qualification not matched."
                )

        qualification_report = {
            "matched": matched_qualifications,
            "matched_preferred": matched_preferred_qualifications,
            "score": qualification_analysis.get("score"),
            "detected_qualifications": detected_qualifications,
            "candidate_fields": qualification_analysis.get(
                "candidate_fields", []
            ),
            "match_reason": qualification_reason,
            "status": qualification_status,
        }

        reasons.append(qualification_reason)

        if matched_preferred_qualifications:
            reasons.append(
                "Matched preferred educational qualification(s)."
            )

    # Semantic similarity
    semantic_score = component_scores.get("semantic")

    if semantic_score is not None:
        reasons.append(
            f"Semantic similarity score: {semantic_score}%."
        )

    # Final candidate report
    return {
        "candidate_name": candidate_name,
        "email": email,
        "phone": phone,
        "final_score": scoring_result.get("final_score", 0),
        "component_scores": component_scores,
        "skills": skills_report,
        "experience": experience_report,
        "qualifications": qualification_report,
        "reasons": reasons,
    }

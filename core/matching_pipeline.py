
from core.jd_parser import parse_job_description
from core.resume_processor import process_resume
from core.semantic_matcher import calculate_semantic_similarity
from core.scoring_engine import calculate_final_score
from core.candidate_analyzer import analyze_candidate
from core.ranking_engine import rank_candidates


def run_matching_pipeline(jd_text: str, resume_files: list) -> dict:

    if not isinstance(jd_text, str) or not jd_text.strip():
        raise ValueError("Job description cannot be empty.")

    if not resume_files:
        raise ValueError("Please provide at least one resume.")

    # 1. Parse the Job Description
    jd_data = parse_job_description(jd_text)
    print("ACTUAL JD QUALIFICATIONS:", jd_data["qualifications"])
    print("ACTUAL PREFERRED QUALIFICATIONS:", jd_data["preferred_qualifications"])
    print("Required qualifications:", jd_data.get("qualifications"))
    print("Preferred qualifications:", jd_data.get("preferred_qualifications"))

    candidate_results = []
    processing_errors = []

    # 2. Process each resume
    for filename, file_bytes in resume_files:

        try:
            resume_data = process_resume(
                filename,
                file_bytes
            )

            # 3. Calculate semantic similarity
            semantic_result = calculate_semantic_similarity(
                jd_data["job_description"],
                resume_data["resume_text"]
            )

            # 4. Calculate final score
            scoring_result = calculate_final_score(
                jd_data,
                resume_data,
                semantic_result
            )

            # 5. Generate candidate analysis
            candidate_analysis = analyze_candidate(
                jd_data,
                resume_data,
                scoring_result
            )

            candidate_analysis["filename"] = filename

            candidate_results.append(candidate_analysis)

        except Exception as error:
            processing_errors.append({
                "filename": filename,
                "error": str(error)
            })

    # 6. Rank successfully processed candidates
    ranked_candidates = rank_candidates(
        candidate_results
    )

    # 7. Return complete results
    return {
        "job_description": jd_data,
        "total_resumes": len(resume_files),
        "successfully_processed": len(ranked_candidates),
        "failed_resumes": len(processing_errors),
        "ranked_candidates": ranked_candidates,
        "processing_errors": processing_errors
    }

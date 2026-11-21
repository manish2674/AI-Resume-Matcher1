
import csv
import json
from pathlib import Path
from datetime import datetime


def create_report_directory(output_dir="reports"):
    report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir


def export_json_report(results, output_dir="reports"):
    report_dir = create_report_directory(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = report_dir / f"candidate_report_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False, default=str)

    return file_path


def export_csv_report(results, output_dir="reports"):
    report_dir = create_report_directory(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = report_dir / f"candidate_rankings_{timestamp}.csv"

    candidates = results.get("ranked_candidates", [])

    fieldnames = [
        "rank",
        "candidate_name",
        "email",
        "phone",
        "final_score",
        "matched_required_skills",
        "missing_required_skills",
        "matched_preferred_skills",
        "missing_preferred_skills",
        "candidate_experience_years",
        "required_experience_years",
        "experience_status",
        "matched_qualifications",
        "qualification_score",
        "qualification_status",
        "reasons"
    ]

    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for candidate in candidates:
            skills = candidate.get("skills", {})
            experience = candidate.get("experience", {})
            qualifications = candidate.get("qualifications", {})

            row = {
                "rank": candidate.get("rank"),
                "candidate_name": candidate.get("candidate_name"),
                "email": candidate.get("email"),
                "phone": candidate.get("phone"),
                "final_score": candidate.get("final_score"),

                "matched_required_skills": ", ".join(
                    skills.get("matched_required", [])
                ),
                "missing_required_skills": ", ".join(
                    skills.get("missing_required", [])
                ),
                "matched_preferred_skills": ", ".join(
                    skills.get("matched_preferred", [])
                ),
                "missing_preferred_skills": ", ".join(
                    skills.get("missing_preferred", [])
                ),

                "candidate_experience_years": experience.get(
                    "candidate_years"
                ),
                "required_experience_years": experience.get(
                    "required_years"
                ),
                "experience_status": experience.get("status"),

                "matched_qualifications": ", ".join(
                    qualifications.get("matched", [])
                ),
                "qualification_score": qualifications.get("score"),
                "qualification_status": qualifications.get("status"),

                "reasons": " | ".join(
                    candidate.get("reasons", [])
                )
            }

            writer.writerow(row)

    return file_path

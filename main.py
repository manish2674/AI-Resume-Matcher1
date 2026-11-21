
from pathlib import Path
import json

from core.matching_pipeline import run_matching_pipeline


def get_job_description():
    print("\nEnter the Job Description.")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines).strip()


def load_resumes(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise ValueError("The provided path is not a folder.")

    resume_files = []

    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in [".pdf", ".docx"]:
            resume_files.append(
                (file_path.name, file_path.read_bytes())
            )

    return resume_files


def display_rankings(candidates):
    print("\nCANDIDATE RANKINGS")
    print("-" * 75)

    print(
        f"{'Rank':<8}"
        f"{'Candidate':<30}"
        f"{'Match Score':<15}"
    )

    print("-" * 75)

    for candidate in candidates:
        name = candidate.get(
            "candidate_name",
            candidate.get("name", "Unknown")
        )

        score = candidate.get("final_score", 0)
        rank = candidate.get("rank", "-")

        print(
            f"{rank:<8}"
            f"{name:<30}"
            f"{score}%"
        )

    print("-" * 75)


def display_candidate_details(candidates):
    while True:
        choice = input(
            "\nEnter candidate rank to view details, "
            "or type 0 to exit: "
        ).strip()

        if choice == "0":
            break

        if not choice.isdigit():
            print("Please enter a valid rank.")
            continue

        selected_rank = int(choice)

        candidate = next(
            (
                item for item in candidates
                if item.get("rank") == selected_rank
            ),
            None
        )

        if candidate is None:
            print("Candidate rank not found.")
            continue

        print("\nCANDIDATE ANALYSIS")
        print("-" * 75)
        print(json.dumps(candidate, indent=4, default=str))
        print("-" * 75)


def main():
    print("=" * 75)
    print("AI-BASED RESUME MATCHING AND CANDIDATE RANKING SYSTEM")
    print("=" * 75)

    try:
        jd_text = get_job_description()

        if not jd_text:
            print("Error: Job Description cannot be empty.")
            return

        folder_path = input(
            "\nEnter resume folder path "
            "[default: sample_data/synthetic_resumes]: "
        ).strip()

        if not folder_path:
            folder_path = "sample_data/synthetic_resumes"

        resume_files = load_resumes(folder_path)

        if not resume_files:
            print("No PDF or DOCX resumes found in the folder.")
            return

        print(f"\nLoaded {len(resume_files)} resumes.")
        print("Starting resume matching. Please wait...\n")

        results = run_matching_pipeline(jd_text, resume_files)

        print("\nPROCESSING SUMMARY")
        print("-" * 40)
        print("Total resumes:", results["total_resumes"])
        print("Successfully processed:", results["successfully_processed"])
        print("Failed resumes:", results["failed_resumes"])

        if results["ranked_candidates"]:
            display_rankings(results["ranked_candidates"])
            display_candidate_details(results["ranked_candidates"])
        else:
            print("\nNo candidates could be ranked.")

        if results["processing_errors"]:
            print("\nPROCESSING ERRORS")

            for error in results["processing_errors"]:
                print(error["filename"], ":", error["error"])

    except (ValueError, FileNotFoundError) as error:
        print(f"\nError: {error}")

    except KeyboardInterrupt:
        print("\nApplication stopped by user.")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    main()

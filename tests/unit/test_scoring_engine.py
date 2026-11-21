
from core.scoring_engine import calculate_final_score


# Sample Job Description result
jd_data = {
    "required_skills": {
        "programming_languages": ["Python"],
        "data_science": ["Pandas", "NumPy", "Scikit-learn"],
        "databases": ["SQL"],
    },

    "preferred_skills": {
        "data_science": ["TensorFlow", "PyTorch"],
        "tools": ["Docker", "AWS"],
    },

    "minimum_experience_years": 2.0,

    "qualifications": ["B.Tech"],
}


# Sample Resume result
resume_data = {
    "skills": {
        "programming_languages": ["Python"],
        "data_science": ["Pandas", "NumPy", "Scikit-learn"],
        "databases": ["SQL"],
        "tools": ["Docker"],
    },

    "experience": {
        "total_experience_years": 2.0,
    },

    "resume_text": """
    Rahul Sharma
    B.Tech in Computer Science
    Python developer with experience in Pandas,
    NumPy, Scikit-learn and SQL.
    """
}


# Sample semantic similarity result
semantic_result = {
    "semantic_similarity": 75.41
}


# Calculate final score
result = calculate_final_score(
    jd_data,
    resume_data,
    semantic_result
)


print("\n========== FINAL MATCH SCORE ==========")
print(result["final_score"], "%")

print("\n========== COMPONENT SCORES ==========")

for component, score in result["component_scores"].items():
    print(f"{component}: {score}")

print("\n========== SKILL ANALYSIS ==========")

print(
    "Matched Required:",
    result["skill_analysis"]["matched_required"]
)

print(
    "Missing Required:",
    result["skill_analysis"]["missing_required"]
)

print(
    "Matched Preferred:",
    result["skill_analysis"]["matched_preferred"]
)

print(
    "Missing Preferred:",
    result["skill_analysis"]["missing_preferred"]
)

print("\n QUALIFICATION ANALYSIS ")
print(result["qualification_analysis"])

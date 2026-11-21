
from core.candidate_analyzer import analyze_candidate


jd_data = {
    "minimum_experience_years": 2.0
}


resume_data = {
    "candidate_info": {
        "name": "Rahul Sharma",
        "email": "rahul@example.com"
    },

    "experience": {
        "total_experience_years": 2.0
    }
}


scoring_result = {
    "final_score": 86.62,

    "component_scores": {
        "skills": 85.0,
        "semantic": 75.41,
        "experience": 100.0,
        "qualification": 100.0
    },

    "skill_analysis": {
        "matched_required": [
            "Python",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL"
        ],

        "missing_required": [],

        "matched_preferred": ["Docker"],

        "missing_preferred": [
            "TensorFlow",
            "PyTorch",
            "AWS"
        ]
    },

    "qualification_analysis": {
        "score": 100,
        "matched": ["B.Tech"],
        "detected": ["B.Tech"]
    }
}


result = analyze_candidate(
    jd_data,
    resume_data,
    scoring_result
)


print("\n========== CANDIDATE ANALYSIS ==========")

print("Name:", result["candidate_name"])
print("Email:", result["email"])
print("Final Score:", result["final_score"], "%")

print("\n========== COMPONENT SCORES ==========")

for component, score in result["component_scores"].items():
    print(component, ":", score)

print("\n========== SKILL ANALYSIS ==========")

for category, skills in result["skills"].items():
    print(category, ":", skills)

print("\n========== EXPERIENCE ANALYSIS ==========")
print(result["experience"])

print("\n========== QUALIFICATION ANALYSIS ==========")
print(result["qualifications"])

print("\n========== REASONS ==========")

for reason in result["reasons"]:
    print("-", reason)

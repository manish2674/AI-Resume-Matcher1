
from core.skill_extractor import extract_skills

sample_resume = """
Experienced Python developer.

Worked with Pandas, NumPy, and Scikit-learn.

Built Machine Learning models using Random Forest.

Experience with PostgreSQL, Flask, Git, and Docker.
"""

skills = extract_skills(sample_resume)

print("EXTRACTED SKILLS")
print("=" * 40)

for category, skill_list in skills.items():
    print(f"\n{category}:")
    for skill in skill_list:
        print("-", skill)

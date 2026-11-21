
from core.skill_extractor import extract_skills

sample_text = """
I have experience in ML and NLP.

I have also worked with sklearn,
JS, NodeJS and Natural Language Processing.
"""

skills = extract_skills(sample_text)

for category, skill_list in skills.items():

    print(f"\n{category}:")

    for skill in skill_list:
        print("-", skill)


from core.semantic_matcher import calculate_semantic_similarity


jd_text = """
We are looking for a Machine Learning Engineer
with Python, Machine Learning, NLP, Pandas,
Scikit-learn and experience building predictive models.
"""


resume_1 = """
Python developer with experience in Machine Learning,
Natural Language Processing, Pandas and Scikit-learn.
Built predictive models using Python.
"""


resume_2 = """
Frontend developer with experience in HTML, CSS,
JavaScript, React and Node.js.
Built responsive websites and web applications.
"""


score_1 = calculate_semantic_similarity(
    jd_text,
    resume_1
)

score_2 = calculate_semantic_similarity(
    jd_text,
    resume_2
)


print("========== SEMANTIC MATCHING ==========")

print("Resume 1:", score_1["semantic_similarity"], "%")
print("Resume 2:", score_2["semantic_similarity"], "%")

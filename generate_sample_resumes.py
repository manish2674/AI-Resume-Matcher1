
from pathlib import Path
from docx import Document


OUTPUT_FOLDER = Path("sample_data/synthetic_resumes")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


candidates = [
    {
        "name": "Aarav Mehta",
        "email": "aarav@example.com",
        "title": "Machine Learning Engineer",
        "experience": "4 years",
        "skills": "Python, Machine Learning, Deep Learning, Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, SQL, Docker, AWS",
        "education": "B.Tech in Computer Science",
        "summary": "Experienced Machine Learning Engineer building predictive models, classification systems and deep learning applications.",
    },
    {
        "name": "Ananya Sharma",
        "email": "ananya@example.com",
        "title": "Python Developer",
        "experience": "3 years",
        "skills": "Python, Pandas, NumPy, SQL, Flask, Django, Git, PostgreSQL",
        "education": "B.Tech in Information Technology",
        "summary": "Python developer experienced in backend development, data processing and database integration.",
    },
    {
        "name": "Rohan Patel",
        "email": "rohan@example.com",
        "title": "Data Analyst",
        "experience": "2 years",
        "skills": "Python, SQL, Pandas, NumPy, Power BI, Tableau, Excel, Matplotlib",
        "education": "B.Sc in Statistics",
        "summary": "Data Analyst experienced in data cleaning, reporting, visualization and business intelligence.",
    },
    {
        "name": "Ishita Verma",
        "email": "ishita@example.com",
        "title": "Deep Learning Engineer",
        "experience": "5 years",
        "skills": "Python, Deep Learning, TensorFlow, PyTorch, Keras, Computer Vision, NLP, NumPy, Scikit-learn",
        "education": "M.Tech in Artificial Intelligence",
        "summary": "Deep Learning Engineer developing neural networks, computer vision and NLP applications.",
    },
    {
        "name": "Kabir Shah",
        "email": "kabir@example.com",
        "title": "NLP Engineer",
        "experience": "3 years",
        "skills": "Python, NLP, Natural Language Processing, Machine Learning, Transformers, SQL, PyTorch, Scikit-learn",
        "education": "B.Tech in Computer Science",
        "summary": "NLP Engineer working on text classification, language processing and semantic search applications.",
    },
    {
        "name": "Diya Joshi",
        "email": "diya@example.com",
        "title": "Junior ML Developer",
        "experience": "6 months",
        "skills": "Python, Machine Learning, Pandas, NumPy, Scikit-learn, Matplotlib",
        "education": "B.Tech in Computer Engineering",
        "summary": "Junior developer with internship experience in data preprocessing and basic machine learning models.",
    },
    {
        "name": "Vivaan Desai",
        "email": "vivaan@example.com",
        "title": "Backend Developer",
        "experience": "4 years",
        "skills": "Python, FastAPI, Flask, Django, SQL, PostgreSQL, MongoDB, Docker, Git, AWS",
        "education": "B.E. in Computer Engineering",
        "summary": "Backend developer building REST APIs, scalable services and database-driven applications.",
    },
    {
        "name": "Meera Kapoor",
        "email": "meera@example.com",
        "title": "Senior Data Scientist",
        "experience": "6 years",
        "skills": "Python, Machine Learning, Deep Learning, Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, NLP, SQL, AWS, Docker",
        "education": "M.Tech in Data Science",
        "summary": "Senior Data Scientist experienced in predictive analytics, model development and production machine learning.",
    },
    {
        "name": "Aditya Rao",
        "email": "aditya@example.com",
        "title": "Business Intelligence Analyst",
        "experience": "3 years",
        "skills": "SQL, Power BI, Tableau, Excel, Python, Pandas, MySQL, PostgreSQL",
        "education": "B.Com in Finance",
        "summary": "Business Intelligence Analyst specializing in dashboards, reporting and business data analysis.",
    },
    {
        "name": "Sana Khan",
        "email": "sana@example.com",
        "title": "Software Developer",
        "experience": "2 years",
        "skills": "JavaScript, React, Node.js, HTML, CSS, MongoDB, Git, SQL",
        "education": "BCA",
        "summary": "Software developer experienced in frontend development and full-stack web applications.",
    },
]


for index, candidate in enumerate(candidates, start=1):

    document = Document()

    document.add_heading(candidate["name"], level=0)

    document.add_paragraph(candidate["email"])

    document.add_heading("Professional Summary", level=1)
    document.add_paragraph(candidate["summary"])

    document.add_heading("Work Experience", level=1)
    document.add_paragraph(candidate["title"])
    document.add_paragraph(
        f"Total Experience: {candidate['experience']}"
    )

    document.add_heading("Technical Skills", level=1)
    document.add_paragraph(candidate["skills"])

    document.add_heading("Education", level=1)
    document.add_paragraph(candidate["education"])

    filename = f"candidate_{index:02d}.docx"

    document.save(OUTPUT_FOLDER / filename)

    print(f"Created: {filename}")


print(f"\nSuccessfully generated {len(candidates)} synthetic resumes.")
print(f"Location: {OUTPUT_FOLDER}")

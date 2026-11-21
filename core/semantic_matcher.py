
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the pretrained model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(
    jd_text: str,
    resume_text: str
) -> dict:

    if not isinstance(jd_text, str) or not isinstance(resume_text, str):
        raise TypeError("Both inputs must be strings.")

    if not jd_text.strip() or not resume_text.strip():
        raise ValueError("JD and resume text cannot be empty.")

    # 1. Convert both texts into embeddings
    embeddings = model.encode([
        jd_text,
        resume_text
    ])

    # 2. Calculate cosine similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # 3. Convert similarity into a percentage
    score = round(float(similarity) * 100, 2)

    return {
        "semantic_similarity": score
    }

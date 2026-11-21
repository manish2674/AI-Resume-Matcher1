# AI-Based Resume Matching & Candidate Ranking System

An AI-powered resume screening application that compares multiple candidate resumes against a Job Description (JD), calculates matching scores, and ranks candidates based on their suitability.

The application supports PDF and DOCX resumes, semantic similarity, skill matching, experience evaluation, qualification analysis, and candidate-level explanations.

## Project Overview

Recruiters often need to review multiple resumes for a single job opening. Manually comparing every resume against the job requirements can be time-consuming.

This project automates the initial screening process by:

- Accepting a Job Description as input.
- Processing multiple PDF and DOCX resumes in one batch.
- Extracting candidate information, skills, education, and experience.
- Comparing resumes against the Job Description.
- Calculating an overall matching score from 0 to 100.
- Ranking candidates based on their matching scores.
- Providing candidate-level analysis and explanations.
- Exporting candidate reports in JSON and CSV formats.

## Features

### 1. Job Description Analysis
- Paste a complete Job Description.
- Extract required and preferred skills.
- Identify minimum experience requirements.
- Extract required and preferred qualifications.

### 2. Resume Processing
- Upload multiple resumes in one batch.
- Support for PDF and DOCX formats.
- Extract resume text.
- Identify candidate name, email, and phone number.
- Extract technical skills.
- Estimate professional experience.
- Identify educational qualifications.

### 3. AI-Based Resume Matching
- Required and preferred skill matching.
- Semantic similarity using Sentence Transformers.
- Experience requirement evaluation.
- Educational qualification matching.
- Weighted matching score calculation.

### 4. Candidate Ranking Dashboard
- Display total uploaded resumes.
- Show successfully processed and failed resumes.
- Rank candidates by matching score.
- Display candidate experience and matched skills.

### 5. Individual Candidate Analysis
- Candidate information.
- Overall matching score.
- Matched and missing skills.
- Experience comparison.
- Qualification analysis.
- Component-wise score breakdown.
- Explanations behind the matching result.

### 6. Report Export
- Export candidate analysis as JSON.
- Export candidate rankings as CSV.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | Web application interface |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| spaCy | Skill extraction |
| Sentence Transformers | Semantic similarity |
| Scikit-learn | Cosine similarity calculation |
| PyTorch | Deep learning model backend |
| Pandas | Data handling and reporting |

## Project Architecture

```text
AI-Resume-Matcher-V2/
│
├── core/
│   ├── __init__.py
│   ├── parser.py
│   ├── text_cleaner.py
│   ├── skill_extractor.py
│   ├── experience_extractor.py
│   ├── candidate_info.py
│   ├── jd_parser.py
│   ├── semantic_matcher.py
│   ├── scoring_engine.py
│   ├── ranking_engine.py
│   ├── candidate_analyzer.py
│   ├── resume_processor.py
│   ├── matching_pipeline.py
│   └── report_exporter.py
│
├── utils/
│   ├── __init__.py
│   └── skill_dictionary.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   └── integration/
│
├── sample_data/
│   └── synthetic_resumes/
│
├── reports/
│
├── app.py
├── main.py
├── generate_sample_resumes.py
├── requirements.txt
├── requirements-lock.txt
├── README.md
└── .gitignore
```

## Resume Matching Workflow

1. The recruiter provides a Job Description.
2. The JD parser extracts skills, experience requirements, and qualifications.
3. Uploaded resumes are parsed from PDF or DOCX.
4. Extracted text is cleaned and normalized.
5. Candidate information, skills, and experience are identified.
6. Sentence Transformers generate semantic embeddings.
7. The scoring engine evaluates the available matching components.
8. Candidates are ranked by their final scores.
9. The dashboard displays individual candidate analysis.
10. Reports can be exported in JSON and CSV formats.

## Matching and Scoring Methodology

The system combines four matching components using weighted scoring.

| Component | Weight |
|---|---:|
| Skill Matching | 40% |
| Semantic Similarity | 30% |
| Experience Matching | 20% |
| Qualification Matching | 10% |
| **Total** | **100%** |

### Skill Matching
Required and preferred skills are evaluated separately.

- Required skills contribute 80% of the skill component.
- Preferred skills contribute 20% of the skill component.
- Matched and missing skills are displayed separately.

### Semantic Similarity
The `all-MiniLM-L6-v2` Sentence Transformer model generates embeddings for the Job Description and resume text.

Cosine similarity is used to calculate semantic similarity between the two text representations.

### Experience Matching
Candidate experience is compared with the minimum experience requirement.

The score is capped at 100 when the candidate meets or exceeds the required experience.

### Qualification Matching
The system evaluates recognized educational qualifications and relevant technical fields.

Equivalent or higher degrees in related technical fields may satisfy the required qualification level, depending on the JD requirements.

### Missing Information
When experience or qualification information cannot be determined, the corresponding component is treated as unavailable rather than automatically assigning a score of zero.

The final score is calculated using the weights of the available components.

**Note:** The final matching percentage is an algorithmic ranking indicator, not a guarantee of candidate suitability or a hiring decision.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Resume-Matcher-V2
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

Windows PowerShell:

```powershell
& .\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

For reproducing the pinned environment:

```bash
pip install -r requirements-lock.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, normally:

```text
http://localhost:8501
```

## Running Tests

Run unit and integration tests from the project root.

Example:

```bash
python -m tests.unit.test_scoring_engine
```

```bash
python -m tests.unit.test_qualification_matching
```

```bash
python -m tests.integration.test_edge_cases
```

```bash
python -m tests.integration.test_synthetic_batch
```

The integration tests cover batch processing, missing information, invalid PDF handling, and PDF/DOCX processing.

## Sample Data

The project includes synthetic resumes for demonstration and testing.

Use synthetic or publicly licensed resume data only. Do not upload real candidate personal information or confidential documents to the public repository.

## Limitations

- Scanned PDFs without extractable text are not processed through OCR.
- Skill extraction depends on the configured skill dictionary and matching logic.
- Resume layouts and formatting can affect extraction accuracy.
- Semantic similarity is not a calibrated probability of job suitability.
- Matching scores should support human review, not replace recruiter judgment.

## Future Improvements

- Improve resume parsing for more document layouts.
- Expand skill aliases and qualification recognition.
- Add OCR support for scanned resumes.
- Improve matching evaluation using labeled datasets.
- Add more detailed reporting and visualization.
- Improve handling of overlapping employment periods and experience relevance.

## Testing and Validation

The project has been tested with:

- Multiple synthetic resumes in a single batch.
- PDF and DOCX resume processing.
- Missing education and experience information.
- Missing contact information.
- Unrelated educational qualifications.
- Empty and corrupted PDF files.
- Candidate ranking and score calculation.

These tests validate the implemented scenarios; they do not establish production-level hiring accuracy.

## Project Purpose

This project was developed as a practical AI/NLP application to demonstrate resume parsing, semantic matching, scoring, ranking, and explainable candidate analysis.

---

**Built with Python, NLP, Machine Learning, and Streamlit.**
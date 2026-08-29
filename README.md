# ResumeLens AI

### AI-Powered Resume Intelligence & Career Fit Analysis

ResumeLens AI is a full-stack machine learning application that analyzes a candidate's resume against a target job description, evaluates skill alignment, identifies missing skills, calculates a job-fit score, and predicts the candidate's career category using a trained machine learning model.

The project combines **machine learning, natural language processing, document processing, and a modern React interface** into one practical career intelligence platform.

---

## ✨ Features

### 📄 Resume Upload & Extraction

* Upload resumes in **PDF or DOCX** format.
* Validates file type and file size.
* Extracts readable resume content automatically.
* Displays extracted resume information before analysis.

### 🎯 Job Fit Analysis

* Compares resume content against a target job description.
* Extracts required skills from the job requirements.
* Detects skills already present in the resume.
* Identifies missing skills.
* Calculates an overall **Job Fit Score**.

### 🤖 Career Category Prediction

* Uses a trained machine learning classification model.
* Predicts the candidate's most relevant career category.
* Uses TF-IDF vectorization to transform resume text into machine-learning features.

### 📊 Resume Intelligence Report

After analysis, ResumeLens AI presents:

* Job Fit Score
* Predicted Career Category
* Total Required Skills
* Matched Skills
* Missing Skills
* Complete Job Requirement Profile

### 🛡️ Input Validation

* PDF/DOCX validation
* Maximum 5 MB upload limit
* Resume content validation
* Job description validation
* Backend response validation
* Safe frontend result normalization
* User-friendly error messages

---

## 🏗️ Architecture

```text
                    ┌─────────────────────────┐
                    │       React Frontend    │
                    │        Vite + CSS       │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP / REST API
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    │                         │
                    │  Resume Upload API      │
                    │  Analysis API            │
                    │  Job Fit Service         │
                    │  Skill Extraction        │
                    │  Document Parser         │
                    │  ML Prediction           │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌─────────────────┐       ┌─────────────────┐
          │ Resume Documents│       │ ML Model Files  │
          │ PDF / DOCX      │       │ TF-IDF + Model  │
          └─────────────────┘       └─────────────────┘
```

---

## 🧠 Machine Learning Pipeline

ResumeLens AI uses a machine learning pipeline for career-category prediction.

```text
Resume
   │
   ▼
Text Extraction
   │
   ▼
Text Cleaning / Processing
   │
   ▼
TF-IDF Vectorization
   │
   ▼
Trained ML Classifier
   │
   ▼
Predicted Career Category
```

For job-fit analysis, the system separately compares resume skills with skills extracted from the target job description.

```text
Resume ───────────────┐
                      │
                      ▼
                Skill Extraction
                      │
                      ▼
              Matched / Missing
                      │
Job Description ──────┘
                      │
                      ▼
                Fit Score
```

---

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* JavaScript
* CSS3
* Responsive UI
* Glassmorphism-inspired interface

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* REST APIs

### Machine Learning

* Scikit-learn
* TF-IDF Vectorization
* Machine Learning Classification
* Job-fit skill matching

### Document Processing

* PDF text extraction
* DOCX text extraction
* File validation

### Development Tools

* Git
* GitHub
* VS Code
* PowerShell

---

## 📁 Project Structure

```text
ResumeLens-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── analysis.py
│   │   │   ├── analyze.py
│   │   │   ├── job_fit.py
│   │   │   ├── prediction.py
│   │   │   └── upload.py
│   │   │
│   │   ├── ml/
│   │   │   ├── predictor.py
│   │   │   └── validate_model.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── analyze.py
│   │   │   ├── job_fit.py
│   │   │   └── prediction.py
│   │   │
│   │   ├── services/
│   │   │   ├── document_parser.py
│   │   │   ├── job_fit.py
│   │   │   └── skill_extractor.py
│   │   │
│   │   └── main.py
│   │
│   ├── ml/
│   │   ├── predictor.py
│   │   ├── train_model.py
│   │   └── validate_model.py
│   │
│   └── requirements.txt
│
├── data/
│   └── job_resume_fit.csv
│
├── docs/
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── models/
│   ├── resume_category_model.pkl
│   └── resume_tfidf_vectorizer.pkl
│
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/najamrizvi/ResumeLens-AI.git
cd ResumeLens-AI
```

---

## ⚙️ Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

## 💻 Frontend Setup

Open another terminal and navigate to:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

## 🔄 Application Workflow

```text
1. User opens ResumeLens AI
              │
              ▼
2. Upload PDF/DOCX resume
              │
              ▼
3. Backend extracts resume text
              │
              ▼
4. User provides target job description
              │
              ▼
5. ResumeLens extracts required skills
              │
              ▼
6. Resume skills are compared
              │
              ▼
7. Matched & missing skills identified
              │
              ▼
8. Job-fit score calculated
              │
              ▼
9. Resume passed through ML pipeline
              │
              ▼
10. Career category predicted
              │
              ▼
11. Complete intelligence report displayed
```

---

## 📊 Example Analysis

For a resume containing:

```text
Python
FastAPI
Machine Learning
TensorFlow
SQL
```

and a job requiring:

```text
Python
FastAPI
Machine Learning
TensorFlow
SQL
Docker
Scikit-learn
Data Analysis
```

ResumeLens AI can identify:

### Matched Skills

```text
✓ Python
✓ FastAPI
✓ Machine Learning
✓ TensorFlow
✓ SQL
```

### Missing Skills

```text
+ Docker
+ Scikit-learn
+ Data Analysis
```

The system then generates an overall job-fit score based on the detected skill alignment.

---

## 🔌 API Endpoints

The backend provides REST endpoints for the major application operations.

### Resume Upload

```text
POST /api/upload-resume
```

Uploads a PDF or DOCX resume and extracts its readable content.

### Resume Analysis

```text
POST /api/analyze
```

Analyzes the extracted resume against a supplied job description.

### Additional APIs

ResumeLens AI also separates functionality into dedicated API modules for:

* Analysis
* Job-fit evaluation
* Career prediction
* Resume upload

---

## 🔐 Production & Reliability Considerations

ResumeLens AI includes several defensive mechanisms:

* File extension validation
* MIME-type validation
* File size restrictions
* Resume content validation
* Job-description validation
* Backend response validation
* Required-field validation
* Numeric score normalization
* Safe array handling
* Loading-state management
* Upload-state management
* User-friendly error handling

Uploaded test documents are excluded from version control through `.gitignore`.

Python cache files such as `__pycache__` and generated `.pyc` files are also excluded from the repository.

---

## 🎯 Project Goals

ResumeLens AI was designed to demonstrate how machine learning can be integrated into a practical full-stack application.

The project focuses on:

* Applying machine learning to real-world career data
* Combining ML with REST APIs
* Processing unstructured resume documents
* Extracting useful information from text
* Building an interactive React frontend
* Designing a complete end-to-end AI workflow
* Creating a portfolio-ready AI engineering project

---

## 🔮 Future Improvements

Potential future versions could include:

* Automatic job-description collection from job platforms
* Multiple resume comparison
* Resume improvement recommendations
* ATS compatibility scoring
* Resume keyword optimization
* Semantic similarity using transformer models
* LLM-powered resume feedback
* Personalized learning recommendations
* Authentication and user accounts
* Resume history and analytics
* Cloud deployment
* Docker-based production deployment

---

## 📌 Project Status

**Version:** 1.0
**Status:** Production-ready project structure / deployment preparation

ResumeLens AI currently provides a complete workflow for resume upload, document extraction, job-fit analysis, skill comparison, and ML-powered career classification.

---

## 👨‍💻 Author

**Syed Najam Ul Hassan**

AI / Data Science Engineer

GitHub:
https://github.com/najamrizvi

---

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.

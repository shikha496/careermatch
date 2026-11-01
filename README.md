SkillGap Prep 🚀

An AI-powered career preparation platform that helps job seekers identify skill gaps, analyze resume compatibility, and prepare for interviews.

📌 Project Overview

SkillGap Prep is a career development platform designed to help students, fresh graduates, and job seekers prepare for their desired careers.

The platform allows users to upload their resumes, compare their skills against job descriptions, identify missing skills, and receive recommendations for improving their employability.

The project currently includes a React-based frontend and a Python FastAPI backend with PDF/DOCX resume extraction and rule-based skill matching.

Project Status: In Development
🎯 Objectives
Analyze resumes against job descriptions.
Identify matching and missing skills.
Calculate an estimated career compatibility score.
Recommend skills that users should improve.
Provide an interview preparation environment.
Build a centralized career preparation dashboard.
✨ Features
1. Dashboard
Centralized career preparation dashboard.
Career statistics cards.
Navigation between different tools.
Responsive interface.
2. Career Match AI
Resume upload interface.
PDF and DOCX support.
Job description input.
Resume text extraction.
Skill identification.
Matching and missing skill detection.
Estimated compatibility percentage.
Skill improvement recommendations.
3. Interview IQ — Planned
Technical interview practice.
Behavioral interview questions.
Mock interview sessions.
Answer evaluation.
Personalized feedback.
4. Skill Gap Analysis — Planned
Identify skill deficiencies.
Analyze job requirements.
Recommend learning paths.
Track skill development.
5. User Authentication — Planned
User registration.
Login and logout.
Personal user dashboard.
Saved analysis reports.
🛠️ Technology Stack
Technology	Purpose
React.js	Frontend development
Vite	Frontend development server
JavaScript	Frontend functionality
CSS3	UI styling
Lucide React	Icons
Python	Backend programming
FastAPI	REST API framework
Uvicorn	Backend server
PyPDF	PDF text extraction
python-docx	DOCX text extraction
📂 Project Structure
text
skillgap-prep/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── public/
│
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │   ├── Sidebar.jsx
│   │   ├── Header.jsx
│   │   ├── StatCard.jsx
│   │   └── ToolCard.jsx
│   │
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── CareerMatch.jsx
│   │   ├── InterviewIQ.jsx
│   │   └── SkillAnalysis.jsx
│   │
│   ├── styles/
│   │   └── App.css
│   │
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── .venv/
├── package.json
├── package-lock.json
├── vite.config.js
├── index.html
└── README.md

⚙️ Installation and Setup
Prerequisites

Install the following before starting:

Node.js
Python
Visual Studio Code
Git (optional, for version control)
Step 1: Clone the Repository

If you have uploaded the project to GitHub:

bash
git clone YOUR_REPOSITORY_URL
cd skillgap-prep


Alternatively, open your existing project folder in VS Code.

Step 2: Install Frontend Dependencies

Open the terminal in the project root directory.

bash
npm install

Step 3: Install Python Backend Dependencies

Create a virtual environment:

bash
py -m venv .venv


Activate it on Windows PowerShell:

powershell
.venv\Scripts\Activate.ps1


If PowerShell blocks activation:

powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass


Then activate again:

powershell
.venv\Scripts\Activate.ps1


Install backend dependencies:

bash
pip install -r backend/requirements.txt

▶️ Running the Project

The frontend and backend must run simultaneously.

Terminal 1: Start the Backend

From the project root directory:

bash
python -m uvicorn main:app --reload --app-dir backend --port 8000


Backend URL:

http://127.0.0.1:8000/

Interactive API documentation:

http://127.0.0.1:8000/docs

Terminal 2: Start the Frontend

Open another terminal in VS Code:

bash
npm run dev


Frontend URL:

http://localhost:5173/

🔌 Backend API Documentation
GET /

Checks whether the backend is running.

Example response:

json
{
  "message": "Welcome to SkillGap Prep API",
  "status": "running"
}

POST /analyze

Analyzes a resume against a job description.

Request type: multipart/form-data

Parameter	Type	Description
resume	File	PDF or DOCX resume
job_description	String	Target job description

Example response:

json
{
  "success": true,
  "analysis_type": "rule_based_skill_matching",
  "match_score": 75,
  "resume_skills": [
    "html",
    "css",
    "javascript",
    "react"
  ],
  "required_skills": [
    "html",
    "css",
    "javascript",
    "react",
    "python",
    "git"
  ],
  "matched_skills": [
    "html",
    "css",
    "javascript",
    "react"
  ],
  "missing_skills": [
    "python",
    "git"
  ],
  "total_required_skills": 6,
  "recommendations": [
    "Improve your python skills",
    "Improve your git skills"
  ]
}


Note: The example response is illustrative. Actual results depend on the uploaded resume and job description.

🧠 How Career Match Works

The current resume analysis process follows these steps:

User uploads a PDF or DOCX resume.
Backend validates the uploaded file.
Resume text is extracted.
User-provided job description is processed.
Supported skills are identified using predefined skill keywords 
skillgap-prep/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── public/
│
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │   ├── Sidebar.jsx
│   │   ├── Header.jsx
│   │   ├── StatCard.jsx
│   │   └── ToolCard.jsx
│   │
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── CareerMatch.jsx
│   │   ├── InterviewIQ.jsx
│   │   └── SkillAnalysis.jsx
│   │
│   ├── styles/
│   │   └── App.css
│   │
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── .venv/
├── package.json
├── package-lock.json
├── vite.config.js
├── index.html
└── README.md
skillgap-prep/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── public/
│
├── src/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── .gitignore
├── .venv/
├── README.md
├── package.json
├── package-lock.json
├── vite.config.js
└── index.htmlv

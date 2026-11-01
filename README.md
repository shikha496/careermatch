# Career Match AI

Streamlit frontend with a FastAPI backend for resume analysis and interview
practice. The existing ATS/evidence analysis remains local. Optional AI features
use Gemini for structured resume analysis and Groq for interview questions and
coaching; when a cloud provider is not configured or unavailable, requests fall
back to the configured Ollama model. If all applicable providers are unavailable,
the AI request returns a clear error rather than fabricated output.

## Setup

Use Python 3.10 or newer. From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your own `GROQ_API_KEY` and/or `GEMINI_API_KEY` to `.env`. Never commit
credentials. Alternatively, install and start Ollama, then pull the configured
local model (default `llama3.2:3b`).

## Run

Start the backend in one terminal:

```powershell
.\.venv\Scripts\python.exe run_server.py
```

Start the Streamlit frontend in a second terminal:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

The backend is available at `http://127.0.0.1:8000` and the UI at
`http://127.0.0.1:8501`. Configure `CAREER_MATCH_API_URL` if the frontend must
connect to a backend at another address.

## AI routing

| Feature | Primary | Fallback |
| --- | --- | --- |
| Resume analysis | Gemini | Ollama |
| Interview questions and coaching | Groq | Ollama |

`GET /api/health` reports which providers have credentials/configuration, not
whether a provider or local model is currently reachable. AI response endpoints
return HTTP 502 with provider details if neither the primary nor fallback works.
The resume analysis endpoint is `POST /api/ai/resume-analysis` (multipart fields
`file` and `job_description`). Existing local ATS analysis remains at
`POST /api/analyze-resume`.
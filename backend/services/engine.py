import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


def _load_project_env():
    env_file = ROOT_DIR / ".env"
    if not env_file.is_file():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip("\"'")
        if name:
            os.environ.setdefault(name, value)


_load_project_env()


class AIEngineError(RuntimeError):
    pass


def _setting(name, default):
    return os.getenv(name, default).strip()


def _timeout():
    try:
        return max(1, min(300, int(_setting("AI_TIMEOUT_SECONDS", "120"))))
    except ValueError:
        return 120


def _ollama_num_predict():
    try:
        return max(64, min(2048, int(_setting("OLLAMA_NUM_PREDICT", "512"))))
    except ValueError:
        return 512


def configuration_status():
    return {
        "groq_configured": bool(_setting("GROQ_API_KEY", "")),
        "gemini_configured": bool(_setting("GEMINI_API_KEY", "")),
        "ollama_configured": bool(_setting("OLLAMA_BASE_URL", "http://127.0.0.1:11434")),
        "models": {
            "groq": _setting("GROQ_MODEL", "llama-3.3-70b-versatile"),
            "gemini": _setting("GEMINI_MODEL", "gemini-2.5-flash"),
            "ollama": _setting("OLLAMA_MODEL", "llama3.2:3b"),
        },
    }


def _post_json(url, payload, headers=None):
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=_timeout()) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code == 404 and url.rstrip("/").endswith("/api/chat"):
            raise AIEngineError(
                "Ollama endpoint or model was not found. Check OLLAMA_BASE_URL "
                "and install the configured model with `ollama pull "
                + _setting("OLLAMA_MODEL", "llama3.2:3b")
                + "`."
            ) from error
        raise AIEngineError("AI provider returned HTTP " + str(error.code) + ".") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        reason = getattr(error, "reason", error)
        raise AIEngineError("Could not reach AI provider: " + str(reason)) from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AIEngineError("AI provider returned an invalid response.") from error


def _provider_response(provider, messages, temperature=0.3, json_response=False):
    if provider == "groq":
        key = _setting("GROQ_API_KEY", "")
        if not key:
            raise AIEngineError("GROQ_API_KEY is not configured.")
        payload = {
            "model": _setting("GROQ_MODEL", "llama-3.3-70b-versatile"),
            "messages": messages,
            "temperature": temperature,
        }
        if json_response:
            payload["response_format"] = {"type": "json_object"}
        result = _post_json(
            "https://api.groq.com/openai/v1/chat/completions",
            payload,
            {"Authorization": "Bearer " + key},
        )
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise AIEngineError("Groq returned no message content.") from error

    if provider == "gemini":
        key = _setting("GEMINI_API_KEY", "")
        if not key:
            raise AIEngineError("GEMINI_API_KEY is not configured.")
        model = _setting("GEMINI_MODEL", "gemini-2.5-flash")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + urllib.parse.quote(model, safe=":")
            + ":generateContent?"
            + urllib.parse.urlencode({"key": key})
        )
        contents = [
            {
                "role": "user" if item["role"] == "user" else "model",
                "parts": [{"text": item["content"]}],
            }
            for item in messages
            if item["role"] != "system"
        ]
        system_instruction = next(
            (item["content"] for item in messages if item["role"] == "system"),
            None,
        )
        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature},
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
        if json_response:
            payload["generationConfig"]["responseMimeType"] = "application/json"
        result = _post_json(url, payload)
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as error:
            raise AIEngineError("Gemini returned no message content.") from error

    if provider == "ollama":
        base_url = _setting("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
        payload = {
            "model": _setting("OLLAMA_MODEL", "llama3.2:3b"),
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": _ollama_num_predict(),
            },
        }
        if json_response:
            payload["format"] = "json"
        result = _post_json(base_url + "/api/chat", payload)
        try:
            return result["message"]["content"]
        except (KeyError, TypeError) as error:
            raise AIEngineError("Ollama returned no message content.") from error

    raise AIEngineError("Unsupported AI provider.")


def _run_with_fallback(messages, primary, temperature=0.3, json_response=False):
    providers = [primary] if primary == "ollama" else [primary, "ollama"]
    errors = []
    for provider in providers:
        try:
            content = _provider_response(
                provider,
                messages,
                temperature=temperature,
                json_response=json_response,
            )
            if not isinstance(content, str) or not content.strip():
                raise AIEngineError(provider + " returned empty message content.")
            return content.strip(), provider
        except AIEngineError as error:
            errors.append(provider + ": " + str(error))
    raise AIEngineError("AI request failed. " + " ".join(errors))


def chat(message, context=None, role=None):
    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")
    context = (context or "").strip()
    role = (role or "").strip()
    system_prompt = (
        "You are a concise, supportive career interview coach. Give practical, "
        "truthful advice. Do not invent candidate experience, facts, or outcomes."
    )
    if role:
        system_prompt += " Tailor the response to the " + role + " role."
    messages = [{"role": "system", "content": system_prompt}]
    if context:
        messages.append({"role": "user", "content": "Context:\n" + context})
    messages.append({"role": "user", "content": message.strip()})
    answer, provider = _run_with_fallback(messages, "groq", temperature=0.5)
    return {"answer": answer, "provider": provider}


def generate_questions(role, category, difficulty):
    prompt = (
        "Write exactly five distinct interview questions. Return only a numbered "
        "list, with no introduction or answers.\n"
        "Role: " + role.strip() + "\n"
        "Category: " + category.strip() + "\n"
        "Difficulty: " + difficulty.strip()
    )
    return chat(prompt, role=role)


def _parse_analysis(content):
    candidate = content.strip()
    candidate = re.sub(r"^```(?:json)?\s*", "", candidate, flags=re.IGNORECASE)
    candidate = re.sub(r"\s*```$", "", candidate)
    try:
        result = json.loads(candidate)
    except json.JSONDecodeError as error:
        raise AIEngineError("AI response was not valid structured JSON.") from error
    required = ("overall_assessment", "strengths", "gaps", "recommendations", "evidence")
    if not isinstance(result, dict):
        raise AIEngineError("AI response did not match the required analysis format.")
    for field in required:
        value = result.get(field)
        valid = isinstance(value, str) if field == "overall_assessment" else isinstance(value, list)
        if not valid:
            raise AIEngineError("AI response is missing valid `" + field + "` data.")
    if not all(isinstance(item, str) for item in result["strengths"] + result["gaps"] + result["recommendations"]):
        raise AIEngineError("AI response contained invalid analysis items.")
    if not all(
        isinstance(item, dict)
        and isinstance(item.get("quote"), str)
        and isinstance(item.get("relevance"), str)
        for item in result["evidence"]
    ):
        raise AIEngineError("AI evidence must include a quoted resume excerpt and relevance.")
    return result


def analyze_resume(resume_text, job_description):
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")
    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")
    messages = [
        {
            "role": "system",
            "content": (
                "You are a careful resume analyst. Compare only information present "
                "in the supplied resume and job description. Never invent credentials, "
                "skills, experience, or outcomes. Any evidence quote must be copied "
                "verbatim from the resume. If evidence is insufficient, say so. "
                "Return one JSON object with: overall_assessment (string), strengths "
                "(array of strings), gaps (array of strings), recommendations "
                "(array of strings), and evidence (array of objects with quote and "
                "relevance strings)."
            ),
        },
        {
            "role": "user",
            "content": (
                "Analyze this resume against this job description.\n\n"
                "RESUME:\n" + resume_text.strip()
                + "\n\nJOB DESCRIPTION:\n" + job_description.strip()
            ),
        },
    ]

    errors = []
    for provider in ("gemini", "ollama"):
        try:
            content = _provider_response(
                provider,
                messages,
                temperature=0.2,
                json_response=True,
            )
            analysis = _parse_analysis(content)
            return {"status": "success", "provider": provider, "analysis": analysis}
        except AIEngineError as error:
            errors.append(provider + ": " + str(error))
    raise AIEngineError("Resume analysis failed. " + " ".join(errors))

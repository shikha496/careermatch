import json
import os
from pathlib import Path
import urllib.error
import urllib.request
import uuid


def _base_url():
    configured = os.getenv("CAREER_MATCH_API_URL")
    if not configured:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                name, separator, value = line.partition("=")
                if separator and name.strip() == "CAREER_MATCH_API_URL":
                    configured = value.strip().strip("\"'")
                    break
    return (configured or "http://127.0.0.1:8000").rstrip("/")


def _decode_response(response):
    try:
        return json.loads(response.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("The backend returned an invalid response.") from error


def _open(request, timeout):
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return _decode_response(response)
    except urllib.error.HTTPError as error:
        try:
            body = json.loads(error.read().decode("utf-8"))
            detail = body.get("detail", "Backend request failed.")
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = "Backend request failed with HTTP " + str(error.code) + "."
        raise RuntimeError(str(detail)) from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        reason = getattr(error, "reason", error)
        raise RuntimeError("Backend is unavailable: " + str(reason)) from error


def _post_json(path, payload):
    request = urllib.request.Request(
        _base_url() + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return _open(request, timeout=150)


def analyze_resume(file_bytes, filename, job_description):
    boundary = "----CareerMatch" + uuid.uuid4().hex
    fields = {
        "job_description": job_description,
    }
    parts = []
    for name, value in fields.items():
        parts.extend(
            [
                ("--" + boundary + "\r\n").encode("ascii"),
                (
                    'Content-Disposition: form-data; name="'
                    + name
                    + '"\r\n\r\n'
                    + value
                    + "\r\n"
                ).encode("utf-8"),
            ]
        )
    safe_filename = (
        (filename or "resume.txt")
        .replace('"', "")
        .replace("\r", "")
        .replace("\n", "")
    )
    parts.extend(
        [
            ("--" + boundary + "\r\n").encode("ascii"),
            (
                'Content-Disposition: form-data; name="file"; filename="'
                + safe_filename
                + '"\r\n'
            ).encode("utf-8"),
            b"Content-Type: application/octet-stream\r\n\r\n",
            file_bytes,
            b"\r\n",
            ("--" + boundary + "--\r\n").encode("ascii"),
        ]
    )
    request = urllib.request.Request(
        _base_url() + "/api/ai/resume-analysis",
        data=b"".join(parts),
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary},
        method="POST",
    )
    return _open(request, timeout=180)


def generate_questions(role, category, difficulty):
    return _post_json(
        "/api/generate-question",
        {"role": role, "category": category, "difficulty": difficulty},
    )


def interview_chat(message, role=None, context=None):
    return _post_json(
        "/api/ai/chat",
        {"message": message, "role": role, "context": context},
    )

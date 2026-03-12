import os
import sys
import json
import requests as http

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"


def _call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        print("⚠️  GEMINI_API_KEY not set in .env file")
        return ""
    url = GEMINI_URL.format(key=GEMINI_API_KEY)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = http.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except http.exceptions.RequestException as e:
        print(f"⚠️  Gemini API request failed: {e}")
        return ""
    except (KeyError, IndexError) as e:
        print(f"⚠️  Unexpected Gemini response format: {e}")
        return ""


def analyze_paper(title: str, text: str = "") -> dict:
    content = f"Title: {title}\n\n{text.strip()}" if text.strip() else f"Title: {title}"
    prompt = f"""You are a research assistant. Analyze this research paper and return a JSON object with exactly these 3 fields:
1. "summary"  - A clear 2-3 sentence summary of the paper and its key contribution.
2. "keywords" - A comma-separated list of 5-8 specific technical keywords.
3. "concepts" - A comma-separated list of 3-5 high-level research concepts.

Return ONLY a valid JSON object. No explanation, no markdown, no code blocks.
Example: {{"summary": "This paper proposes...", "keywords": "transformer,attention,NLP", "concepts": "deep learning,NLP"}}

Paper: {content}"""

    raw = _call_gemini(prompt)
    if not raw:
        return {"summary": "", "keywords": "", "concepts": ""}

    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                raw = part
                break

    try:
        result = json.loads(raw)
        return {
            "summary":  result.get("summary",  ""),
            "keywords": result.get("keywords", ""),
            "concepts": result.get("concepts", ""),
        }
    except json.JSONDecodeError as e:
        print(f"⚠️  Could not parse Gemini JSON response: {e}\nRaw: {raw}")
        return {"summary": "", "keywords": "", "concepts": ""}


def analyze_paper_from_file(title: str, file_path: str) -> dict:
    text = ""
    try:
        if file_path and os.path.exists(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            if ext in [".txt", ".md"]:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()[:8000]
    except Exception as e:
        print(f"⚠️  Could not read file {file_path}: {e}")
    return analyze_paper(title, text)

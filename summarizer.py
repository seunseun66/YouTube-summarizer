
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def format_timestamp(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}" if h else f"{m:02}:{s:02}"

def call_gemini(prompt: str, json_mode: bool = False) -> str:
    url = f"{BASE_URL}/gemini-flash-latest:generateContent?key={API_KEY}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    if json_mode:
        body["generationConfig"] = {"response_mime_type": "application/json"}

    response = requests.post(url, json=body)
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def summarize_chunk(chunk: dict) -> dict:
    prompt = f"""Extract 2-4 key points from this transcript segment.
Respond ONLY with JSON in this format, no other text:
{{"points": ["point 1", "point 2", ...]}}

TRANSCRIPT:
{chunk['text']}"""

    result_text = call_gemini(prompt, json_mode=True)
    data = json.loads(result_text)
    return {
        "timestamp": format_timestamp(chunk["start"]),
        "seconds": chunk["start"],
        "points": data["points"]
    }

def merge_summary(chunk_summaries: list[dict], video_url: str) -> dict:
    all_points = [
        {"timestamp": c["timestamp"], "seconds": c["seconds"], "point": p}
        for c in chunk_summaries for p in c["points"]
    ]

    overview_prompt = "Write a 2-3 sentence overview of a video given these key points:\n" + \
        "\n".join(p["point"] for p in all_points)

    overview_text = call_gemini(overview_prompt)

    return {
        "video_url": video_url,
        "overview": overview_text,
        "key_points": all_points
    }

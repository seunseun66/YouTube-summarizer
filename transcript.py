
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not match:
        raise ValueError("Couldn't extract a video ID from that URL")
    return match.group(1)

def get_transcript(url: str) -> list[dict]:
    video_id = extract_video_id(url)
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id)
        return fetched.to_raw_data()
    except Exception as e:
        raise ValueError(f"No transcript available: {e}")

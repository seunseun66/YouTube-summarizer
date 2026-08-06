def chunk_transcript(transcript: list[dict], chunk_seconds: int = 600) -> list[dict]:
    chunks = []
    current_chunk = []
    chunk_start = transcript[0]["start"]

    for entry in transcript:
        if entry["start"] - chunk_start > chunk_seconds and current_chunk:
            chunks.append({
                "start": chunk_start,
                "text": " ".join(e["text"] for e in current_chunk)
            })
            current_chunk = []
            chunk_start = entry["start"]
        current_chunk.append(entry)

    if current_chunk:
        chunks.append({
            "start": chunk_start,
            "text": " ".join(e["text"] for e in current_chunk)
        })
    return chunks

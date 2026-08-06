
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transcript import get_transcript
from chunker import chunk_transcript
from summarizer import summarize_chunk, merge_summary

app = FastAPI()

class SummarizeRequest(BaseModel):
    url: str

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        transcript = get_transcript(req.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    chunks = chunk_transcript(transcript)
    chunk_summaries = [summarize_chunk(c) for c in chunks]
    result = merge_summary(chunk_summaries, req.url)
    return result

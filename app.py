"""Minimal AI chatbot backend: FastAPI + Google Gemini, streamed over SSE."""

import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field


# Load .env file
load_dotenv(override=True)

# Get Gemini API key
key = os.getenv("GEMINI_API_KEY")

print("GEMINI API KEY LOADED:", bool(key))
print("GEMINI API KEY PREFIX:", key[:7] if key else "NONE")
print("GEMINI API KEY LENGTH:", len(key) if key else 0)


MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer clearly and concisely. "
    "If you are unsure about something, say so."
)

MAX_TURNS = 20


# Gemini client
client = genai.Client(api_key=key) if key else None

app = FastAPI(title="Chatbot MVP")


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1)


def stream_completion(messages: list[Message]):
    """Yield server-sent events as tokens arrive from the model."""
    if not client:
        yield f"data: {json.dumps({'error': 'Gemini client is not initialized. Please set GEMINI_API_KEY in .env.'})}\n\n"
        yield "data: [DONE]\n\n"
        return

    # Convert conversation turns for Gemini (assistant -> model)
    contents = []
    for m in messages[-MAX_TURNS:]:
        gemini_role = "user" if m.role == "user" else "model"
        contents.append(
            types.Content(
                role=gemini_role,
                parts=[types.Part.from_text(text=m.content)],
            )
        )

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7,
    )

    try:
        response = client.models.generate_content_stream(
            model=MODEL,
            contents=contents,
            config=config,
        )

        for chunk in response:
            token = chunk.text
            if token:
                yield f"data: {json.dumps({'token': token})}\n\n"

    except APIError as exc:
        print("GEMINI API ERROR:", exc)
        yield f"data: {json.dumps({'error': str(exc)})}\n\n"

    except Exception as exc:
        print("GENERAL ERROR:", exc)
        yield f"data: {json.dumps({'error': str(exc)})}\n\n"

    yield "data: [DONE]\n\n"


@app.post("/api/chat")
def chat(req: ChatRequest):

    if not key:
        raise HTTPException(
            500,
            "GEMINI_API_KEY is not set. Add it to your .env file."
        )

    return StreamingResponse(
        stream_completion(req.messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "provider": "gemini",
        "model": MODEL,
        "api_key_configured": bool(key),
    }


# Serve frontend
app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
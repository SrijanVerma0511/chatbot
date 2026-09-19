"""Minimal AI chatbot backend: FastAPI + OpenAI, streamed over SSE."""

import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field


# Load .env file
load_dotenv(override=True)

# Get API key
key = os.getenv("OPENAI_API_KEY")

print("API KEY LOADED:", bool(key))
print("API KEY PREFIX:", key[:7] if key else "NONE")
print("API KEY LENGTH:", len(key) if key else 0)


MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer clearly and concisely. "
    "If you are unsure about something, say so."
)

MAX_TURNS = 20


# OpenAI client
client = OpenAI(api_key=key)

app = FastAPI(title="Chatbot MVP")


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1)


def stream_completion(messages: list[Message]):
    """Yield server-sent events as tokens arrive from the model."""

    payload = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    payload += [m.model_dump() for m in messages[-MAX_TURNS:]]

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=payload,
            temperature=0.7,
            stream=True,
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content

            if token:
                yield f"data: {json.dumps({'token': token})}\n\n"

    except OpenAIError as exc:
        print("OPENAI ERROR:", exc)
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
            "OPENAI_API_KEY is not set. Add it to your .env file."
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
        "model": MODEL
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
<<<<<<< HEAD
# AI_Chatbot
An AI-powered chatbot designed to provide intelligent, real-time, and conversational responses using modern AI technologies.
=======
# AI Chatbot MVP

FastAPI + OpenAI backend with a streaming vanilla JS front end.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then paste your real key into .env
python app.py
```

Open http://127.0.0.1:8000

## Files

| File | Job |
|---|---|
| `app.py` | `/api/chat` streams tokens over SSE, `/api/health` reports status, serves `static/` |
| `static/index.html` | Markup |
| `static/style.css` | Styling |
| `static/app.js` | Sends history, reads the stream, renders tokens live |

## How a turn works

1. JS posts the whole conversation array to `/api/chat`.
2. `app.py` prepends the system prompt, trims to the last 20 turns, calls OpenAI with `stream=True`.
3. Each token is pushed as `data: {"token": "..."}` and appended to the bubble as it arrives.
4. `data: [DONE]` closes the stream.

State lives in browser memory, so a refresh clears it.

## Next steps

- Persist chats in SQLite (`conversations` and `messages` tables keyed by session id).
- Rate-limit `/api/chat` by IP with `slowapi` before exposing it publicly.
- Render Markdown in replies with `marked` + `DOMPurify`.
- Add retrieval: embed your docs, search on each turn, prepend hits to the system prompt.
- For deployment, run `uvicorn app:app --host 0.0.0.0` behind nginx with `proxy_buffering off` so streaming survives.
>>>>>>> 6679173 (feat: add AI chatbot application)

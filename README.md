# AI Chatbot (Google Gemini)

An AI-powered chatbot designed to provide intelligent, real-time, and conversational responses powered by **Google Gemini** and **FastAPI**, streamed over SSE to a clean vanilla JS frontend.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then paste your Gemini API key into .env
python app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Environment Variables

In `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Files

| File | Job |
|---|---|
| `app.py` | `/api/chat` streams Gemini tokens over SSE, `/api/health` reports status, serves `static/` |
| `test_api.py` | Quick CLI verification of Gemini API connection and model response |
| `static/index.html` | Chat UI markup |
| `static/style.css` | Styling |
| `static/app.js` | Sends message history, parses token stream, renders bubbles live |

## How a turn works

1. JS posts the conversation array to `/api/chat`.
2. `app.py` formats the history for Gemini (`assistant` -> `model`), attaches system instructions, and calls `client.models.generate_content_stream()`.
3. Each token is yielded as `data: {"token": "..."}` and rendered into the message bubble in real-time.
4. `data: [DONE]` signals stream completion.

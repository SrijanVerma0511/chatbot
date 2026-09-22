# 🤖 AI Chatbot

A simple and lightweight AI chatbot built with **FastAPI, Google Gemini API, HTML, CSS, and JavaScript**.

The chatbot allows users to send messages and receive AI-generated responses through a clean web interface with real-time response streaming.

> 🔐 **Important:** This project requires a Google Gemini API key. Each user must use their own API key. Never share or commit your API key to GitHub.

---

## ✨ Features

- 💬 AI-powered conversations
- ⚡ Real-time streaming responses
- 🧠 Google Gemini API integration (`gemini-2.5-flash`)
- 🚀 FastAPI backend
- 🌐 HTML, CSS and JavaScript frontend
- 📱 Responsive chat interface
- 🔐 Secure API-key configuration using `.env`
- 🩺 Health-check endpoint (`/api/health`)
- 🛠️ Simple and clean project structure

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Google GenAI SDK (`google-genai`)
- Uvicorn
- python-dotenv

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)

### Communication
- REST API
- Server-Sent Events (SSE)

---

## 📁 Project Structure

```text
chatbot/
│
├── static/
│   ├── index.html       # Chatbot interface
│   ├── style.css        # Frontend styling
│   └── app.js           # Frontend JavaScript
│
├── app.py               # FastAPI backend with Gemini SSE streaming
├── test_api.py          # Gemini API test script
├── testapp.py           # Application testing
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignored files
├── .env.example         # Environment variable template
└── README.md            # Project documentation
```

---

## 🚀 Run It

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then paste your Gemini API key into .env
python app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## ⚙️ Environment Variables

In `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

---

## 🔄 How a Turn Works

1. **Frontend**: JS posts the conversation history array to `/api/chat`.
2. **Backend**: `app.py` formats the history for Gemini (`assistant` -> `model`), attaches system instructions, and calls `client.models.generate_content_stream()`.
3. **Streaming**: Each token chunk is yielded over Server-Sent Events as `data: {"token": "..."}` and rendered into the message bubble in real-time.
4. **Completion**: `data: [DONE]` signals stream completion and finishes the bubble.

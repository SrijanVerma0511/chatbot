# 🤖 AI Chatbot

A simple and lightweight AI chatbot built with **FastAPI, OpenAI API, HTML, CSS, and JavaScript**.

The chatbot allows users to send messages and receive AI-generated responses through a clean web interface with real-time response streaming.

> 🔐 **Important:** This project requires an OpenAI API key. Each user must use their own API key. Never share or commit your API key to GitHub.

---

## ✨ Features

- 💬 AI-powered conversations
- ⚡ Real-time streaming responses
- 🧠 OpenAI API integration
- 🚀 FastAPI backend
- 🌐 HTML, CSS and JavaScript frontend
- 📱 Responsive chat interface
- 🔐 Secure API-key configuration using `.env`
- 🩺 Health-check endpoint
- 🛠️ Simple and beginner-friendly project structure

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- OpenAI Python SDK
- Uvicorn
- python-dotenv

### Frontend
- HTML5
- CSS3
- JavaScript

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
├── app.py               # FastAPI backend
├── test_api.py          # OpenAI API test
├── testapp.py           # Application testing
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignored files
├── .env.example         # Environment variable template
└── README.md            # Project documentation

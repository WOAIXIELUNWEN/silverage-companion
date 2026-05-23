# 🌿 银龄智伴 (SilverAge Companion)

> AI-powered companion platform for the elderly — built with **Xiaomi MiMo-V2.5** large language model.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal.svg)](https://fastapi.tiangolo.com)
[![MiMo-V2.5](https://img.shields.io/badge/Powered%20by-MiMo--V2.5-orange.svg)](https://platform.xiaomimimo.com)

**SilverAge Companion** (银龄智伴) is an intelligent companion platform designed for elderly care. It leverages large language models to provide emotional companionship, health knowledge Q&A, and emergency alert detection through a **multi-agent collaborative pipeline**.

---

## ✨ Features

- **🤗 Emotional Companionship** — Warm, patient conversation with long-context memory
- **💊 Health Knowledge Q&A** — RAG-powered answers on medication, chronic disease management, wellness
- **🚨 Emergency Detection** — Keyword + LLM dual-layer detection for urgent situations, auto-escalation
- **🛡️ Safety Guard** — AI-powered content moderation ensuring responses are elderly-appropriate
- **🧠 Multi-Agent Pipeline** — Intent Classification → Knowledge Retrieval → Dialogue Generation → Safety Review
- **👴 Elderly-Friendly UI** — Large fonts, high contrast, simple interactions
- **💾 Conversation Memory** — SQLite-backed session persistence with history recall

---

## 🏗️ Architecture

```
┌─────────────┐
│  User Input  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Intent Classifier │  ← LLM Agent #1
│ chat/health/emerg │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Knowledge Retriever│  ← RAG Agent #2 (health intent only)
│ Local KB + fuzzy  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Companion Dialogue │  ← LLM Agent #3 (MiMo-V2.5)
│ Context-aware gen │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Safety Reviewer  │  ← LLM Agent #4
│ Content moderation │
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│  Response    │
└─────────────┘
```

Each message flows through **4 specialized agents**, forming a complete production-grade AI pipeline optimized for elderly care scenarios.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [MiMo API Key](https://platform.xiaomimimo.com) (from Xiaomi MiMo Orbit Program)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/silverage-companion.git
cd silverage-companion

# Set up environment
cp .env.example .env
# Edit .env — add your MIMO_API_KEY

# Install dependencies
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```

Open http://localhost:8000 in your browser.

### Docker

```bash
cp .env.example .env
# Edit .env with your API key
docker-compose up -d
```

---

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/chat` | Send a message, get AI companion reply |
| `GET` | `/api/chat/history/{session_id}` | Retrieve conversation history |
| `POST` | `/api/health/search` | Search health knowledge base |
| `GET` | `/api/health` | Health check |

### Chat Example

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "高血压平时需要注意什么？", "session_id": "test123"}'
```

Response:
```json
{
  "session_id": "test123",
  "intent": "health",
  "reply": "您好！关于高血压的日常护理..."
}
```

---

## 🧪 Agent Pipeline Detail

### 1. Intent Classifier
Classifies every user message into one of three categories using MiMo LLM, with a keyword-based fallback for offline use:
- `chat` — casual conversation, emotional expression
- `health` — medical/wellness questions
- `emergency` — urgent situations requiring immediate attention

### 2. Knowledge Retriever (RAG)
When a health question is detected, searches a local knowledge base with fuzzy keyword + text similarity matching. Provides contextual references to the dialogue agent.

### 3. Companion Dialogue Agent
The core agent powered by **MiMo-V2.5**. Uses a carefully crafted system prompt to ensure warm, safe, and elderly-appropriate responses. Maintains conversation context for multi-turn dialogue.

### 4. Safety Reviewer
Post-generation content moderation. Filters out medical prescriptions, drug brand recommendations, and panic-inducing content. Ensures all outputs are suitable for elderly users.

---

## 📂 Project Structure

```
silverage-companion/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py             # Environment configuration
│   ├── agents/
│   │   ├── intent.py         # Intent classifier agent
│   │   ├── retrieval.py      # RAG knowledge retrieval
│   │   ├── companion.py      # Dialogue system prompts
│   │   └── safety.py         # Content safety filter
│   ├── services/
│   │   ├── llm.py            # MiMo API client
│   │   └── chat_service.py   # Agent orchestration
│   ├── api/
│   │   ├── chat.py           # Chat API endpoints
│   │   └── health.py         # Health search API
│   ├── models/
│   │   ├── database.py       # SQLite setup
│   │   └── chat.py           # Conversation ORM
│   └── static/
│       ├── index.html        # Elderly-friendly chat UI
│       ├── style.css         # Accessible styling
│       └── app.js            # Frontend logic
├── data/
│   └── knowledge_base.json   # Health knowledge entries
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🎯 Use Cases

| Scenario | Example |
|----------|---------|
| Daily companionship | "今天天气不错，想出去走走" |
| Medication guidance | "降压药忘了吃怎么办？" |
| Sleep advice | "最近总是睡不着，有什么办法？" |
| Diet management | "糖尿病能吃什么水果？" |
| Exercise suggestions | "膝盖不好适合做什么运动？" |
| Emergency alert | "我胸口突然很闷..." → triggers emergency protocol |

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | MiMo-V2.5 (Xiaomi, OpenAI-compatible API) |
| **Backend** | Python 3.11 + FastAPI |
| **Database** | SQLite + SQLAlchemy ORM |
| **Frontend** | Vanilla HTML/CSS/JS (zero dependencies) |
| **Deployment** | Docker + docker-compose |
| **Model Context** | Up to 100K tokens (leverages MiMo-V2.5 long context) |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built for the [Xiaomi MiMo Orbit 100T Token Program](https://100t.xiaomimimo.com)
- Powered by [MiMo-V2.5](https://platform.xiaomimimo.com) large language model
- Inspired by the growing need for AI-powered elderly care solutions

---

*Made with ❤️ for the silver generation*

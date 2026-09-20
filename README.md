

# 💰 MoneyFollows

### AI-Powered Government Scheme Discovery & Eligibility Assistant

*Describe your situation in plain language — MoneyFollows finds the government schemes you may be eligible for.*

Built for **Hackday 1.0 — Tech for a Better Tomorrow**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React_19-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite_8-646CFF?style=flat-square&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_v4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

</div>

---

## 🎯 The Problem

Millions of Indian citizens miss out on government benefits because:

1. **Information is scattered** — Schemes are spread across hundreds of `.gov.in` websites with no single source of truth.
2. **Eligibility is confusing** — Complex criteria written in bureaucratic language make it hard to know if you qualify.
3. **Search engines fall short** — Generic results return outdated lists instead of personalized, actionable recommendations.

## 💡 The Solution

**MoneyFollows** is an AI-powered assistant that lets users describe their situation in natural language (English or Hindi) and instantly discovers relevant government schemes. It dynamically searches official sources, extracts eligibility criteria using LLMs, and evaluates them against the user's profile using a **deterministic, rule-based engine** — avoiding hallucinations.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗣️ **Natural Language Search** | Ask in plain English or Hindi — *"I'm a 22-year-old B.Tech student from UP. What scholarships can I get?"* |
| 🔍 **Real-Time Web Discovery** | Dynamically fetches scheme data from official `.gov.in` and `.nic.in` sources |
| 🧮 **Deterministic Eligibility** | Rule-based engine evaluates Age, Income, State, Gender, Category, Education, Occupation — no LLM guessing |
| 💬 **Follow-Up Chat** | Context-aware conversations to drill deeper into specific schemes |
| 🌐 **Bilingual UI** | Full English & Hindi support for both interface and AI responses |
| 🌗 **Dark / Light Mode** | System-preference aware theme with manual toggle |
| 📄 **Source Citations** | Every scheme links back to its official source for verification |
| 📊 **Eligibility Statuses** | Clear labels — *Likely Eligible*, *Possibly Eligible*, *Needs More Info*, *Likely Not Eligible* |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                    │
│              Tailwind CSS v4  •  Lucide Icons                │
└──────────────────────┬───────────────────────────────────────┘
                       │  REST API
┌──────────────────────▼───────────────────────────────────────┐
│                  FastAPI Backend (Python)                     │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   Orchestrator Pipeline                  │ │
│  │                                                         │ │
│  │  1. Query Understanding ──► Extracts intent & profile   │ │
│  │  2. Web Search ───────────► Fetches from .gov.in        │ │
│  │  3. Scheme Extraction ────► Structures data via LLM     │ │
│  │  4. Eligibility Engine ───► Deterministic rule matching  │ │
│  │  5. Answer Generation ────► User-friendly summary       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ LLM      │  │ Search       │  │ Eligibility Engine     │ │
│  │ Provider  │  │ Provider     │  │ (Rule-Based)           │ │
│  │          │  │              │  │                        │ │
│  │ • Google  │  │ • DuckDuckGo │  │ • Age / Income         │ │
│  │ • OpenAI  │  │ • Tavily     │  │ • State / Gender       │ │
│  │ • OpenR.  │  │ • Serper     │  │ • Education / Category │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite 8, Tailwind CSS v4, Lucide React |
| **Backend** | Python 3.10+, FastAPI, Pydantic, HTTPX |
| **LLM Providers** | Google Gemini *(default)*, OpenAI, OpenRouter |
| **Search Providers** | DuckDuckGo *(default, free)*, Tavily, Serper |
| **Data** | 161 central government schemes in local dataset |
| **Deployment** | Docker (multi-stage build), Docker Compose |

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** v20+
- **Python** v3.10+
- **API Key** for at least one LLM provider (Google AI recommended — free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/axyz97836/Money-Follow-s.git
cd Money-Follow-s
```

> 🔗 **GitHub:** [github.com/axyz97836/Money-Follow-s](https://github.com/axyz97836/Money-Follow-s)

### 2. Environment Setup

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required — pick one LLM provider
LLM_PROVIDER=google
GOOGLE_API_KEY=your_google_api_key_here

# Search — DuckDuckGo works out of the box (no key needed)
SEARCH_PROVIDER=duckduckgo
```

### 3. Start the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

### 4. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

### 🐳 Running via Docker (Alternative)

```bash
docker-compose up --build
```

This builds both frontend and backend into a single container and serves the app on port `8000`.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check & service status |
| `POST` | `/api/search` | Full scheme discovery & eligibility pipeline |
| `POST` | `/api/chat` | Context-aware follow-up conversation |

### Example — Search for Schemes

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I am a farmer from Uttar Pradesh. What schemes may help me?",
    "profile": {
      "age": 45,
      "state": "Uttar Pradesh",
      "occupation": "Farmer"
    }
  }'
```

> See [`docs/API.md`](docs/API.md) for full request/response schemas.

---

## 📁 Project Structure

```
moneyfollows/
├── frontend/                  # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx            # Main application component
│   │   ├── api/               # API client
│   │   ├── lib/i18n.js        # English & Hindi translations
│   │   ├── constants.js       # States, education levels, categories
│   │   └── index.css          # Tailwind v4 styles & custom theme
│   └── package.json
│
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Centralized settings (env vars)
│   │   ├── api/routes/        # REST endpoint handlers
│   │   ├── models/            # Pydantic data models
│   │   ├── prompts/           # LLM prompt templates
│   │   ├── services/
│   │   │   ├── orchestrator.py    # Main pipeline coordinator
│   │   │   ├── llm/provider.py    # Multi-provider LLM abstraction
│   │   │   ├── search/provider.py # Multi-provider search abstraction
│   │   │   ├── eligibility/engine.py  # Deterministic rule engine
│   │   │   ├── citations/        # Source citation service
│   │   │   └── ranking/          # Result ranking service
│   │   └── tests/             # Unit tests
│   ├── data/                  # Government scheme dataset (161 schemes)
│   └── requirements.txt
│
├── docs/                      # Documentation
│   ├── PRD.md                 # Product Requirements
│   ├── ARCHITECTURE.md        # System Architecture
│   └── API.md                 # API Reference
│
├── Dockerfile                 # Multi-stage production build
├── docker-compose.yml         # One-command deployment
└── .env.example               # Environment variable template
```

---

## 🧪 Running Tests

```bash
cd backend
pytest app/tests/ -v
```

---

## 🔧 Configuration

All configuration is managed through environment variables. See [`.env.example`](.env.example) for the full list.

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `google` | LLM provider: `google`, `openai`, or `openrouter` |
| `LLM_MODEL` | `gemini-2.0-flash` | Model name for the selected provider |
| `SEARCH_PROVIDER` | `duckduckgo` | Search provider: `duckduckgo`, `tavily`, or `serper` |
| `SEARCH_TIMEOUT` | `30` | Web search timeout in seconds |
| `LLM_TIMEOUT` | `60` | LLM request timeout in seconds |
| `RATE_LIMIT_PER_MINUTE` | `30` | API rate limit per client per minute |

---

## 📚 Documentation

- [Product Requirements (PRD)](docs/PRD.md) — Problem statement, features & constraints
- [System Architecture](docs/ARCHITECTURE.md) — Pipeline design & tech stack details
- [API Reference](docs/API.md) — Endpoints, request/response schemas

---

## ⚠️ Disclaimer

MoneyFollows is an **informational tool** designed to help citizens discover government schemes. It does **not**:
- Apply for schemes on behalf of users
- Store any personal data persistently
- Guarantee eligibility — always verify with official government sources

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

<div align="center">

Made with ❤️ for **Hackday 1.0 — Tech for a Better Tomorrow**

</div>

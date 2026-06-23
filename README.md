# VibeDeploy — AI Multi-Agent SaaS Architect

<div align="center">

![VibeDeploy](https://img.shields.io/badge/VibeDeploy-AI%20SaaS%20Generator-purple?style=for-the-badge&logo=lightning&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=for-the-badge&logo=streamlit)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Multi--Model-orange?style=for-the-badge&logo=google)
![FastAPI](https://img.shields.io/badge/FastAPI-Generated-teal?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-Generated-black?style=for-the-badge&logo=next.js)

**Describe your software idea in plain English — VibeDeploy's team of five specialized AI agents will design the database schema, write the FastAPI backend, build the Next.js frontend, craft the marketing copy, and package everything into a ready-to-run ZIP archive.**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Agent Pipeline](#-agent-pipeline)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [How It Works](#-how-it-works)
- [Model Selection](#-model-selection)
- [CLI Reference](#-cli-reference)
- [Deployment](#-deployment)
- [Known Issues & Limitations](#-known-issues--limitations)
- [Roadmap](#-roadmap)

---

## 🚀 Overview

**VibeDeploy** is a multi-agent AI system built for the **Kaggle Vibe Coding Hackathon**. It takes a plain-English description of any SaaS idea and orchestrates five specialized AI agents that collaborate through a shared state pipeline to produce a complete, runnable software project.

- 🧠 **Describe** — Type your SaaS idea in plain English, as specific or vague as you like
- 📐 **Design** — The Architect agent designs the relational database schema and technology stack
- ⚙️ **Build** — The Backend agent writes production-ready FastAPI Python source code
- 🎨 **Style** — The Frontend agent creates Next.js React components with Tailwind CSS
- 📈 **Market** — The Marketing agent generates a landing page headline, pricing tiers, and a professional README
- 📦 **Deploy** — Everything is packaged into a downloadable ZIP archive, ready to run

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Natural Language Input** | Describe any SaaS idea in plain English — no technical spec required |
| 🤖 **5-Agent Collaboration** | Orchestrator → Architect → Backend → Frontend → Marketing agents run in sequence |
| 🔗 **Shared State Memory** | All agents read and write a single shared state dictionary, enabling rich handoffs |
| ⚙️ **FastAPI Backend Generation** | Produces `main.py`, `models.py`, `routes.py`, `schemas.py`, `database.py`, and `requirements.txt` |
| 🎨 **Next.js Frontend Generation** | Generates pages, React components, `package.json`, and Tailwind CSS configuration |
| 🗃️ **Relational Schema Design** | Architect agent designs normalized SQLite/SQLAlchemy database tables with relationships |
| 📈 **Marketing Copywriting** | AI-generated hero headline, subheadline, value propositions, and 3-tier pricing strategy |
| 📄 **Custom README Generation** | Each project gets a tailored, professional README following a production-grade template |
| 📦 **One-Click ZIP Download** | All generated files are packaged into a single downloadable ZIP archive |
| 🎛️ **Model Selector** | Choose from 7 Gemini models (free and paid) directly from the sidebar |
| 🔁 **Rate Limit Resilience** | Exponential backoff retry logic handles 429 and 503 API quota errors automatically |
| 🖥️ **Premium Streamlit UI** | Dark-mode glassmorphism UI with real-time progress indicators and tabbed result views |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                                │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    Streamlit Web UI (app.py)                     ││
│  │  Sidebar: Model Selector · Concept Map                          ││
│  │  Main:    Prompt Input → Progress Bar → Tabbed Results          ││
│  └─────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────┬──────────────────────────────────┘
                                   │  User submits SaaS idea
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     AGENT PIPELINE (Python)                          │
│                                                                      │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│   │ Orchestrator │───▶│  Architect   │───▶│   Backend    │          │
│   │   Agent      │    │   Agent      │    │   Agent      │          │
│   │              │    │              │    │              │          │
│   │ product_name │    │  db_schema   │    │ backend_code │          │
│   │ description  │    │  stack       │    │ (6 files)    │          │
│   │ features[]   │    │              │    │              │          │
│   └──────────────┘    └──────────────┘    └──────┬───────┘          │
│                                                  │                  │
│                                                  ▼                  │
│                        ┌──────────────┐    ┌──────────────┐         │
│                        │  Marketing   │◀───│  Frontend    │         │
│                        │   Agent      │    │   Agent      │         │
│                        │              │    │              │         │
│                        │ hero_headline│    │frontend_code │         │
│                        │ pricing_tiers│    │ (6 files)    │         │
│                        │ readme (md)  │    │              │         │
│                        └──────┬───────┘    └──────────────┘         │
└───────────────────────────────┼─────────────────────────────────────┘
                                │
                                ▼
              ┌────────────────────────────────┐
              │        utils/zipper.py          │
              │                                │
              │  backend/ + frontend/ + README  │
              │  → Packaged into .ZIP archive   │
              └────────────────────────────────┘
                                │
                                ▼
                   💾 Downloadable .ZIP file
```

---

## 🤖 Agent Pipeline

Each agent is a standalone Python class with a `run(state) → state` interface. They share a single dictionary that accumulates output as it flows through the pipeline.

| Step | Agent | Input | Output |
|------|-------|-------|--------|
| 1 | **OrchestratorAgent** | `user_input` (plain English) | `product_name`, `description`, `features[]` |
| 2 | **ArchitectAgent** | `product_name`, `features[]` | `db_schema[]`, `stack{}` |
| 3 | **BackendAgent** | `db_schema[]`, `stack{}` | `backend_code{}` (6 Python files) |
| 4 | **FrontendAgent** | `features[]`, `stack{}` | `frontend_code{}` (6 JS/config files) |
| 5 | **MarketingAgent** | All of the above | `marketing_copy{}` (JSON metadata + Markdown README) |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI** | Streamlit 1.35+ | Glassmorphic dark-mode web interface |
| **AI Models** | Google Gemini (via `google-genai` SDK) | All 5 agents — content generation & reasoning |
| **Agent Orchestration** | Python 3.10+ (custom pipeline) | Shared state multi-agent coordination |
| **Generated Backend** | FastAPI + SQLAlchemy + SQLite | Scaffolded REST API for each project |
| **Generated Frontend** | Next.js 16 + React + Tailwind CSS | Scaffolded web client for each project |
| **Packaging** | Python `zipfile` (in-memory) | ZIP archive generation without disk I/O |
| **Config** | `python-dotenv` | Environment variable management |

---

## 📁 Project Structure

```
VibeDeploy/
├── agents/
│   ├── orchestrator.py    # Agent 1: Parses idea → product spec (JSON)
│   ├── architect.py       # Agent 2: Designs DB schema & stack (JSON)
│   ├── backend.py         # Agent 3: Generates FastAPI source code
│   ├── frontend.py        # Agent 4: Generates Next.js components
│   └── marketing.py       # Agent 5: Writes copy, pricing & README
├── utils/
│   ├── state.py           # Shared state, GenAI client wrapper, retry logic
│   └── zipper.py          # In-memory ZIP packager
├── app.py                 # Streamlit web UI (main entry point)
├── main.py                # CLI pipeline runner
├── .env.example           # Template for environment variables
├── requirements.txt       # Python dependencies
└── test.py                # Quick connectivity test — verifies your API key works
```

### 🔌 Verify Your Setup

Before running the full pipeline, use `test.py` to confirm your API key is valid and the Gemini connection is working:

```python
# test.py
from utils.state import get_model

model = get_model()
response = model.generate_content("Say: VibeDeploy is connected!")
print(response.text)
```

```bash
python test.py
```

**Expected output:**
```
VibeDeploy is connected!
```

If you see that line, your `GEMINI_API_KEY` is set correctly and the project is ready to use.

### Generated Project Output Structure

Each generated project follows this layout inside the ZIP:

```
<ProductName>/
├── backend/
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # SQLAlchemy ORM models
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── routes.py          # API route handlers
│   ├── database.py        # DB connection & session setup
│   └── requirements.txt   # Backend Python dependencies
├── frontend/
│   ├── pages/
│   │   └── index.jsx      # Main dashboard page
│   ├── components/
│   │   ├── Navbar.jsx     # Navigation component
│   │   ├── Metrics.jsx    # Stats/metrics cards
│   │   └── Auth.jsx       # Login/register forms
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS configuration
└── README.md              # AI-generated project-specific README
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.10+
- **pip**
- A **Google AI Studio API key** → [aistudio.google.com](https://aistudio.google.com/apikey) *(free)*

### 1. Clone the Repository

```bash
git clone https://github.com/adhipatya3552/vibedeploy.git
cd vibedeploy
```

### 2. Create a Virtual Environment

**Windows (PowerShell / CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt, confirming the environment is active.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API key (see [Environment Variables](#-environment-variables) below).

### 5. Launch the Web UI

```bash
streamlit run app.py
```

App runs at → **http://localhost:8501**

### 6. Or Use the CLI

```bash
python main.py "I want a SaaS for freelancers to track clients, invoices, and payments"
```

Output is saved to `output/<product_name>/` and `output/<product_name>.zip`.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | Google AI Studio API key. Get one free at [aistudio.google.com](https://aistudio.google.com/apikey) |
| `VIBEDEPLOY_MODEL` | Optional | Override the Gemini model ID. Defaults to `gemini-3.1-flash-lite` if unset |

> **Streamlit Cloud deployment**: Add `GEMINI_API_KEY` under **Settings → Secrets** in your Streamlit Cloud dashboard. Never expose the key in the UI.
>
> **Generate a key**: Visit [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) — free tier includes 1,500 requests/day on most models.

---

## ⚙️ How It Works

### Step 1 — User Describes the Idea
User types a plain-English SaaS description into the text area (e.g. *"A tool for pet sitting businesses to manage bookings, client profiles, and payments"*).

### Step 2 — Orchestrator Parses the Concept
The `OrchestratorAgent` sends the raw text to Gemini and extracts a structured JSON spec: `product_name`, `description`, and a list of 4–6 developer-friendly `features`.

### Step 3 — Architect Designs the Schema
The `ArchitectAgent` receives the spec and designs the relational database — producing a `db_schema` list of tables with typed columns, primary keys, foreign keys, and nullability constraints, plus a `stack` object specifying backend/frontend/db choices.

### Step 4 — Backend Agent Writes Python Code
The `BackendAgent` uses the schema and stack to generate a full FastAPI project: SQLAlchemy models, Pydantic schemas, route handlers with CRUD operations, database setup, and a `requirements.txt`.

### Step 5 — Frontend Agent Writes React Code
The `FrontendAgent` generates a Next.js project with a responsive Tailwind CSS dashboard, authentication forms, metrics cards, and a navigation component — all wired to call the generated API endpoints.

### Step 6 — Marketing Agent Creates Copy & README
The `MarketingAgent` runs two separate model calls:
1. **JSON call** → generates `hero_headline`, `hero_subheadline`, `copywriting_bullets`, and 3 `pricing_tiers`
2. **Text call** → generates a full professional `README.md` tailored to the specific product

### Step 7 — ZIP Packaging
`utils/zipper.py` assembles all generated files into an in-memory ZIP archive (`backend/` + `frontend/` + `README.md`) and serves it as a one-click download via the Streamlit UI.

---

## 🎛️ Model Selection

VibeDeploy supports 7 Gemini models selectable from the sidebar, sourced from the [official Google AI model list](https://ai.google.dev/gemini-api/docs/models):

| Model | ID | Tier |
|-------|----|------|
| Gemini 3.5 Flash *(Newest)* | `gemini-3.5-flash` | 🆓 Free |
| **Gemini 3.1 Flash Lite** *(Default)* | `gemini-3.1-flash-lite` | 🆓 Free |
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | 🆓 Free |
| Gemini 2.5 Flash | `gemini-2.5-flash` | 🆓 Free |
| Gemini 2.5 Flash Lite | `gemini-2.5-flash-lite` | 🆓 Free |
| Gemini 2.5 Pro | `gemini-2.5-pro` | 💰 Paid |
| Gemini 3.1 Pro Preview | `gemini-3.1-pro-preview` | 💰 Paid |

All rate-limit errors (429 / 503) are caught and retried automatically with exponential backoff (up to 6 attempts, max 60s delay).

---

## 💻 CLI Reference

Run the full pipeline from the terminal without the UI:

```bash
python main.py "<your SaaS idea>"
```

**Example:**
```bash
python main.py "A SaaS platform where restaurants can manage reservations, table assignments, and waitlists"
```

**Output:**
```
============================================================
================= VibeDeploy CLI Pipeline ==================
============================================================

[Step 1/5] Running Orchestrator Agent...
[+] Orchestrator Agent: Identified Product -> 'TableFlow'

[Step 2/5] Running Architect Agent...
[+] Architect Agent: Designed 4 tables.

[Step 3/5] Running Backend Agent...
[+] Backend Agent: Generated 6 files.

[Step 4/5] Running Frontend Agent...
[+] Frontend Agent: Generated 6 files.

[Step 5/5] Running Marketing Agent...
[+] Marketing Agent: Successfully generated customized template-styled README.md.

[+] Success! Complete workspace generated:
  - Source files directory: output\tableflow
  - Downloadable ZIP: output\tableflow.zip
============================================================
```

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo and set **Main file path** to `app.py`
4. Under **Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Click **Deploy**

> ⚠️ **Do not** expose your API key in the Streamlit UI — the sidebar API key input has been removed for security. Always use Streamlit Secrets or environment variables.

---

## ⚠️ Known Issues & Limitations

| Issue | Status | Workaround |
|-------|--------|-----------|
| Free-tier IP quota exhaustion (429) in cloud VMs | Active | Run locally; the retry backoff handles transient limits |
| Generated code is a scaffold, not production-ready | By Design | Use output as a starting point; review and extend before shipping |
| `gemini-2.0-flash` / `gemini-2.0-flash-lite` are deprecated | Active | Removed from dropdown — use Gemini 3.x or 2.5 models |
| Large/complex SaaS ideas may produce incomplete frontend | Active | Be specific in your prompt about key pages and features |
| Multi-drive path issues (`.env` on D: when script runs on C:) | Fixed | `state.py` uses `__file__`-relative path resolution |

---

## 🗺️ Roadmap

- [x] 5-agent pipeline (Orchestrator → Architect → Backend → Frontend → Marketing)
- [x] Shared state memory architecture
- [x] FastAPI + SQLAlchemy backend code generation
- [x] Next.js + Tailwind CSS frontend generation
- [x] In-memory ZIP packaging with one-click download
- [x] Glassmorphic dark-mode Streamlit UI
- [x] Exponential backoff retry for 429/503 rate limits
- [x] AI-generated marketing copy + 3-tier pricing strategy
- [x] Custom project README generation (production-grade template)
- [x] Multi-model selector (7 Gemini models, free + paid)
- [x] CLI runner (`main.py`) for terminal-based usage
- [ ] Authentication scaffolding (JWT) in generated backend
- [ ] Database migration support (Alembic) in generated output
- [ ] Multi-cloud deployment config generation (Dockerfile, Vercel, Fly.io)
- [ ] Agent memory persistence across sessions
- [ ] Support for additional stacks (Django, Express.js, SvelteKit)

---

<div align="center">

Built with ❤️ for developers who deserve to focus on ideas, not boilerplate.

*Submitted to the [Kaggle Vibe Coding Hackathon](https://www.kaggle.com/competitions/vibe-coding-hackathon)*

</div>

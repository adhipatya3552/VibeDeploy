import json
from utils.state import get_model

class MarketingAgent:
    def __init__(self):
        self.model = get_model()
        self.system_prompt_json = """
You are the Lead Marketing Strategist and Copywriter at VibeDeploy.
Your job is to write compelling, high-converting copywriting assets and define a business pricing strategy for the newly generated SaaS.

You will receive the product name, description, and core features list.
Output a JSON object containing:
1. `hero_headline`: A catchy, high-impact headline for the landing page hero section.
2. `hero_subheadline`: A clear, benefit-driven subheadline that explains the value proposition.
3. `copywriting_bullets`: An array of 3-4 key product value propositions or benefits (e.g., "Automate client follow-ups and never miss an invoice payment").
4. `pricing_tiers`: An array of exactly 3 pricing tiers (typically Free, Pro, and Enterprise). Each tier must be an object with:
   - `name`: Tier name (e.g., "Starter", "Pro", "Agency")
   - `price`: Pricing price text (e.g., "$0/month", "$29/month", "Contact Us")
   - `target`: Target customer description (e.g., "Best for solo freelancers just starting out")
   - `features`: An array of 3-5 features included in this tier.

Ensure the copy is custom-tailored to the specific SaaS and uses professional, modern startup terminology.

You MUST respond ONLY with a valid JSON object matching the following structure:
{
  "hero_headline": "string",
  "hero_subheadline": "string",
  "copywriting_bullets": ["string", "string", ...],
  "pricing_tiers": [
    {
      "name": "string",
      "price": "string",
      "target": "string",
      "features": ["string", "string", ...]
    }
  ]
}
Do not add any markdown formatting, explanations, or code fences around the JSON response. Just the raw JSON.
"""

        self.system_prompt_readme = """
You are a Lead Technical Writer at VibeDeploy.
Your job is to write a complete, extremely professional, and detailed markdown README.md file for the generated SaaS workspace.

You will receive:
- Product name
- Description
- Core features list
- Tech stack details
- Database schema tables

You MUST write the README.md content in raw markdown. Do not wrap it in JSON. Do not write any introduction or explanation outside of the markdown itself.

The README.md MUST strictly follow the exact style, formatting, and layout of the following structure:

# [Product Name] — [Catchy Tagline]

<div align="center">

![[Product Name] Logo](https://img.shields.io/badge/[Product Name]-[Catchy%20Tagline]-red?style=for-the-badge&logo=heart&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16.2-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-teal?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3.0-blue?style=for-the-badge&logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Auth-green?style=for-the-badge&logo=jsonwebtokens)

**[A bold, italicized 1-sentence value proposition custom-tailored to the SaaS concept.]**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Authentication System](#-authentication-system)
- [How It Works](#-how-it-works)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Known Issues & Limitations](#-known-issues--limitations)
- [Roadmap](#-roadmap)

---

## 🏥 Overview

**[Product Name]** is [1-2 sentences overview of the product]. [Detail what the system does using emojis and clear bullet points].

---

## ✨ Features

A markdown table detailing 6-10 specific features and their descriptions customized for this SaaS.
| Feature | Description |
|---------|-------------|
| [Feature Name 1] | [Detailed description of feature 1] |
| [Feature Name 2] | [Detailed description of feature 2] |
...

---

## 🏗️ Architecture

A clean text-based ASCII flowchart block using box drawing characters representing client browser calling Next.js API Routes and Next.js calling the FastAPI backend endpoints, which connect to SQLite.
Ensure you represent the login/auth flow and main feature page flows.

---

## 🛠️ Tech Stack

A markdown table showing Layer, Technology, and Purpose.
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js + React + JavaScript/JSX | Web client interface |
| **Backend** | FastAPI + Python | Robust API layer |
| **Database** | SQLite + SQLAlchemy | Structured relational data storage |
| **Authentication** | JWT (JSON Web Tokens) | Secure session authentication |

---

## 📁 Project Structure

A clean code tree comment layout showing the folder tree matching the generated FastAPI backend and Next.js frontend workspace:
```
[Product Name]/
├── backend/
│   ├── main.py        # Application entry point
│   ├── models.py      # Database models (SQLAlchemy schemas)
│   ├── routes.py      # FastAPI API endpoints / routers
│   └── database.py    # DB connection setup
├── frontend/
│   ├── pages/
│   │   ├── index.jsx  # Main user dashboard / home
│   │   ├── login.jsx  # User sign-in page
│   │   └── _app.jsx   # Next.js app wrapper
│   └── styles/
│       └── globals.css# Modern dark glassmorphic styles
├── .env               # Environment variables template
└── requirements.txt   # Backend dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** v18+
- **Python** 3.9+
- **pip**

### 1. Setup Backend
Detailed installation/execution commands block.

### 2. Setup Frontend
Detailed installation/execution commands block.

---

## 🔑 Environment Variables

A markdown table detailing required environment variables.
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ Yes | SQLite database URL (e.g. `sqlite:///./app.db`) |
| `JWT_SECRET` | ✅ Yes | Secret key for signing authentication JSON Web Tokens |
| `GEMINI_API_KEY` | Optional | API key for Gemini models if AI features are enabled |

---

## 🔐 Authentication System

A detailed description of the JSON Web Tokens (JWT) authentication system, Access Token Strategy, How It Works, and Security Best Practices.

---

## ⚙️ How It Works

A detailed 4-8 step user/system flow from login to processing actions, updating SQLite, and loading dashboard state.

---

## 📡 API Reference

Detailed descriptions and JSON request/response formats.
Include definitions for:
- `POST /api/auth/register` (Registers a new user account)
- `POST /api/auth/login` (Authenticates a user and issues a JWT token)
- At least 2 CRUD endpoints tailored to the specific database schema tables generated for the SaaS.

---

## 🧪 Testing

Detailed instructions on how to run backend unit tests (e.g. `pytest`).

---

## 🌐 Deployment

Detailed instructions for deploying the backend (to Fly.io/Render) and the frontend (to Vercel).

---

## ⚠️ Known Issues & Limitations

A markdown table detailing known limitations.
| Issue | Status | Workaround |
|-------|--------|-----------|
| SQLite lacks concurrency under heavy writes | Active | Upgrade to PostgreSQL for high traffic production uses |
| Client-side token storage security | Active | Ensure cookies are configured as HttpOnly in production |

---

## 🗺️ Roadmap

Checkboxed roadmap list:
- [x] Initial FastAPI backend scaffolding
- [x] Next.js frontend pages and styled components
- [x] JWT user registration and authentication
- [x] Interactive responsive layout and styling
- [ ] Database migration utilities
- [ ] Comprehensive unit and integration test suite
- [ ] Multi-tenant isolation

---

<div align="center">

Built with ❤️ for [Target Audience] who deserve to focus on [Main Value], not paperwork.

</div>
"""


    def run(self, state):
        """
        Executes the Marketing Agent.
        Inputs: state dictionary containing 'product_name', 'description', 'features', 'stack', 'db_schema'
        Outputs: updated state dictionary containing 'marketing_copy'
        """
        print(f"[*] Marketing Agent: Generating copy and pricing for '{state['product_name']}'")
        
        context = {
            "product_name": state["product_name"],
            "description": state["description"],
            "features": state["features"]
        }
        
        prompt_json = f"Product Concept Details:\n{json.dumps(context, indent=2)}"
        
        response_json = self.model.generate_content(
            contents=[self.system_prompt_json, prompt_json],
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Initialize marketing dictionary
        state["marketing_copy"] = {}
        
        try:
            data = json.loads(response_json.text.strip())
            state["marketing_copy"]["hero_headline"] = data.get("hero_headline", "Revolutionize Your Workflow")
            state["marketing_copy"]["hero_subheadline"] = data.get("hero_subheadline", "The simplest way to manage your business.")
            state["marketing_copy"]["copywriting_bullets"] = data.get("copywriting_bullets", [])
            state["marketing_copy"]["pricing_tiers"] = data.get("pricing_tiers", [])
            print("[+] Marketing Agent: Successfully generated product copy deck.")
        except Exception as e:
            print(f"[-] Marketing Agent: Error parsing JSON: {e}")
            # Fallback copy
            state["marketing_copy"]["hero_headline"] = f"Empower Your Work with {state['product_name']}"
            state["marketing_copy"]["hero_subheadline"] = state["description"]
            state["marketing_copy"]["copywriting_bullets"] = ["Fast performance", "Modern design", "Easy integrations"]
            state["marketing_copy"]["pricing_tiers"] = [
                {"name": "Free", "price": "$0/month", "target": "Individual builders", "features": ["Core features", "Community support"]},
                {"name": "Pro", "price": "$29/month", "target": "Growing businesses", "features": ["Advanced features", "Email support"]},
                {"name": "Enterprise", "price": "Custom", "target": "Large scale projects", "features": ["Dedicated support", "Custom SLA"]}
            ]
            
        # Step B: Generate README.md dynamically in raw text
        print(f"[*] Marketing Agent: Generating custom template-styled README.md for '{state['product_name']}'...")
        
        readme_context = {
            "product_name": state["product_name"],
            "description": state["description"],
            "features": state["features"],
            "stack": state.get("stack", {}),
            "db_schema": state.get("db_schema", [])
        }
        
        prompt_readme = f"Technical Specifications:\n{json.dumps(readme_context, indent=2)}"
        
        try:
            response_readme = self.model.generate_content(
                contents=[self.system_prompt_readme, prompt_readme]
            )
            state["marketing_copy"]["readme"] = response_readme.text.strip()
            print("[+] Marketing Agent: Successfully generated customized template-styled README.md.")
        except Exception as e:
            print(f"[-] Marketing Agent: Error generating README.md: {e}")
            state["marketing_copy"]["readme"] = f"# {state['product_name']}\n\n{state['description']}\n"
            
        return state

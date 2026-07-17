# QuantData Platform

**An AI-powered alternative data platform for quantitative researchers and hedge funds.**

QuantData ingests, normalizes, and indexes non-traditional financial data sources — making them queryable via SQL, natural language (NL→SQL), and semantic vector search. Built for point-in-time integrity so every data point is safe for backtesting.

---

## 🧠 What It Does

Traditional quant platforms focus on price and volume. QuantData focuses on **the events that move prices** — clinical trial outcomes, patent filings, and bank stress test results — and makes them instantly searchable.

| Feature | Description |
|---|---|
| **Unified Event Schema** | Every data point — regardless of source — is normalized into a single `events` table with structured JSONB fields. |
| **Point-in-Time Integrity** | Every event has a `published_at` timestamp (when it became public) and a `content_date` (what period it refers to), ensuring clean backtests with no lookahead bias. |
| **AI-Powered Querying** | Ask questions in plain English (e.g., *"Which banks had the lowest CET1 ratio in the 2023 stress test?"*) and Gemini translates it to SQL automatically. |
| **Semantic Search** | Find related events using vector embeddings powered by `pgvector`, not just keyword matching. |
| **Python SDK** | Access all data programmatically with `QuantDataClient` — returns pandas DataFrames ready for analysis. |

---

## 📊 Data Verticals

### 1. Clinical Trials (Pharma & Biotech)
- **Source:** [ClinicalTrials.gov](https://clinicaltrials.gov/) API
- **Update Frequency:** Every 6 hours
- **Key Fields:** Phase, Status, Indication, Enrollment, Sponsor
- **Use Case:** Detect phase transitions (e.g., Phase 2 → Phase 3) before market reaction.

### 2. Patents (Technology & IP)
- **Source:** [PatentsView](https://patentsview.org/) API (USPTO)
- **Update Frequency:** Weekly
- **Key Fields:** Assignee, Technology Clusters, CPC Codes, Grant Date
- **Use Case:** Track patent velocity as a leading indicator of R&D investment.

### 3. Bank Stress Tests (Financials)
- **Source:** Federal Reserve DFAST/CCAR Reports
- **Update Frequency:** Annually
- **Key Fields:** Pre/Post-Stress CET1, Stress Capital Buffer, Loss Projections
- **Use Case:** Identify banks with excess capital (buyback candidates) vs. those near regulatory minimums.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Web Dashboard                     │
│          (Next.js + TailwindCSS on Vercel)          │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────┐
│                  Backend API                        │
│            (FastAPI + Uvicorn on Render)             │
│                                                     │
│   /api/events   — Browse & filter events            │
│   /api/query    — Raw SQL & semantic search          │
│   /api/ask      — Natural language → SQL (Gemini)    │
└──────────────────────┬──────────────────────────────┘
                       │ asyncpg
┌──────────────────────▼──────────────────────────────┐
│               PostgreSQL + pgvector                 │
│                  (Neon Serverless)                   │
│                                                     │
│   events table — JSONB + GIN + HNSW vector index    │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Python SDK
```python
from quantdata import QuantDataClient

client = QuantDataClient(base_url="https://your-api.onrender.com/api")

# Get all clinical trial events
trials = client.get_events(event_type="trial")

# Ask a question in plain English
result = client.ask("Which Phase 3 trials failed in the last 30 days?")
print(result["sql_generated"])
print(result["df"])

# Raw SQL
df = client.query("SELECT * FROM events WHERE ticker = 'PFE' ORDER BY published_at DESC LIMIT 10")

# Semantic search
similar = client.semantic_search("FDA approval for cancer drug")
```

### Web Dashboard
The dashboard provides four views:
- **Data Explorer** — Browse and filter all ingested events
- **AI Chat** — Ask questions in natural language, see the generated SQL and results
- **Entity Timeline** — View a chronological event feed for any ticker
- **Data Catalog** — Schema reference for all supported data sources

---

## 🛠️ Tech Stack

| Layer | Technology | Hosting |
|---|---|---|
| Database | PostgreSQL 16 + pgvector | [Neon](https://neon.tech/) (Free Tier) |
| Backend API | Python, FastAPI, SQLAlchemy, asyncpg | [Render](https://render.com/) (Free Tier) |
| Frontend | Next.js 14, TypeScript, TailwindCSS | [Vercel](https://vercel.com/) (Free Tier) |
| AI / LLM | Google Gemini 2.5 Flash | [Google AI Studio](https://aistudio.google.com/) (Free Tier) |
| Automation | GitHub Actions (cron workflows) | GitHub (Free Tier) |
| SDK | Python, pandas, requests | PyPI (planned) |

**Total hosting cost: $0/month**

---

## 📁 Project Structure

```
quantdataplatform/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI route handlers
│   │   ├── ai/            # Gemini SQL translator, embeddings
│   │   ├── ingestion/     # Data pipeline for each vertical
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── config.py      # Environment configuration
│   │   ├── database.py    # Async database engine
│   │   └── main.py        # FastAPI application entry point
│   ├── alembic/           # Database migrations
│   ├── scripts/           # CLI ingestion scripts
│   └── requirements.txt
├── frontend/
│   ├── app/               # Next.js App Router pages
│   ├── components/        # Reusable React components
│   └── lib/               # Utilities
├── sdk/
│   └── quantdata/         # Python SDK package
├── .github/
│   └── workflows/         # Automated ingestion cron jobs
└── README.md
```

---

## 📄 License

This project is for educational and research purposes.

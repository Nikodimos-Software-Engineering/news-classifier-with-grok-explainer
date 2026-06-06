# News Classifier with Grok Explainer

A bilingual (Amharic + English) news article classifier that predicts article categories using scikit-learn, then generates human-readable explanations via the Groq API (Llama 3.3 70B).

## Architecture

```
┌─────────────┐     POST /classify     ┌──────────────┐
│  Streamlit   │ ────────────────────────▶   FastAPI    │
│   Frontend   │ ◀────────────────────────   Backend    │
└─────────────┘     JSON response      └──────┬───────┘
                                              │
                          ┌───────────────────┼───────────────────┐
                          ▼                   ▼                   ▼
                   ┌──────────────┐  ┌───────────────┐  ┌──────────────┐
                   │   Language   │  │  Classifier   │  │    Groq      │
                   │   Detector   │──▶  (English /   │──▶   API       │
                   │              │  │   Amharic)    │  │ (explanation)│
                   └──────────────┘  └───────────────┘  └──────────────┘
```

## Features

- **Language Detection** — Automatically detects Amharic or English text using Unicode character ranges
- **ML Classification** — Logistic Regression with TF-IDF vectorization (trained per language)
- **LLM Explanations** — Groq-powered natural language explanations for each prediction
- **Streamlit UI** — Simple web interface for testing

### Categories

| English | Amharic |
|---------|---------|
| Technology | ስፖርት (Sport) |
| Business | መዝናኛ (Entertainment) |
| Sports | ሀገር አቀፍ ዜና (National News) |
| Entertainment | ቢዝነስ (Business) |
| Politics | ዓለም አቀፍ ዜና (World News) |
| | ፖለቲካ (Politics) |

## Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/)

### Backend

```bash
cd backend
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
uvicorn main:app --reload --port 8000
```

API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
pip install -r requirements.txt
# Optional: set BACKEND_URL in .env if not on localhost:8000
streamlit run app.py
```

Opens at `http://localhost:8501`.

## API

### `POST /classify`

```json
{
  "headline": "Ethiopia launches new satellite",
  "article_body": "The Ethiopian Space Science Institute announced...",
  "source_url": "https://example.com"
}
```

**Response:**

```json
{
  "category": "Technology",
  "confidence": 92.4,
  "explanation": "The article discusses the launch of a satellite...",
  "language_detected": "English",
  "model_used": "English Model",
  "source_url": "https://example.com",
  "mixed_warning": false
}
```

### `GET /health`

Returns `{"status": "ok"}`.

## Model Training

Training data (CSV files) goes in `data/` (gitignored). Run:

```bash
cd model
pip install pandas scikit-learn joblib
python trainer.py
```

Trained pipelines are saved to `model/*.pkl`.

## Deployment

The backend includes a [Render](https://render.com/) config at `backend/render.yaml`. Set `GROQ_API_KEY` as an environment variable.

## Tech Stack

- **Backend**: FastAPI, scikit-learn, joblib, httpx
- **Frontend**: Streamlit, requests
- **ML**: TF-IDF + Logistic Regression pipeline
- **LLM**: Groq API (llama-3.3-70b-versatile)

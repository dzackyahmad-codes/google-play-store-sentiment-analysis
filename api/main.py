# api/main.py

import sys
import os
import json
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# =====================================================
# FIX PATH (PYTHON VS PYINSTALLER)
# =====================================================
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

# =====================================================
# IMPORT INTERNAL MODULE
# =====================================================
from scraper.google_play import GooglePlayScraper
from analysis.batch_inference import run_batch_inference
from analysis.insight_generator import generate_insight
from analysis.summary_engine import generate_summary

from analysis.model.indobertweet import SentimentModel
from analysis.sentiment_engine import SentimentDecisionEngine

# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI(
    title="Sentiment Analysis Platform (Indonesia)",
    description="Analyze Google Play reviews and manual text sentiment",
    version="1.0.0"
)

# =====================================================
# SCHEMA
# =====================================================
class GooglePlayRequest(BaseModel):
    app_id: str
    limit: int = 100


class ManualTextRequest(BaseModel):
    text: str
    rating: int | None = None

# =====================================================
# HELPER
# =====================================================
def safe_app_name(app_id: str) -> str:
    return app_id.replace(".", "_")

# =====================================================
# GOOGLE PLAY ANALYSIS
# =====================================================
@app.post("/analyze/google-play")
def analyze_google_play(data: GooglePlayRequest):
    app_id = data.app_id
    limit = data.limit
    app_name = safe_app_name(app_id)

    raw_path = BASE_DIR / "data" / "raw" / f"{app_name}_raw.json"
    processed_path = BASE_DIR / "data" / "processed" / f"{app_name}_processed.json"
    insight_path = BASE_DIR / "data" / "insight" / f"{app_name}_insight.json"

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    insight_path.parent.mkdir(parents=True, exist_ok=True)

    # STEP 1: SCRAPE
    scraper = GooglePlayScraper()
    reviews = scraper.scrape(app_id, limit)

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    # STEP 2: SENTIMENT
    run_batch_inference(
        input_path=str(raw_path),
        output_path=str(processed_path)
    )

    # STEP 3: INSIGHT
    insight = generate_insight(
        processed_path=str(processed_path),
        insight_path=str(insight_path)
    )

    # STEP 4: SUMMARY
    summary = generate_summary(insight)

    return {
        "app_id": app_id,
        "total_reviews": insight["total_reviews"],
        "sentiment_distribution": insight["sentiment_distribution"],
        "rating_distribution": insight["rating_distribution"],
        "top_negative_keywords": insight["top_negative_keywords"],
        "top_positive_keywords": insight["top_positive_keywords"],
        "summary": summary
    }

# =====================================================
# MANUAL TEXT ANALYSIS
# =====================================================
@app.post("/analyze/manual-text")
def analyze_manual_text(data: ManualTextRequest):
    model = SentimentModel()
    engine = SentimentDecisionEngine()

    model_output = model.predict(data.text)

    response = {
        "model_output": model_output
    }

    if data.rating is not None:
        decision = engine.decide(model_output, data.rating)
        response["decision"] = decision

    return response

# =====================================================
# STATIC UI (SUPER IMPORTANT FOR .EXE)
# =====================================================
UI_DIR = BASE_DIR / "api" / "ui"

app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")

@app.get("/app")
def app_ui():
    return FileResponse(UI_DIR / "app.html")

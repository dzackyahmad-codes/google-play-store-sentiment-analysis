# analysis/run_full_pipeline.py

import sys
import os
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.google_play import GooglePlayScraper
from analysis.batch_inference import run_batch_inference
from analysis.insight_generator import generate_insight
from analysis.summary_engine import generate_summary, load_insight


def safe_app_name(app_id: str) -> str:
    return app_id.replace(".", "_")


def run_pipeline(app_id: str, limit: int):
    app_name = safe_app_name(app_id)

    RAW_PATH = f"data/raw/{app_name}_raw.json"
    PROCESSED_PATH = f"data/processed/{app_name}_processed.json"
    INSIGHT_PATH = f"data/insight/{app_name}_insight.json"

    print("🔹 STEP 1: Scraping Google Play...")
    scraper = GooglePlayScraper()
    reviews = scraper.scrape(app_id, limit)

    os.makedirs("data/raw", exist_ok=True)
    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    print(f"✔ Scraped {len(reviews)} reviews")

    print("\n🔹 STEP 2: Batch Sentiment Analysis...")
    run_batch_inference(
        input_path=RAW_PATH,
        output_path=PROCESSED_PATH
    )

    print("\n🔹 STEP 3: Insight Generation...")
    insight = generate_insight(PROCESSED_PATH, INSIGHT_PATH)

    print("\n🔹 STEP 4: Summary Generation...")
    insight = load_insight(INSIGHT_PATH)
    summary = generate_summary(insight)

    print("\n========== FINAL SUMMARY ==========")
    print(summary)
    print("===================================")


if __name__ == "__main__":
    app_id = input("Masukkan App ID (contoh: com.gojek.app): ").strip()
    limit = int(input("Jumlah review: ").strip())


    run_pipeline(app_id, limit)

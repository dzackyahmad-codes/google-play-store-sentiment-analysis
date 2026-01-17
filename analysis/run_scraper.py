# analysis/run_scraper.py

import json
import os
from scraper.google_play import GooglePlayScraper



OUTPUT_PATH = "data/raw/google_play_reviews.json"


def run_google_play_scraper(app_id: str, limit: int):
    scraper = GooglePlayScraper()
    reviews = scraper.scrape(app_id, limit)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    print(f"Scraped {len(reviews)} reviews from Google Play")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    app_id = input("Masukkan App ID (contoh: com.gojek.app): ").strip()
    limit = int(input("Jumlah review: ").strip())

    run_google_play_scraper(app_id, limit)

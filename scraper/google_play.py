# scraper/google_play.py

from google_play_scraper import reviews, Sort
from scraper.base import BaseScraper


class GooglePlayScraper(BaseScraper):
    def __init__(self, lang="id", country="id"):
        self.lang = lang
        self.country = country

    def scrape(self, app_id: str, limit: int):
        result, _ = reviews(
            app_id,
            lang=self.lang,
            country=self.country,
            sort=Sort.NEWEST,
            count=limit
        )

        cleaned = []
        for r in result:
            cleaned.append({
                "review_id": r.get("reviewId"),
                "user_name": r.get("userName"),
                "rating": r.get("score"),
                "text": r.get("content"),
                "at": r.get("at").isoformat() if r.get("at") else None,
                "source": "google_play",
                "app_id": app_id
            })

        return cleaned

# scraper/base.py

from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self, target_id: str, limit: int):
        pass

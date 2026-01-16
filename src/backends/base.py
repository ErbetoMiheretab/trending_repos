"""Abstract backend interface for different data sources."""

from ..models import Repository
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional


class Backend(ABC):
    """Abstract base class for trending repos backends."""

    @abstractmethod
    def fetch(
        self,
        language: Optional[str],
        since: Optional[datetime] = None,
        topic: Optional[str] = None,
        limit: int = 10,
    ) -> list[Repository]:
        pass

    @abstractmethod
    def get_rate_limit_status(self) -> dict[str, int]:
        pass

    @staticmethod
    def duration_to_since(duration: str) -> datetime:
        """Convert duration string to datetime"""
        now = datetime.now()
        durations = {
            "day": timedelta(days=1),
            "week": timedelta(weeks=1),
            "month": timedelta(days=30),
            "year": timedelta(days=365),
        }
        delta = durations.get(duration, timedelta(weeks=1))
        return now - delta

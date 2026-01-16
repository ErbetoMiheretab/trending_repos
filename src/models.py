from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Repository:
    name: str
    full_name: str
    description: Optional[str]
    url: str
    created_at: datetime
    updated_at: datetime
    topics: list[str] = field(default_factory=list)
    forks: int = 0
    open_issues: int = 0
    owner: str = ""
    stars: Optional[int] = None
    stars_30d_ago: Optional[int] = None

    @property
    def growth_rate(self) -> Optional[float]:
        """Calculate daily growth rate over 30 days."""
        if self.stars_30d_ago is None:
            return None
        diff = self.stars - self.stars_30d_ago
        return diff / 30.0

    @property
    def day_to_10k(self) -> Optional[float]:
        """Predict days until 10k stars at current growth rate."""
        if self.growth_rate is None or self.growth_rate <= 0:
            return None
        remainig = 10_000 - self.stars
        if remainig <= 0:
            return 0.0
        return remainig / self.growth_rate

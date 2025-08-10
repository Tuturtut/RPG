from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GameTime:
    """Horloge in-game (minutes depuis minuit)."""
    day: int = 1
    minute: int = 8 * 60  # 08:00

    def advance(self, minutes: int) -> None:
        if minutes < 0:
            raise ValueError("minutes must be >= 0")
        self.minute += minutes
        while self.minute >= 24 * 60:
            self.minute -= 24 * 60
            self.day += 1

    @property
    def total_minutes(self) -> int:
        return (self.day - 1) * 24 * 60 + self.minute

    def __str__(self) -> str:
        h, m = divmod(self.minute, 60)
        return f"Day {self.day} {h:02d}:{m:02d}"

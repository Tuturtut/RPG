from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Callable, List, Optional, Tuple


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


class Scheduler:
    """Planifie des callbacks sur le temps de jeu (version minimale)."""

    def __init__(self, time: Optional[GameTime] = None) -> None:
        self.time = time or GameTime()
        self._q: List[Tuple[int, int, Callable[[], None]]] = []
        self._counter = 0

    def call_in(self, minutes: int, cb: Callable[[], None]) -> None:
        """Exécute cb dans `minutes` minutes in-game."""
        heappush(self._q, (self.time.total_minutes + minutes, self._counter, cb))
        self._counter += 1

    def call_at(self, hour: int, minute: int, cb: Callable[[], None]) -> None:
        """Planifie cb aujourd'hui à HH:MM (ou demain si déjà passé)."""
        today = (self.time.day - 1) * 24 * 60
        target = today + hour * 60 + minute
        if target <= self.time.total_minutes:
            target += 24 * 60  # demain
        heappush(self._q, (target, self._counter, cb))
        self._counter += 1

    def call_every(self, interval: int, cb: Callable[[], None]) -> None:
        """Planifie cb toutes les `interval` minutes (répétitif)."""
        def wrap() -> None:
            cb()
            self.call_in(interval, wrap)
        self.call_in(interval, wrap)
    
    
    def call_on(self, day: int, hour: int, minute: int, cb: Callable[[], None]) -> None:
        """Planifie cb au JOUR/HEURE/MINUTE absolus (day>=1).
        Utile en attendant un calendrier custom : on reste en minutes absolues.
        """
        if day < 1:
            raise ValueError("day must be >= 1")
        target = (day - 1) * 24 * 60 + hour * 60 + minute
        heappush(self._q, (target, self._counter, cb))
        self._counter += 1


    def tick(self, minutes: int = 1) -> None:
        """Fait avancer le temps et exécute les tâches dues."""
        self.time.advance(minutes)
        while self._q and self._q[0][0] <= self.time.total_minutes:
            _, _, cb = heappop(self._q)
            cb()

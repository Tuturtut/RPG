from __future__ import annotations

from typing import Any, Callable, Dict, List


class EventBus:
    """Pub/Sub très simple (pas de scopes pour l’instant)."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        self._listeners.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: Any) -> None:
        for h in list(self._listeners.get(event_type, [])):
            h(payload)

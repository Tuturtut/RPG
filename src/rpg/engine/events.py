from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, Dict, List, Tuple


@dataclass(frozen=True)
class Scope:
    kind: str
    id: str | None = None


# Scopes pratiques
GLOBAL = Scope("GLOBAL")
def WORLD(area_id: str) -> Scope: return Scope("WORLD", area_id)
def COMBAT(combat_id: str) -> Scope: return Scope("COMBAT", combat_id)
def DIALOGUE(dialogue_id: str) -> Scope: return Scope("DIALOGUE", dialogue_id)


@dataclass(frozen=True)
class Token:
    scope: Scope
    idx: int


class EventBus:
    """Pub/Sub avec scopes.
    - subscribe(scope, event, handler) -> Token
    - publish(scope, event, payload)
    - close_scope(scope)   # nettoie les listeners de ce scope
    """

    def __init__(self) -> None:
        self._handlers: DefaultDict[Scope, Dict[str, List[Callable[[Any], None]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self._counter = 0
        self._tokens: Dict[Token, Tuple[Scope, str, Callable[[Any], None]]] = {}

    def subscribe(self, scope: Scope, event_type: str, handler: Callable[[Any], None]) -> Token:
        self._handlers[scope][event_type].append(handler)
        tok = Token(scope, self._counter)
        self._tokens[tok] = (scope, event_type, handler)
        self._counter += 1
        return tok

    def publish(self, scope: Scope, event_type: str, payload: Any) -> None:
        # D'abord les handlers GLOBAL, puis ceux du scope ciblé
        for h in list(self._handlers[GLOBAL].get(event_type, [])):
            h(payload)
        for h in list(self._handlers[scope].get(event_type, [])):
            h(payload)

    def unsubscribe(self, token: Token) -> None:
        """Retire le handler inscrit avec ce token (idempotent)."""
        entry = self._tokens.pop(token, None)
        if not entry:
            return  # déjà désinscrit
        scope, event_type, handler = entry
        lst = self._handlers.get(scope, {}).get(event_type, [])
        try:
            lst.remove(handler)
        except ValueError:
            pass  # déjà retiré
        # Nettoyage si la liste (ou le scope) est vide
        if not lst and scope in self._handlers:
            self._handlers[scope].pop(event_type, None)
            if not self._handlers[scope]:
                self._handlers.pop(scope, None)


    def close_scope(self, scope: Scope) -> None:
        # Supprime tous les handlers rattachés à ce scope (utile quand on quitte une zone/écran)
        if scope in self._handlers:
            del self._handlers[scope]
        for t, (s, _, _) in list(self._tokens.items()):
            if s == scope:
                del self._tokens[t]

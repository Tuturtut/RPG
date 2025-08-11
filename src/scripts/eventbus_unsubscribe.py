from rpg.engine.events import EventBus, WORLD

bus = EventBus()
hits: list[str] = []

def handler(p): hits.append(p)

scope = WORLD("village")

tok = bus.subscribe(scope, "E", handler)
bus.publish(scope, "E", {"n": 1})
print(hits)  # [{'n': 1}]

# bus.unsubscribe(tok)
bus.publish(scope, "E", {"n": 2})
print(hits)  # reste [{'n': 1}] -> le handler ne reçoit plus

from rpg.engine.events import EventBus, GLOBAL, WORLD, COMBAT

bus = EventBus()
hits: list[str] = []

bus.subscribe(GLOBAL, "E", lambda p: hits.append("G"))
bus.subscribe(WORLD("forest"), "E", lambda p: hits.append("W-forest"))
bus.subscribe(WORLD("village"), "E", lambda p: hits.append("W-village"))
bus.subscribe(COMBAT("c1"), "E", lambda p: hits.append("C1"))

bus.publish(WORLD("forest"), "E", {})
print(hits)  # ['G', 'W-forest']

hits.clear()
bus.publish(COMBAT("c1"), "E", {})
print(hits)  # ['G', 'C1']

# Nettoyage d'un scope
bus.close_scope(WORLD("forest"))
hits.clear()
bus.publish(WORLD("forest"), "E", {})
print(hits)  # ['G'] (le handler forest a été nettoyé)

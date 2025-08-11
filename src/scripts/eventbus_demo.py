from rpg.engine.events import EventBus

bus = EventBus()
hits = []

def on_move(p): hits.append(("move", p["to"]))
def on_weather(p): hits.append(("weather", p["new"]))

bus.subscribe("NPC_MOVED", on_move)
bus.subscribe("WEATHER_CHANGED", on_weather)

bus.publish("NPC_MOVED", {"to": "forest"})
bus.publish("WEATHER_CHANGED", {"new": "rainy"})
print(hits)  # [('move', 'forest'), ('weather', 'rainy')]

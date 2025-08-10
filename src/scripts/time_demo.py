from rpg.engine.time import GameTime

t = GameTime(day=1, minute=8*60)   # 08:00
print(t)                           # Day 1 08:00
t.advance(30)                      # +30 min
print(t)                           # Day 1 08:30
t.advance(16*60)                   # +16h -> passe minuit
print(t)                           # Day 2 00:30
print("total:", t.total_minutes)   # 60*? -> juste pour voir le compteur

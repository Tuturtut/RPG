from rpg.engine.time import Scheduler, GameTime

hits: list[str] = []
t = GameTime(day=1, minute=8*60)  # 08:00
sched = Scheduler(t)

def ping(): hits.append(f"PING@{t}")
def tea(): hits.append("TEA")

# À 08:10 précises
sched.call_at(8, 10, tea)
# Toutes les 5 minutes (démarre à 08:05)
sched.call_every(5, ping)

# Avançons pas à pas
sched.tick(5)   # -> 08:05 : ping
print(hits)     # ['PING@Day 1 08:05']

sched.tick(5)   # -> 08:10 : tea + ping (ordre garanti par le tas + compteur)
print(hits)     # ['PING@Day 1 08:05', 'TEA', 'PING@Day 1 08:10']

sched.tick(5)   # -> 08:15 : ping
print(hits)     # ['PING@Day 1 08:05', 'TEA', 'PING@Day 1 08:10', 'PING@Day 1 08:15']

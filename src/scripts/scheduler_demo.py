from rpg.engine.time import Scheduler, GameTime

hits = []

def a(): hits.append("A")
def b(): hits.append("B")
def c(): hits.append("C")

sched = Scheduler(GameTime(day=1, minute=8*60))  # 08:00
sched.call_in(10, a)   # 08:10
sched.call_in(5, b)    # 08:05
sched.call_in(15, c)   # 08:15

sched.tick(5)          # -> B
print(hits)            # ['B']
sched.tick(5)          # -> A
print(hits)            # ['B', 'A']
sched.tick(5)          # -> C
print(hits)            # ['B', 'A', 'C']

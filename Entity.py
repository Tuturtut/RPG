class Entity:
    def __init__(self, name, health, damage, defense):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.defense = defense
    
    def __str__(self):
        return f"{self.name} (Health: {self.health}, Damage: {self.damage}, Defense: {self.defense})"
    
    
    def take_damage(self, damage):
        final_damage = max(0, damage - self.defense)
        self.health -= final_damage
        print(f"{self.name} takes {final_damage} damage. Health: {self.health} / {self.max_health}")
        self.after_damage()

    def after_damage(self):
        pass
    
    def attack(self, target):
        print(f"{self.name} attacks {target.name}")
        print(f"\n")
        target.take_damage(self.damage)
    
    def is_alive(self):
        return self.health > 0
    
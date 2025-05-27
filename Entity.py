class Entity:
    def __init__(self, name, health, damage, defense):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.defense = defense
    
    def __str__(self):
        return f"{self.name} {self.health_bar(self.health, self.max_health)}"
    

    def health_bar(self, current, max_hp, length=20):
        filled = int(length * current / max_hp)
        empty = length - filled
        return f"[{'█'*filled}{'░'*empty}] {current}/{max_hp}\n"

    
    def take_damage(self, damage):
        final_damage = max(0, damage - self.defense)
        self.health -= final_damage
        # Affichage des dégâts dans un format lisible
        print(f"{self.name} takes {final_damage} damage!")
        print(self.health_bar(self.health, self.max_health))
        self.after_damage()

    def after_damage(self):
        pass
    
    def attack(self, target):
        print(f"[{self.name} -> {target.name}]")
        target.take_damage(self.damage)
    
    def is_alive(self):
        return self.health > 0
    
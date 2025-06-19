from entities.Human import Human

class Player(Human):
    def __init__(self, name, health, damage, defense, actions=None):
        super().__init__(name, health, damage, defense, actions)

    def getAction(self):
        if self.current_action is not None and self.current_action.rounds_left > 0:
            return self.current_action
        else:
            while True:
                print(f"{self.getName()}, choisissez une action:")
                for i, action in enumerate(self.actions):
                    print(f"{i + 1}. {action.name} - {action.description}")
                try:
                    choice = int(input("Entrez le numéro de l'action: ")) - 1
                    if 0 <= choice < len(self.actions):
                        self.current_action = self.actions[choice]
                        return self.current_action
                    else:
                        print("Choix invalide.")
                except ValueError:
                    print("Veuillez entrer un nombre valide.")

    
    def setTarget(self, enemies):
        if not self.current_action.needsTarget():
            self.current_action.setTarget(None)
            return

        alive_enemies = [
            enemy for enemy in enemies
            if enemy.is_alive() and any(isinstance(enemy, t) for t in self.current_action.valid_target_types)
        ]
        
        if not alive_enemies:
            print("Aucun ennemi vivant.")
            self.current_action.setTarget(None)
            return

        while True:
            print(f"{self.getName()}, choisissez une cible:")
            for i, enemy in enumerate(alive_enemies):
                print(f"{i + 1}. {enemy.getName()} - {enemy.health_bar(enemy.health, enemy.max_health)}")
            try:
                choice = int(input("Entrez le numéro de la cible: ")) - 1
                if 0 <= choice < len(alive_enemies):
                    self.current_action.setTarget(alive_enemies[choice])
                    return
                else:
                    print("Choix invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")


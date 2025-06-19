from core.Game import Game
from world.Area import Area
from world.Events import AreaEvent
from core.GameContext import GameContext
from entities.Human import Human
from entities.Goblin import Goblin
from entities.Player import Player
from actions.AttackAction import AttackAction
from combat.CombatManager import CombatManager
from entities.Entity import Entity

def create_test_area(game):
    maruen = Human("Maruen")
    maruen.languages = ["human"]
    game.dialogue_manager.register(maruen)

    goblin = Goblin("Goblin")
    attack_action = AttackAction("Attaquer", rounds=0, description="Attaque la cible", valid_target_types=[Entity])
    player = Player("Arthur", health=100, damage=40, defense=2, actions=[attack_action])


    auberge = Area("Auberge", "Une petite auberge à l’orée de la forêt.")
    auberge.add_entity(maruen)
    auberge.add_entity(goblin)
    auberge.add_entity(player)

    def fuite_condition(ws, area):
        return ws.weather.current == "rainy"

    def fuite_effet(ws, area):
        print("[Événement] Une fuite s’écoule du plafond.")
        GameContext.journal.add(ws.day, f"Fuite déclenchée dans {area.name}.")
        for entity in area.entities:
            if entity.name == "Maruen":
                entity.mood = "grincheux"
                GameContext.journal.add(ws.day, "Maruen est devenu grincheux.")

    fuite = AreaEvent("fuite_toit", fuite_condition, fuite_effet)
    auberge.add_event(fuite)

    return auberge

def game_loop(game):
    area = game.current_area
    player = [e for e in area.entities if isinstance(e, Player)][0]

    while True:
        print(f"\n=== {game.world.day}e jour — {game.time_manager.get_hours_minutes()} ({game.time_manager.get_time_of_day()}) ===")
        print(f"Zone : {area.name}")
        print("Que veux-tu faire ?")

        print("1. Parler à quelqu’un")
        print("2. Combattre une créature")
        print("3. Attendre une heure")
        print("4. Afficher le journal")
        print("5. Quitter")

        choix = input("→ ")

        if choix == "1":
            for entity in area.entities:
                if entity is not player and hasattr(entity, "get_dialogue"):
                    print(entity.get_dialogue(game.world, observer=player))
            game.wait(5)

        elif choix == "2":
            enemies = [e for e in area.entities if e != player and e.is_alive()]
            if not enemies:
                print("Il n’y a aucun ennemi vivant ici.")
                continue

            for i, enemy in enumerate(enemies):
                print(f"{i + 1}. {enemy.name} ({enemy.health} PV)")

            try:
                i = int(input("Qui veux-tu combattre ? ")) - 1
                if 0 <= i < len(enemies):
                    CombatManager.start(player, [enemies[i]])
                    if not enemies[i].is_alive():
                        area.entities.remove(enemies[i])
                        print(f"{enemies[i].name} a été vaincu.")
                else:
                    print("Choix invalide.")
            except ValueError:
                print("Veuillez entrer un nombre.")

        elif choix == "3":
            game.wait(60)

        elif choix == "4":
            game.journal.show()

        elif choix == "5":
            print("À bientôt.")
            break

        else:
            print("Choix invalide.")

        area.check_events(game.world)

def run():
    game = Game()
    game.world.weather.set_weather("rainy")
    game.world.add_flag("seen_bear")

    area = create_test_area(game)
    game.add_area(area)
    game.change_area(area.name)

    # Affichage initial
    area.describe()
    area.check_events(game.world)

    game_loop(game)


if __name__ == "__main__":
    run()

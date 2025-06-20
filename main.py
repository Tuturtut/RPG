from core.Game import Game
from entities.Player import Player
from entities.Human import Human
from world.Area import Area
from world.Path import Path
from world.PlayerPath import PlayerPath
from events.MapDialogueEvent import MapDialogueEvent
from events.MapFightEvent import MapFightEvent
from dialogue.DialogueManager import DialogueManager
from dialogue.Dialogue import DialogueEntry
from entities.Entity import Entity
from actions.AttackAction import AttackAction

def setup_world(game):
    # ZONES
    auberge = Area("Auberge de Bruneval", "Une auberge rustique au toit moussu.")
    campement = Area("Campement abandonné", "Une tente déchirée et quelques braises encore chaudes.")
    tour = Area("Ancienne Tour", "Un vieux bâtiment en ruine, recouvert de lierre.")
    plaine = Area("Plaine Centrale", "Une étendue vallonnée battue par le vent.", subareas=[auberge, campement, tour])

    # PERSONNAGES
    maruen = Human("Maruen")
    maruen.languages = ["human"]
    maruen_dialogues = [
        DialogueEntry("Rien à signaler.", priority=1),
        DialogueEntry("On raconte qu’un bandit rôde dans les environs…", conditions=["flag == heard_bandit"], priority=5),
        DialogueEntry("Il y a quelques jours, j’ai vu un cerf étrange dans la plaine.", conditions=["weather == sunny"], priority=3),
    ]
    for entry in maruen_dialogues:
        maruen.add_dialogue(entry)
    game.dialogue_manager.register(maruen)

    auberge.add_entity(maruen)

    # JOUEUR
    player = Player("Arthur", health=100, damage=12, defense=6, 
                    actions=[AttackAction("Attaquer", valid_target_types=[Entity])])
    auberge.add_entity(player)
    game.player = player
    game.current_area = plaine

    # PATHS
    path_aub_camp = Path(auberge, campement, steps=4)
    path_camp_tour = Path(campement, tour, steps=3)

    # Événement FIXE : cerf visible au pas 2
    path_aub_camp.events[2] = MapDialogueEvent("Un cerf à la robe blanche surgit d’un bosquet, t’observant longuement.")
    # Événement FIXE : attaque au pas 4

    brigand = Entity("Brigand", health=50, damage=5, defense=2, actions=[AttackAction("Attaquer", valid_target_types=[Entity])])
    path_aub_camp.events[4] = MapFightEvent(brigand)

    # Événements ALÉATOIRES
    path_aub_camp.add_random_event(MapDialogueEvent("Des branches craquent au loin..."), weight=3)
    brigand_affame = Entity("Brigand affamé", health=50, damage=8, defense=2, actions=[AttackAction("Attaquer")])
    path_aub_camp.add_random_event(MapFightEvent(brigand_affame), weight=1)

    return plaine

def run_full_test():
    game = Game()
    game.world.weather.set_weather("sunny")  # météo fixe pour le test
    game.world.add_flag("heard_bandit")      # active un dialogue

    plaine = setup_world(game)

    print(f"Bienvenue dans la région : {plaine.name}")
    while True:
        location = game.player.location
        print(f"\nLieu : {location.getFullName()}")
        print(f"Description : {location.description}")
        print(f"Heure : {game.time_manager.get_hours_minutes()} | Météo : {game.world.weather.current}")

        print("\nPersonnes présentes :")
        for entity in location.entities:
            if entity is not game.player:
                print(f"- {entity.name} : '{entity.get_dialogue(game.world)}'")

        print("\nQue voulez-vous faire ?")
        print("1. Voir les chemins")
        print("2. Se déplacer")
        print("3. Quitter")

        choix = input("→ ")

        if choix == "1":
            if not location.paths:
                print("Aucun chemin ici.")
            else:
                print("Chemins disponibles :")
                for i, (dest, path) in enumerate(location.paths.items()):
                    print(f"{i+1}. Vers {dest.name} ({path.steps} pas)")

        elif choix == "2":
            destinations = list(location.paths.keys())
            if not destinations:
                print("Aucun chemin à emprunter.")
                continue

            print("Vers quelle destination ?")
            for i, dest in enumerate(destinations):
                print(f"{i+1}. {dest.name}")
            try:
                idx = int(input("Choix : ")) - 1
                if 0 <= idx < len(destinations):
                    destination = destinations[idx]
                    path = location.paths[destination]
                    print(f"\n→ Départ pour {destination.name} ({path.steps} pas).")

                    ppath = PlayerPath(path)
                    while True:
                        input("Appuyez sur Entrée pour faire un pas...")
                        if ppath.advance(game):
                            break
                else:
                    print("Choix invalide.")
            except ValueError:
                print("Entrée invalide.")

        elif choix == "3":
            print("Fin de la session.")
            break

        else:
            print("Choix inconnu.")

if __name__ == "__main__":
    run_full_test()

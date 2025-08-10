from core.Journal import Journal
from core.GameController import GameController

class GameContext:

    journal = Journal()
    game_controller = None
    
    def get_game_controller(game):
        if GameContext.game_controller is None:
            GameContext.game_controller = GameController(game)
        return GameContext.game_controller

        


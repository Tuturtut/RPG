import curses
from core.Game import Game
from core.GameController import GameController
from tui.interface.ExplorationContext import ExplorationContext

def startCurses():
    curses.wrapper(main)

def main(stdscr):
    # Initialisation de curses
    curses.curs_set(0)
    stdscr.clear()

    # Init game + controller
    game = Game()
    game.setup()
    controller = GameController(game)

    controller.set_context(ExplorationContext(controller))

    # Dimensions
    height, width = stdscr.getmaxyx()
    info_h, dialogue_h = 7, 7
    zone_h = height - info_h - dialogue_h

    # Fenêtres
    info_win = curses.newwin(info_h, width, 0, 0)
    zone_win = curses.newwin(zone_h, width, info_h, 0)
    dialogue_win = curses.newwin(dialogue_h, width, info_h + zone_h, 0)

    while True:

        # Rendering
        controller.context.render(info_win, zone_win, dialogue_win)

        key = stdscr.getch()
        result = controller.context.handle_input(key)
        if result is "quit":
            controller.last_message = "Sortie du jeu."
            break
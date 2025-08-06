import curses
from core.Game import Game
from core.GameController import GameController
from tui.interface.ExplorationContext import ExplorationContext
import traceback
from utils.debug import log
from core.GameContext import GameContext

def startCurses():
    curses.wrapper(main)

def main(stdscr):

    DEBUG = True

    # Initialisation de curses
    curses.curs_set(0)
    stdscr.clear()

    # Init game + controller
    game = Game()
    game.setup()

    controller = GameContext.get_game_controller(game)
    

    controller.set_context(controller.exploration_context)

    # Dimensions
    height, width = stdscr.getmaxyx()
    info_h, dialogue_h = 7, 7
    zone_h = height - info_h - dialogue_h
    debug_w = width // 2

    # Position
    debug_pos = "left"
    x_pos = 0

    if DEBUG:
        windows_w = width - debug_w
    else:
        windows_w = width

    # Fenêtres
    if DEBUG:
        if debug_pos == "left":
            debug_win = curses.newwin(height, debug_w, 0, 0)
            x_pos = debug_w
        else:
            debug_win = curses.newwin(height, debug_w, 0, windows_w)

    info_win = curses.newwin(info_h, windows_w, 0, x_pos)
    zone_win = curses.newwin(zone_h, windows_w, info_h, x_pos)
    dialogue_win = curses.newwin(dialogue_h, windows_w, info_h + zone_h, x_pos)


    while True:
        try:
            controller.context.render(info_win, zone_win, dialogue_win, debug_win if DEBUG else None)
            key = stdscr.getch()
            result = controller.context.handle_input(key)

            if result == "quit":
                break
        except Exception:
            error_text = traceback.format_exc()
            if DEBUG and debug_win:
                log(error_text)

                debug_win.clear()
                debug_win.box()
                for i, line in enumerate(error_text.splitlines()[-debug_win.getmaxyx()[0]+2:]):
                    try:
                        debug_win.addstr(i + 1, 1, line[:debug_win.getmaxyx()[1]-2])
                    except Exception:
                        pass
                debug_win.refresh()

                while True:
                    key = stdscr.getch()
                    if key == ord("q"):
                        break
            else:
                raise
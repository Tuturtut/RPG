import curses
from core.Game import Game
from core.GameController import GameController

def startCurses():
    curses.wrapper(main)

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    # Init game + controller
    game = Game()
    game.setup()
    controller = GameController(game)

    # Dimensions
    height, width = stdscr.getmaxyx()
    info_h, dialogue_h = 4, 5
    zone_h = height - info_h - dialogue_h

    # Création des fenêtres
    info_win = curses.newwin(info_h, width, 0, 0)
    zone_win = curses.newwin(zone_h, width, info_h, 0)
    dialogue_win = curses.newwin(dialogue_h, width, info_h + zone_h, 0)

    def refresh_all():
        def draw_multiline(win, lines, max_height):
            for i, line in enumerate(lines):
                if i + 1 < max_height - 1:
                    try:
                        win.addstr(i + 1, 2, line)
                    except curses.error:
                        pass  # ignore overflow silently

        info_win.clear(); info_win.box()
        zone_win.clear(); zone_win.box()
        dialogue_win.clear(); dialogue_win.box()

        draw_multiline(info_win, controller.render_game_info().split("\n"), 10)
        draw_multiline(zone_win, controller.render_zone().split("\n"), 10)
        draw_multiline(dialogue_win, controller.render_messages().split("\n"), 10)


        info_win.refresh()
        zone_win.refresh()
        dialogue_win.refresh()

    refresh_all()

    while True:
        key = stdscr.getch()

        if key == ord("q"):
            break
        elif key == ord("r"):
            controller.last_message = "Interface rafraîchie."
            refresh_all()
        elif key in (ord("1"), ord("2"), ord("3"), ord("4"), ord("5")):
            index = key - ord("1")
            controller.move_to(index)
            refresh_all()
        elif key == ord(" "):
            controller.advance_step()
            refresh_all()
import curses

def main(stdscr):
    # Configuration de base
    curses.curs_set(0)  # Masquer le curseur
    stdscr.nodelay(True)  # Ne pas bloquer sur les entrées
    stdscr.timeout(100)   # Attendre 100ms max pour getch()

    # Position initiale du joueur
    y, x = 10, 20

    while True:
        stdscr.clear()

        # Afficher un cadre simple
        stdscr.border()

        # Afficher un personnage
        stdscr.addstr(y, x, "@")

        # Instructions
        stdscr.addstr(0, 2, " Déplace-toi avec les flèches, 'q' pour quitter ")

        stdscr.refresh()

        # Lire la touche appuyée
        key = stdscr.getch()

        if key == ord("q"):
            break
        elif key == curses.KEY_UP:
            y -= 1
        elif key == curses.KEY_DOWN:
            y += 1
        elif key == curses.KEY_LEFT:
            x -= 1
        elif key == curses.KEY_RIGHT:
            x += 1

# Lancer curses avec wrapper (gère bien l’état du terminal)
curses.wrapper(main)

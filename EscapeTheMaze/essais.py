import Maze
from random import randint
import curses
from curses import wrapper
import pygame


def get_key(dictionnaire, valeur):
    for cle, val in dictionnaire.items():
        if val == valeur:
            return cle
    return None


def item_teleportation(laby: Maze):
    items = {(randint(2, laby.width - 5), randint(2, laby.height - 2)): "O",
             (randint(2, laby.width - 2), randint(2, laby.height - 2)): "O"}
    return items


def teleportation(joueur: dict, portail: dict):
    posJoueur = list(joueur.keys())[0]
    posPortails = list(portail.keys())

    for posPortail in posPortails:
        if posJoueur == posPortail:
            # Trouver l'autre portail qui n'est pas à la position du joueur
            autrePortail = [pos for pos in posPortails if pos != posJoueur]
            if autrePortail:  # Vérifier si la liste n'est pas vide
                # Échanger les positions du joueur et de l'autre portail
                joueur[autrePortail[0]] = joueur.pop(posJoueur)
                break

    return joueur


def deplacement(joueur: dict, laby: Maze, key) -> dict:
    cleJoueur = get_key(joueur, "#")
    if key == curses.KEY_DOWN and (cleJoueur[0] + 1, cleJoueur[1]) in laby.get_reachable_cells(cleJoueur):
        cleJoueur = (cleJoueur[0] + 1, cleJoueur[1])

    elif key == curses.KEY_RIGHT and (cleJoueur[0], cleJoueur[1] + 1) in laby.get_reachable_cells(cleJoueur):
        cleJoueur = (cleJoueur[0], cleJoueur[1] + 1)

    elif key == curses.KEY_UP and (cleJoueur[0] - 1, cleJoueur[1]) in laby.get_reachable_cells(cleJoueur):
        cleJoueur = (cleJoueur[0] - 1, cleJoueur[1])

    elif key == curses.KEY_LEFT and (cleJoueur[0], cleJoueur[1] - 1) in laby.get_reachable_cells(cleJoueur):
        cleJoueur = (cleJoueur[0], cleJoueur[1] - 1)

    joueur = {cleJoueur: "#"}
    return joueur


def lancement_jeu(stdscr):
    pygame.mixer.init()

    # Charge la musique
    pygame.mixer.music.load("intro.mp3")

    # Joue la musique
    pygame.mixer.music.play()

    # Attend que la musique soit lancée
    while pygame.mixer.get_busy():
        pass

    # Texte à afficher
    lines = [" _____                       _____ _         ___  ___              ",
             "|  ___|                     |_   _| |        |  \/  |              ",
             "| |__ ___  ___ __ _ _ __   ___| | | |__   ___| .  . | __ _ _______ ",
             "|  __/ __|/ __/ _` | '_ \ / _ \ | | '_ \ / _ \ |\/| |/ _` |_  / _ \"",
             "| |__\__ \ (_| (_| | |_) |  __/ | | | | |  __/ |  | | (_| |/ /  __/",
             "\____/___/\___\__,_| .__/ \___\_/ |_| |_|\___\_|  |_/\__,_/___\___|",
             "                   | |                                             ",
             "                   |_|                                             ",
             "                                                                   ",
             "         Appuyer sur une touche pour démarrer le jeu "]

    # Affichage du texte
    for i, line in enumerate(lines):
        stdscr.addstr(i + 5, 5, line)  # Ajoute 1 pour la bordure

    stdscr.refresh()

    stdscr.getch()  # Attend une entrée de l'utilisateur


def menu(stdscr):
    res = ""
    stdscr.clear()
    lines = [" _   _            _ _ _                _           _   _                              ",
             "| | | |          (_) | |              | |         | | (_)                             ",
             "| | | | ___ _   _ _| | | ___ ____  ___| | ___  ___| |_ _  ___  _ __  _ __   ___ _ __  ",
             "| | | |/ _ \ | | | | | |/ _ \_  / / __| |/ _ \/ __| __| |/ _ \| '_ \| '_ \ / _ \ '__| ",
             "\ \_/ /  __/ |_| | | | |  __// /  \__ \ |  __/ (__| |_| | (_) | | | | | | |  __/ |    ",
             " \___/ \___|\__,_|_|_|_|\___/___| |___/_|\___|\___|\__|_|\___/|_| |_|_| |_|\___|_|    ",
             "                                   _            _          _                          ",
             "                                  | |          | |        (_)              _          ",
             " _   _ _ __    _ __ ___   ___   __| | ___    __| | ___     _  ___ _   _   (_)         ",
             "| | | | '_ \  | '_ ` _ \ / _ \ / _` |/ _ \  / _` |/ _ \   | |/ _ \ | | |              ",
             "| |_| | | | | | | | | | | (_) | (_| |  __/ | (_| |  __/   | |  __/ |_| |   _          ",
             " \__,_|_| |_| |_| |_| |_|\___/ \__,_|\___|  \__,_|\___|   | |\___|\__,_|  (_)         ",
             "                                                         _/ |                         ",
             "                                                        |__/                          ",
             "                                                                                      ",
             " Facile : Appuyer sur F   |   Moyen : Appuyez sur M   |   Difficile : Appuyez sur D   "]

    for i, line in enumerate(lines):
        stdscr.addstr(i + 5, 5, line)  # Ajoute 5 pour la bordure

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('f') or key == ord('F'):
            res = chr(key).lower()  # Convertit la touche pressée en minuscule
            break
        elif key == ord('m') or key == ord('M'):
            res = chr(key).lower()
            break
        elif key == ord('d') or key == ord('D'):
            res = chr(key).lower()
            break
    return res


def felicitation(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    ROUGE = curses.color_pair(1)
    curses.init_color(2, 1000, 0, 0)
    ORANGE = curses.color_pair(1)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    JAUNE = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    VERT = curses.color_pair(4)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    BLEU = curses.color_pair(5)

    stdscr.clear()

    stdscr.addstr(5, 5, " _____                             _  _  _  ", ROUGE)
    stdscr.addstr(6, 5, "/  ___|                           | || || | ", ROUGE)
    stdscr.addstr(7, 5, "\ `--.  _   _  _ __    ___  _ __  | || || | ", ORANGE)
    stdscr.addstr(8, 5, " `--. \| | | || '_ \  / _ \| '__| | || || | ", JAUNE)
    stdscr.addstr(9, 5, "/\__/ /| |_| || |_) ||  __/| |    |_||_||_| ", VERT)
    stdscr.addstr(10, 5, "\____/  \__,_|| .__/  \___||_|    (_)(_)(_) ", BLEU)
    stdscr.addstr(11, 5, "              | |                           ", BLEU)
    stdscr.addstr(12, 5, "              |_|                           ", BLEU)

    stdscr.refresh()
    stdscr.getch()

def niveau_facile(stdscr):
    laby = Maze.Maze.gen_sidewinder(15, 15)
    cellDebut = (0, 0)
    cellFin = (laby.width - 1, laby.height - 1)
    JOUEUR = {cellDebut: "#"}

    final = JOUEUR.copy()

    stdscr.clear()
    stdscr.addstr(laby.overlay(final))
    while get_key(JOUEUR, "#") != cellFin:
        key = stdscr.getch()
        JOUEUR = deplacement(JOUEUR, laby, key)

        final = JOUEUR.copy()
        stdscr.clear()
        stdscr.addstr(laby.overlay(final))
        stdscr.refresh()
    stdscr.clear()
    felicitation(stdscr)

def main(stdscr):
    stdscr.clear()

    # Appelle la fonction pour afficher le texte
    lancement_jeu(stdscr)
    stdscr.getch()

    key = menu(stdscr)
    if key == 'f':
        niveau_facile(stdscr)
    if key == 'm':
        print("Hello World!")
    if key == 'd':
        print("Bonjour Monde!")

    stdscr.refresh()

wrapper(main)

def item_solution(laby: Maze):
    return {(randint(2, laby.width - 5), randint(2, laby.height - 5)): "$"}


def solution(laby: Maze, joueur: dict) -> dict:
    cellFin = (laby.width - 1, laby.height - 1)
    posJoueur = list(joueur.keys())[0]
    solution = laby.solve_dfs(posJoueur, cellFin)
    str_solution = {c: '*' for c in solution}
    return str_solution

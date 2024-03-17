import time
import Maze
from random import randint
import curses
from curses import wrapper
import pygame


def get_key(dictionnaire: dict, valeur: str):
    """
    Fonction qui permet de retourner la clé du dictionnaire passé en paramètre avec sa valeur associée (valeur)
    Retour :
        Retourne un tuple
    """
    for cle, val in dictionnaire.items():
        if val == valeur:
            return cle
    return None


def item_teleportation(laby : Maze) -> dict:
    """
    Fonction qui permet de créer les portails de téléportation du labyrinthe.
    Le 1er portail sera toujours dans la partie supérieure gauche du labyrinthe
    et le 2ᵉ portail sera toujours dans la partie inférieure droite du labyrinthe
    Retour :
        Retourne un dictionnaire des deux portails
    """
    items = {(randint(2, 5), randint(2, 5)): "O",
             (randint(8, 8), randint(8, 8)): "O"}
    return items


def teleportation(joueur: dict, portail: dict) -> dict:
    """
    Fonction qui permet de téléporter le joueur passé en paramètre aux coordonnées du deuxième portail
    Retour :
        Retourne le nouveau joueur (ses nouvelles coordonnées)
    """
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


def item_generation(laby: Maze) -> dict:
    """
    Fonction qui permet de créer l'item qui va servir de regénération du labyrinthe
    Quand le joueur marchera dessus, un nouveau labyrinthe sera généré
    Retour :
        Retourne un dictionnaire avec pour clé ses coordonnées et pour valeur son character qui le représente "@"
    """
    return {(randint(0, laby.width), randint(0, laby.height)): "@"}


def item_solution(laby: Maze, col: int) -> dict:
    """
    Fonction qui permet de créer l'item qui affichera la solution du labyrinthe
    Retour :
        Retourne un dictionnaire avec pour clé ses coordonnées et pour valeur son character qui le représente "$"
    """
    return {(randint(0, laby.width), randint(0, laby.height - col)): "$"}


def solution(laby: Maze, joueur: dict, cellFin: tuple) -> dict:
    """
    Fonction qui permet d'afficher le chemin entre le joueur passé en paramètre
    et la cellule de fin du labyrinthe passé en paramètre
    Retour :
        Retourne un dictionnaire contenant le chemin
    """
    posJoueur = list(joueur.keys())[0]
    solution = laby.solve_dfs(posJoueur, cellFin)
    str_solution = {c: '*' for c in solution}
    return str_solution


def deplacement(joueur: dict, laby: Maze, key: int) -> dict:
    """"
    Fonction qui permet de changer la clé du joueur passé en paramètre
    en fonction de la direction qu'il a choisi en appuyant sur les flèches directionnelles
    Retour :
        Retourne le nouveau dictionnaire du joueur passé en paramètre
    """
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


def lancement_jeu(stdscr: curses.window) -> None:
    """
    Fonction qui permet d'afficher le lancement du jeu
    Retour :
        Ne retourne rien
    """

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
    return None


def menu(stdscr: curses.window) -> str:
    """
    Affiche le menu du jeu et renvoie la touche appuyée par l'utilisateur
    Retour :
        Retourne la touche appuyée par l'utilisateur sous la forme d'une chaîne de caractères
    """
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
             " Facile : Appuyer sur F   |   Moyen : Appuyez sur M   |   Difficile : Appuyez sur D   ",
             "                                                                                      ",
             "                  Si vous souhaitez quitter le jeu, appuyez sur Q                     "]

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
        elif key == ord('q') or key == ord('Q'):
            res = chr(key).lower()
            break
    return res


def felicitation(stdscr: curses.window, niveau: callable) -> str:
    """
    Affiche le méssage de fin du labyrinthe et permet à l'utilisateur de choisir
    s'il veut recommencer le niveau ou bien retourner au menu
    Retour :
        Retourne la touche appuyée par l'utilisateur sous forme de chaîne de caractères
    """
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    ROUGE = curses.color_pair(1)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    JAUNE = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    VERT = curses.color_pair(4)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    BLEU = curses.color_pair(5)

    stdscr.clear()

    stdscr.addstr(5, 5, " _____                             _  _  _  ", ROUGE)
    stdscr.addstr(6, 5, "/  ___|                           | || || | ", ROUGE)
    stdscr.addstr(7, 5, "\ `--.  _   _  _ __    ___  _ __  | || || | ", ROUGE)
    stdscr.addstr(8, 5, " `--. \| | | || '_ \  / _ \| '__| | || || | ", JAUNE)
    stdscr.addstr(9, 5, "/\__/ /| |_| || |_) ||  __/| |    |_||_||_| ", VERT)
    stdscr.addstr(10, 5, "\____/  \__,_|| .__/  \___||_|    (_)(_)(_) ", BLEU)
    stdscr.addstr(11, 5, "              | |                           ", BLEU)
    stdscr.addstr(12, 5, "              |_|                           ", BLEU)
    stdscr.addstr(14, 5, "Appuyez sur R pour relancer une partie")
    stdscr.addstr(15, 5, "Appuyez sur M pour retourner au menu")

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('r') or key == ord('R'):
            res = "r"
            niveau(stdscr)
            break
        if key == ord('m') or key == ord('M'):
            res = "m"
            break
    return res


def niveau_facile(stdscr: curses.window) -> str:
    """
    Fonction du déroulement du niveau facile
    Retour :
        Retourne la touche appuyée par l'utilisateur lors de la fonction felicitation()
    """
    pygame.mixer.init()
    pygame.mixer.music.load("musiques/facile.mp3")
    sonArrivee = pygame.mixer.Sound("musiques/arrivee.mp3")
    pygame.mixer.music.play(-1)
    while pygame.mixer.get_busy():
        pass

    laby = Maze.Maze.gen_btree(15, 15)
    cellDebut = (0, 0)
    cellFin = (laby.width - 1, laby.height - 1)
    JOUEUR = {cellDebut: "#"}
    ARRIVE = {cellFin: "§"}
    PORTAIL = item_teleportation(laby)
    RANDOM = item_generation(laby)
    SOLUTION = item_solution(laby, 7)
    compteur = 0
    flagGen = 0
    flagSol = 0

    final = JOUEUR.copy()
    final.update(ARRIVE)
    final.update(PORTAIL)
    final.update(RANDOM)
    final.update(SOLUTION)

    stdscr.clear()
    stdscr.addstr(laby.overlay(final))
    while get_key(JOUEUR, "#") != cellFin:

        key = stdscr.getch()
        JOUEUR = deplacement(JOUEUR, laby, key)

        final = JOUEUR.copy()
        final.update(ARRIVE)
        final.update(PORTAIL)

        if get_key(JOUEUR, "#") == get_key(PORTAIL, "O"):
            JOUEUR = teleportation(JOUEUR, PORTAIL)

        if get_key(JOUEUR, "#") == get_key(RANDOM, "@"):
            laby = laby.gen_btree(15, 15)
            del final[get_key(RANDOM, "@")]
            RANDOM[get_key(RANDOM, "@")] = "/"
            flagGen = 1

        elif flagGen == 0:
            final.update(RANDOM)

        if get_key(JOUEUR, "#") == get_key(SOLUTION, "$"):
            SOLUTION = solution(laby, JOUEUR, cellFin)
            final.update(SOLUTION)
            stdscr.clear()
            stdscr.addstr(laby.overlay(final))
            stdscr.refresh()
            start_time = time.time()
            while time.time() - start_time < 2:
                pass
            flagSol = 1

        elif flagSol == 0:
            final.update(SOLUTION)

        final.update(JOUEUR)

        stdscr.clear()
        stdscr.addstr(laby.overlay(final))
        stdscr.refresh()  # Rafraîchir l'affichage après chaque mise à jour
        compteur += 1

    pygame.mixer.music.stop()
    sonArrivee.play()
    stdscr.addstr(laby.height * 2 + 2, 14, f"Vous avez réussis en {compteur} coups !!!")
    stdscr.addstr(laby.height * 2 + 3, 7, f"Le nombre minimal de coup était de : {laby.distance_geo(cellDebut, cellFin)} coups")
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()
    res = felicitation(stdscr, niveau_facile)
    return res


def niveau_moyen(stdscr: curses.window) -> str:
    """
    Fonction du déroulement du niveau moyen
    Retour :
        Retourne la touche appuyée par l'utilisateur lors de la fonction felicitation()
    """
    pygame.mixer.init()
    pygame.mixer.music.load("musiques/moyen.mp3")
    pygame.mixer.music.play(-1)
    while pygame.mixer.get_busy():
        pass

    laby = Maze.Maze.gen_fusion(15, 15)
    cellDebut = (0, 0)
    cellFin = (laby.width - 1, laby.height - 1)
    JOUEUR = {cellDebut: "#"}
    ARRIVE = {cellFin: "§"}
    PORTAIL = item_teleportation(laby)
    RANDOM = item_generation(laby)
    SOLUTION = item_solution(laby, 7)
    sonArrivee = pygame.mixer.Sound("musiques/arrivee.mp3")
    compteur = 0
    flagGen = 0
    flagSol = 0

    final = JOUEUR.copy()
    final.update(ARRIVE)
    final.update(PORTAIL)
    final.update(RANDOM)
    final.update(SOLUTION)

    stdscr.clear()
    stdscr.addstr(laby.overlay(final))
    while get_key(JOUEUR, "#") != cellFin:

        key = stdscr.getch()
        JOUEUR = deplacement(JOUEUR, laby, key)

        final = JOUEUR.copy()
        final.update(ARRIVE)
        final.update(PORTAIL)

        if get_key(JOUEUR, "#") == get_key(PORTAIL, "O"):
            JOUEUR = teleportation(JOUEUR, PORTAIL)

        if get_key(JOUEUR, "#") == get_key(RANDOM, "@"):
            laby = laby.gen_fusion(15, 15)
            del final[get_key(RANDOM, "@")]
            RANDOM[get_key(RANDOM, "@")] = "/"
            flagGen = 1

        elif flagGen == 0:
            final.update(RANDOM)

        if get_key(JOUEUR, "#") == get_key(SOLUTION, "$"):
            SOLUTION = solution(laby, JOUEUR, cellFin)
            final.update(SOLUTION)
            stdscr.clear()
            stdscr.addstr(laby.overlay(final))
            stdscr.refresh()
            start_time = time.time()
            while time.time() - start_time < 1:
                pass
            flagSol = 1

        elif flagSol == 0:
            final.update(SOLUTION)

        final.update(JOUEUR)

        stdscr.clear()
        stdscr.addstr(laby.overlay(final))
        stdscr.refresh()  # Rafraîchir l'affichage après chaque mise à jour
        compteur += 1

    pygame.mixer.music.stop()
    sonArrivee.play()
    stdscr.addstr(laby.height * 2 + 2, 14, f"Vous avez réussis en {compteur} coups !!!")
    stdscr.addstr(laby.height * 2 + 3, 7, f"Le nombre minimal de coup était de : {laby.distance_geo(cellDebut, cellFin)} coups")
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()
    res = felicitation(stdscr, niveau_moyen)
    return res


def niveau_difficile(stdscr: curses.window) -> str:
    """
    Fonction du déroulement du niveau difficile
    Retour :
        Retourne la touche appuyée par l'utilisateur lors de la fonction felicitation()
    """
    pygame.mixer.init()
    pygame.mixer.music.load("musiques/difficile.mp3")
    pygame.mixer.music.play(-1)
    while pygame.mixer.get_busy():
        pass

    laby = Maze.Maze.gen_wilson(17, 17)
    cellDebut = (0, 0)
    cellFin = (laby.width - 1, laby.height - 1)
    JOUEUR = {cellDebut: "#"}
    ARRIVE = {cellFin: "§"}
    PORTAIL = item_teleportation(laby)
    RANDOM = item_generation(laby)
    SOLUTION = item_solution(laby, 7)
    sonArrivee = pygame.mixer.Sound("musiques/arrivee.mp3")
    compteur = 0
    flagGen = 0
    flagSol = 0

    final = JOUEUR.copy()
    final.update(ARRIVE)
    final.update(PORTAIL)
    final.update(RANDOM)
    final.update(SOLUTION)

    stdscr.clear()
    stdscr.addstr(laby.overlay(final))
    while get_key(JOUEUR, "#") != cellFin:

        key = stdscr.getch()
        JOUEUR = deplacement(JOUEUR, laby, key)

        final = JOUEUR.copy()
        final.update(ARRIVE)
        final.update(PORTAIL)

        if get_key(JOUEUR, "#") == get_key(PORTAIL, "O"):
            JOUEUR = teleportation(JOUEUR, PORTAIL)

        if get_key(JOUEUR, "#") == get_key(RANDOM, "@"):
            laby = laby.gen_wilson(17, 17)
            del final[get_key(RANDOM, "@")]
            RANDOM[get_key(RANDOM, "@")] = "/"
            flagGen = 1

        elif flagGen == 0:
            final.update(RANDOM)

        if get_key(JOUEUR, "#") == get_key(SOLUTION, "$"):
            SOLUTION = solution(laby, JOUEUR, cellFin)
            final.update(SOLUTION)
            stdscr.clear()
            stdscr.addstr(laby.overlay(final))
            stdscr.refresh()
            start_time = time.time()
            while time.time() - start_time < 0.7:
                pass
            flagSol = 1

        elif flagSol == 0:
            final.update(SOLUTION)

        final.update(JOUEUR)

        stdscr.clear()
        stdscr.addstr(laby.overlay(final))
        stdscr.refresh()  # Rafraîchir l'affichage après chaque mise à jour
        compteur += 1

    pygame.mixer.music.stop()
    sonArrivee.play()
    stdscr.addstr(laby.height * 2 + 2, 14, f"Vous avez réussis en {compteur} coups !!!")
    stdscr.addstr(laby.height * 2 + 3, 7, f"Le nombre minimal de coup était de : {laby.distance_geo(cellDebut, cellFin)} coups")
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()
    res = felicitation(stdscr, niveau_difficile)
    return res


def main(stdscr: curses.window) -> None:
    """
    Fonction principale du jeu qui est lancée quand le joueur lance le programme
    Retour :
        Ne retourne rien
    """
    quitter = False
    result = ""
    pygame.mixer.init()
    pygame.mixer.music.load("musiques/intro.mp3")
    pygame.mixer.music.play(-1)
    while pygame.mixer.get_busy():
        pass

    lancement_jeu(stdscr)
    stdscr.getch()

    while not quitter:

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("musiques/intro.mp3")
            pygame.mixer.music.play(-1)
        stdscr.clear()

        key = menu(stdscr)
        if key == 'f':
            result = niveau_facile(stdscr)
        elif key == 'm':
            result = niveau_moyen(stdscr)
        elif key == 'd':
            result = niveau_difficile(stdscr)
        elif key == 'q':
            quitter = True

        # Si la partie est terminée et l'utilisateur souhaite revenir au menu
        if result == 'm':
            continue  # Revenir au menu

    stdscr.refresh()
    return None


wrapper(main)

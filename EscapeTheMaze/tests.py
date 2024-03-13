import curses
from curses import wrapper
from random import randint
import pygame
import Maze
import time

def lancement_jeu():
    affichage = """
    _____                       _____ _         ___  ___              
   |  ___|                     |_   _| |        |  \/  |              
   | |__ ___  ___ __ _ _ __   ___| | | |__   ___| .  . | __ _ _______ 
   |  __/ __|/ __/ _` | '_ \ / _ \ | | '_ \ / _ \ |\/| |/ _` |_  / _ \\
   | |__\__ \ (_| (_| | |_) |  __/ | | | | |  __/ |  | | (_| |/ /  __/
   \____/___/\___\__,_| .__/ \___\_/ |_| |_|\___\_|  |_/\__,_/___\___|
                      | |                                             
                      |_|                                             
    """
    return affichage

def fin():
    affichage = """
    
______                       _ 
| ___ \                     | |
| |_/ /_ __ __ ___   _____  | |
| ___ \ '__/ _` \ \ / / _ \ | |
| |_/ / | | (_| |\ V / (_) ||_|
\____/|_|  \__,_| \_/ \___/ (_)
                                                                                                                                 
"""
    return affichage

def get_key(dictionnaire, valeur):
    for cle, val in dictionnaire.items():
        if val == valeur:
            return cle
    return None

def supprimer_enregistrements(dictionnaire, valeur):
    clefs_a_supprimer = [clef for clef, val in dictionnaire.items() if val == valeur]
    for clef in clefs_a_supprimer:
        del dictionnaire[clef]
    return dictionnaire


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

def item_teleportation(laby: Maze):
    items = {(randint(2, laby.width - 5), randint(2, laby.height - 2)): "O",
            (randint(2, laby.width - 2), randint(2, laby.height - 2)): "o"}
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

def item_solution(laby: Maze):
    return {(randint(2, laby.width - 5), randint(2, laby.height - 5)): "$"}

def solution(laby: Maze, joueur: dict) -> dict:
    cellFin = (laby.width - 1, laby.height - 1)
    posJoueur = list(joueur.keys())[0]
    solution = laby.solve_dfs(posJoueur, cellFin)
    str_solution = {c: '*' for c in solution}
    return str_solution

def main(stdscr):
    pygame.mixer.init()
    pygame.mixer.music.load("musiques/intro.mp3")
    laby = Maze.Maze.gen_wilson(7, 7)
    cellDebut = (0, 0)
    cellFin = (laby.width-1, laby.height-1)

    JOUEUR = {cellDebut: "#"}
    PORTAIL = item_teleportation(laby)
    SOLUTION = item_solution(laby)
    pygame.mixer.music.play(-1)

    stdscr.clear()

    # Afficher le texte de lancement
    lancement_texte = lancement_jeu()
    stdscr.addstr(10, 50, lancement_texte)
    stdscr.getch()

    final = JOUEUR.copy()
    final.update(PORTAIL)
    final.update(SOLUTION)

    stdscr.clear()
    stdscr.addstr(laby.overlay(final))
    while get_key(JOUEUR, "#") != cellFin:

        key = stdscr.getch()
        JOUEUR = deplacement(JOUEUR, laby, key)

        final = JOUEUR.copy()
        final.update(PORTAIL)
        final.update(SOLUTION)
        stdscr.addstr(laby.overlay(final))

        if get_key(JOUEUR, "#") == get_key(SOLUTION, '$'):
            SOLUTION = solution(laby, JOUEUR)
            final.update(SOLUTION)
            stdscr.clear()
            stdscr.addstr(laby.overlay(final))
            stdscr.refresh()
            time.sleep(0.7)  # Attendre 1 seconde avant de continuer

        supprimer_enregistrements(final, "*")
        final.update(JOUEUR)

        stdscr.clear()
        stdscr.addstr(laby.overlay(final))
        stdscr.refresh()

    stdscr.clear()
    finA = fin()
    stdscr.addstr(finA)
    stdscr.getch()

pygame.init()
wrapper(main)

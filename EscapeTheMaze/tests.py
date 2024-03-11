import curses
from curses import wrapper
import pygame
import Maze


def get_key(dictionnaire, valeur):
    for cle, val in dictionnaire.items():
        if val == valeur:
            return cle
    return None

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

def main(stdscr):
    pygame.mixer.init()
    pygame.mixer.music.load("intro.mp3")
    laby = Maze.Maze.gen_wilson(10, 10)
    cellDebut = (0, 0)
    cellFin = (laby.width-1, laby.height-1)

    joueur = {cellDebut: "#"}
    pygame.mixer.music.play(-1)
    stdscr.addstr(laby.overlay(joueur))
    while get_key(joueur, "#") != cellFin:
        key = stdscr.getch()
        joueur = deplacement(joueur, laby, key)
        stdscr.clear()
        stdscr.addstr(laby.overlay(joueur))
        stdscr.refresh()

pygame.init()
wrapper(main)
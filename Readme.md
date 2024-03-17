# Escape the Maze

VIDAL Martin

## Description du projet

"Escape the Maze" est un jeu issue d'une SAE autour des graphes et plus précisément des labyrinthes où le joueur doit naviguer à travers un labyrinthe complexe pour atteindre la sortie.

## Installation

Pour installer le jeu, suivez ces étapes :
1. Clonez ce dépôt sur votre machine locale.
2. Installez les dépendances nécessaires mentionnées dans la section "Prérequis".

## Prérequis

- La bibliothèque Pygame 2.5.2
- Le module Curses de Python
- Être en python 3.10

Pour installer ces différentes librairies : 

Faire attention de bien se situer dans le répertoire du projet :

    Windows : `cd .\votreChemin\SAE_labyrinthes`

    Linux : `cd /votreChemin/SAE_labyrinthes`

Installation Pygame :

    Windows : `python -m pip install pygame`

    Linux :  `sudo apt-get install python3-pip`
             `sudo pip3 install -update pip`
             `sudo pip3 install -update pip`
             `sudo pip3 install pygame`

Pour vérifier que Pygame est bien installé tapez **`python`** si vous êtes sur Windows ou bien **`python3`** si vous êtes sur Linux dans votre terminal.

Ensuite, tapez **`import pygame`**

Si vous obtenez ces lignes : 

```
pygame 2.5.2 (SDL 2.28.3, Python 3.10.0)
Hello from the pygame community. https://www.pygame.org/contribute.html
```
Pygame est bien installé.


Maintenant, pour installer curses, il suffit de taper la commande suivante :

```
pip install window-curses
```

**Dernière étape, configurer l'interpréteur python du projet en version 3.10**

Lien pour l'Installation : ![](https://www.python.org/downloads/release/python-3100/)


## Comment jouer
1. Ouvrez un terminal dans le dossier "Escape the Maze".
2. Mettez le terminal en plein écran.
3. Exécutez la ligne suivante : `python ./play.py`

Si vous êtes sur Linux, vous aurez probablement besoin d'exécuter `python3 ./play.py` à la place.

**IMPORTANT** : 

Si vous avez une erreur de ce type : 

```
_curses.error: addwstr() returned ERR
```

C'est que la fenêtre de votre terminal est trop petite. Une fois agrandie, rechargez votre terminal en le fermant et en le réouvrant.

## Contribution
Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request si vous souhaitez contribuer.

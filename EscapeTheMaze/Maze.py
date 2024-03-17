from random import *


class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l, c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """

    def __init__(self, height, width):
        """
        Constructeur d'un labyrinthe de height cellules de haut
        et de width cellules de large
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height = height
        self.width = width
        self.neighbors = {(i, j): set() for i in range(height) for j in range(width)}

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour déboguer)
        Retour :
            chaîne (string) : description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors) + "\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour :
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += "   ┃" if (0, j + 1) not in self.neighbors[(0, j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i + 1, j + 1) not in self.neighbors[(i + 1, j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def add_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Cette méthode permet d'ajouter un mur entre la cellule c1 et la cellule c2
        Retour :
            Ne retourne rien
        """
        self.neighbors[c1].remove(c2)
        self.neighbors[c2].remove(c1)
        return None

    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Cette méthode permet de retirer un mur entre la cellule c1 et la cellule c2
        Retour :
            Ne retourne rien
        """
        self.neighbors[c1].add(c2)
        self.neighbors[c2].add(c1)
        return None

    def get_cells(self) -> list:
        """
        Méthode qui permet d'avoir une liste de toutes les cellules qui composent le labyrinthe
        Retour :
            Retourne une liste de tuples
        """
        liste = []
        for i in range(self.height):
            for j in range(self.width):
                liste.append((i, j))
        return liste

    def get_walls(self) -> list:
        """
        Méthode qui permet d'avoir une liste de tous les murs qui composent le labyrinthe
        Retour :
            Retourne une liste de tuples de cellules
        Exemple :
            [[(0, 0), (0, 1)], [(0, 1), (1, 1)]]
        """
        liste = []
        for i in range(self.height):
            for j in range(self.width):
                if j + 1 < self.width and (i, j + 1) not in self.neighbors[(i, j)]:
                    liste.append([(i, j), (i, j + 1)])
                if i + 1 < self.height and (i + 1, j) not in self.neighbors[(i, j)]:
                    liste.append([(i, j), (i + 1, j)])
        return liste

    def fill(self) -> None:
        """
        Méthode qui permet d'ajouter tous les murs possibles dans le labyrinthe
        Retour :
            Ne retourne rien
        """
        for i in range(self.height):
            for j in range(self.width):
                if j + 1 < self.width and (i, j + 1) in self.neighbors[(i, j)]:
                    self.add_wall((i, j), (i, j + 1))
                if i + 1 < self.height and (i + 1, j) in self.neighbors[(i, j)]:
                    self.add_wall((i, j), (i + 1, j))
        return None

    def empty(self) -> None:
        """
        Méthode qui supprime tous les murs du labyrinthe
        Retour :
            Ne retourne rien
        """
        for i in range(self.height):
            for j in range(self.width):
                if j + 1 < self.width and (i, j + 1) not in self.neighbors[(i, j)]:
                    self.remove_wall((i, j), (i, j + 1))
                if i + 1 < self.height and (i + 1, j) not in self.neighbors[(i, j)]:
                    self.remove_wall((i, j), (i + 1, j))
        return None

    def get_contiguous_cells(self, c: tuple) -> list:
        """
        Méthode qui permet d'avoir une liste des cellules contiguës et dans la grille à la cellule passée en paramètre
        Retour :
            Retourne une liste de tuples
        """
        liste = []
        (i, j) = c
        if j - 1 >= 0:
            liste.append((i, j - 1))
        if i - 1 >= 0:
            liste.append((i - 1, j))
        if j + 1 < self.width:
            liste.append((i, j + 1))
        if i + 1 < self.height:
            liste.append((i + 1, j))
        return liste

    def get_reachable_cells(self, c: tuple) -> list:
        """
        Méthode qui permet d'avoir une liste des cellules accessibles dans la grille
        depuis la cellule c passée en paramètre
        Retour :
            Retourne une liste de tuples
        """
        liste = []
        (i, j) = c
        if j - 1 >= 0 and (i, j - 1) in self.neighbors[(i, j)]:
            liste.append((i, j - 1))
        if i - 1 >= 0 and (i - 1, j) in self.neighbors[(i, j)]:
            liste.append((i - 1, j))
        if j + 1 < self.width and (i, j + 1) in self.neighbors[(i, j)]:
            liste.append((i, j + 1))
        if i + 1 < self.height and (i + 1, j) in self.neighbors[(i, j)]:
            liste.append((i + 1, j))
        return liste

    @classmethod
    def gen_btree(cls, h: int, w: int) -> 'Maze':
        """
        Méthode de classe qui permet de générer un labyrinthe selon l'algorithme de génération par arbre binaire
        Retour :
            Retourne le labyrinthe généré
        """
        laby = Maze(h, w)
        for i in range(laby.height):
            for j in range(laby.width):
                ACTUEL = (i, j)
                EST = (i, j + 1)
                SUD = (i + 1, j)
                if j + 1 < laby.width and i + 1 < laby.height:
                    if 0 == randint(0, 1):
                        laby.remove_wall(ACTUEL, SUD)
                    else:
                        laby.remove_wall(ACTUEL, EST)
                elif j + 1 >= laby.width and i + 1 < laby.height:
                    laby.remove_wall(ACTUEL, SUD)
                elif i + 1 >= laby.height and j + 1 < laby.width:
                    laby.remove_wall(ACTUEL, EST)
        return laby

    @classmethod
    def gen_sidewinder(cls, h: int, w: int) -> 'Maze':
        """
        Méthode de classe qui permet de générer un labyrinthe selon l'algorithme SideWinder
        Retour :
            Retourne le labyrinthe généré
        """
        laby = Maze(h, w)

        for i in range(laby.height - 1):
            sequence = []
            for j in range(laby.width - 1):
                sequence.append((i, j))
                if randint(0, 1) == 0:
                    laby.remove_wall((i, j), (i, j + 1))
                else:
                    murACasser = choice(sequence)
                    laby.remove_wall(murACasser, (murACasser[0] + 1, murACasser[1]))  # On casse le mur SUD
                    sequence = []
            sequence.append((i, w - 1))  # Au cas où on n'arrive pas à la dernière cellule
            murACasser = choice(sequence)
            laby.remove_wall(murACasser, (murACasser[0] + 1, murACasser[1]))  # On casse le mur SUD

        for j in range(laby.width - 1):  # On supprime le mur EST de toute la ligne du bas
            laby.remove_wall((h - 1, j), (h - 1, j + 1))

        return laby

    @classmethod
    def gen_fusion(cls, h: int, w: int) -> 'Maze':
        """
        Méthode de classe qui permet de générer un labyrinthe selon l'algorithme de génération par fusion des chemins
        Retour :
            Retourne le labyrinthe généré
        """

        laby = Maze(h, w)  # Initialisation du labyrinthe
        label = {}  # Création du label (dictionnaire)
        cpt = 1  # Création du compteur pour le label

        # Labellisation de toutes les cellules du labyrinthe
        for i in range(laby.height):
            for j in range(laby.width):
                label[(i, j)] = cpt
                cpt += 1

        listeMurs = laby.get_walls()  # On récupère tous les murs
        shuffle(listeMurs)  # On mélange les murs

        for i in listeMurs:  # On parcours la liste des murs
            if label[i[0]] != label[i[1]]:  # Si deux cellules ont un label différent :
                laby.remove_wall((i[0]), (i[1]))  # On retire le mur entre elle
                # On récupère le label des deux cellules
                labC1 = label[i[0]]
                labC2 = label[i[1]]
                for wall, lab in label.items():  # On parcourt le label
                    if lab == labC2:  # Si une cellule a le même label que notre deuxième cellule :
                        label[wall] = labC1  # On lui affecte le label de la 1re cellule
        return laby

    @classmethod
    def gen_exploration(cls, h: int, w: int) -> 'Maze':
        """
        Méthode de classe qui permet de générer un labyrinthe selon une "exploration" aléatoire du labyrinthe,
        à la manière d’un parcours en profondeur, en cassant les murs à mesure qu’on avance
        Retour :
            Retourne le labyrinthe généré
        """
        laby = Maze(h, w)  # Initialisation du labyrinthe
        premiereCellule = choice(laby.get_cells())  # Choix d'une cellule au hasard
        visite = [premiereCellule]  # Marquer cette cellule comme étant visitée
        pile = [premiereCellule]  # Mettre cette cellule dans une pile

        while pile:  # Tant que la pile n'est pas vide
            fin = len(pile) - 1
            celluleHaut = pile[fin]
            cellulesVoisines = laby.get_contiguous_cells(celluleHaut)
            cellulesNonVisites = []
            # Ajout des cellules voisines non visitées dans une liste
            for a in cellulesVoisines:
                if a not in visite:
                    cellulesNonVisites.append(a)

            if cellulesNonVisites:  # S'il y a un élément dans la liste
                celluleChoisie = choice(cellulesNonVisites)  # Choix aléatoire parmi les voisins de notre cellule
                # en haut de la pile
                laby.remove_wall(celluleHaut, celluleChoisie)  # Cassage du mur entre la cellule tirée au sort et
                # celle du haut de la pile
                visite.append(celluleChoisie)
                pile.append(celluleChoisie)
            else:  # Quand la cellule actuelle n'a plus de voisins
                pile.pop()  # Supprime la première cellule de la pile
        return laby

    @classmethod
    def gen_wilson(cls, h: int, w: int) -> 'Maze':
        """
        Méthode de classe qui permet de générer un labyrinthe selon l'algorithme de Wilson
        Retour :
            Retourne le labyrinthe généré
        """

        laby = Maze(h, w)
        toutesCellules = laby.get_cells()
        visite = []
        celluleDepart = choice(toutesCellules)
        visite.append(celluleDepart)

        while len(visite) < len(toutesCellules):  # Tant qu'il reste des cases non marquées :

            cellulesNonVisitees = []  # Ajout dans une liste de toutes les cellules non marquées
            for a in toutesCellules:
                if a not in visite:
                    cellulesNonVisitees.append(a)

            celluleDepart = choice(cellulesNonVisitees)
            chemin = [celluleDepart]
            celluleActuelle = celluleDepart

            while celluleActuelle not in visite:  # Tant que la case actuelle ne rencontre pas une case marquée
                cellulesVoisines = laby.get_contiguous_cells(celluleActuelle)
                shuffle(cellulesVoisines)
                celluleSuivante = choice(cellulesVoisines)  # On choisit la prochaine case# aléatoirement

                if celluleSuivante in chemin:  # Si la tête se mort la queue
                    index = chemin.index(celluleSuivante)  # On ne garde que la première occurrence
                    chemin = chemin[:index + 1]  # Supprime les cases que l'on a déjà visitées à partir de la 1ère
                    # occurrence
                else:
                    chemin.append(celluleSuivante)  # Ajoute la case au chemin

                celluleActuelle = celluleSuivante

            for i in range(len(chemin) - 1):
                visite.append(chemin[i])  # On ajoute les cases du chemin aux cases visitées
                laby.remove_wall(chemin[i], chemin[i + 1])  # On retire les murs entre les cases du chemin

        return laby

    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument :
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour :
            string
        """
        if content is None:
            content = {(i, j): ' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            # content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i, j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += " " + content[(0, j)] + " ┃" if (0, j + 1) not in self.neighbors[(0, j)] else " " + content[
                (0, j)] + "  "
        txt += " " + content[(0, self.width - 1)] + " ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " " + content[(i + 1, j)] + " ┃" if (i + 1, j + 1) not in self.neighbors[(i + 1, j)] else " " + \
                                                                                                                 content[
                                                                                                                     (
                                                                                                                     i + 1,
                                                                                                                     j)] + "  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt

    def solve_dfs(self, start: tuple, stop: tuple) -> list:
        """
        Méthode qui permet d'obtenir le chemin entre la cellule start et la cellule stop
        en utilisant la méthode du parcours en profondeur (pile)
        Retour :
            Retourne la liste des cellules (liste de tuples)
        """
        pile = [start]
        visite = [start]
        pred = {start: start}
        solution = []

        while pile:
            c = pile.pop()
            if c == stop:
                break
            else:
                voisinesC = self.get_reachable_cells(c)
                for a in voisinesC:
                    if a not in visite:
                        visite.append(a)
                        pile.append(a)
                        pred[a] = c

        c = stop
        while c != start:
            solution.append(c)
            c = pred[c]
        solution.reverse()  # Inverser le chemin pour commencer à partir de start

        return solution

    def solve_bfs(self, start: tuple, stop: tuple) -> list:
        """
        Méthode qui permet d'obtenir le chemin entre la cellule start et la cellule stop
        en utilisant la méthode du parcours en largeur (file)
        Retour :
            Retourne la liste des cellules (liste de tuples)
        """
        file = [start]
        visite = [start]
        pred = {start: start}
        solution = []

        while file:
            c = file.pop(0)
            if c == stop:
                break
            else:
                voisinesC = self.get_reachable_cells(c)
                for a in voisinesC:
                    if a not in visite:
                        visite.append(a)
                        file.append(a)
                        pred[a] = c
        c = stop
        while c != start:
            solution.append(c)
            c = pred[c]
        solution.append(start)
        solution.reverse()

        return solution

    def get_reachable_cells2(self, cell: tuple) -> list:
        """
        Déclinaison de la méthode get_reachable_cells qui permet d'obtenir les cellules atteignables
        dans un ordre précis : EST / NORD / OUEST / SUD
        Retour :
            Retourne la liste des cellules atteignables depuis la cellule passée en paramètre
        """
        lst = []
        (i, j) = cell
        if j - 1 >= 0 and (i, j - 1) in self.neighbors[(i, j)]:
            lst.append((i, j - 1))
        if i + 1 < self.height and (i+1, j) in self.neighbors[(i, j)]:
            lst.append((i+1, j))
        if j + 1 < self.width and (i, j+1) in self.neighbors[(i, j)]:
            lst.append((i, j+1))
        if i - 1 >= 0 and (i-1, j) in self.neighbors[(i, j)]:
            lst.append((i-1, j))
        return lst

    def solve_rhr(self, start: tuple, stop: tuple) -> list:
        """
        Méthode qui permet de résoudre un labyrinthe selon la technique de la "main droite"
        comme si l'on se déplaçait aveuglément dans le labyrinthe
        Retour :
            Retourne la liste de toutes les cellules visitées
        """
        pile = [start]
        visite = []  # Utiliser un ensemble pour garder une trace des cellules visitées
        pred = {start: start}

        while pile:
            c = pile[-1]  # Prendre la dernière cellule de la pile pour l'explorer
            if c == stop:
                break
            else:
                visite.append(c)  # Ajouter la cellule à visite
                voisinesC = self.get_reachable_cells2(c)
                if not voisinesC:  # Si pas de voisins non visités
                    pile.pop()  # Revenir en arrière
                    del pred[c]
                else:
                    # Créer une nouvelle liste de voisins sans le voisin visité
                    new_voisinesC = []
                    for a in voisinesC:
                        if a != c and a not in visite:
                            new_voisinesC.append(a)
                    if new_voisinesC:
                        next_cell = new_voisinesC[0]  # Prendre le premier voisin non visité
                        pred[next_cell] = c  # Enregistrer le prédécesseur
                        pile.append(next_cell)  # Ajouter à la pile
                    else:
                        pile.pop()  # Revenir en arrière

        # Reconstituer le chemin à partir de la destination jusqu'à la source
        c = stop
        chemin = []
        while c != start:
            chemin.append(c)
            c = pred[c]
        chemin.append(start)
        chemin.reverse()
        return visite

    def distance_geo(self, c1: tuple, c2: tuple) -> int:
        """
        Méthode qui permet d'obtenir la distance géodésique entre la cellule c1 et la cellule c2
        (nombre minimal de déplacements nécessaires entre c1 et c2)
        Retour :
            Retourne un entier
        """
        chemin = self.solve_bfs(c1, c2)
        return len(chemin) - 1

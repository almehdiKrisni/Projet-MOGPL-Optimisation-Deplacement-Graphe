


#                                   PROJET MOGPL 2021 GROUPE 3
#                                             GRAPHES
#                                  KRISNI Almehdi et ABREU Hugo
#                          https://github.com/krisninho2000/Projet_MOGPL


#######################################################################################################
# LIBRAIRIES PYTHON
#######################################################################################################

import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
# import time
# import datetime
import math

from networkx.exception import NodeNotFound

#######################################################################################################
# INFORMATIONS
#######################################################################################################

# Les graphes sont des dictionnaires dont :
# - les clés sont des noms de sommets du graphe
# - les valeurs situées dans dans le dictionnaire sont des listes d'arcs sortants du sommet représenté par la clé
# - les arcs sont de la forme (s1, s2, dDD, cDT)
# (s1 : sommet d'origine, s2 : sommet destination)
# (dDD : la date de départ du vol, cDT : le nombre de jours pour effectuer le trajet)

#######################################################################################################
# OUTILS
#######################################################################################################

# Méthode permettant d'acquérir un graphe G (modelisation : dictionnaire) depuis un fichier texte
def acquisitionGraphe(nomFichier) :
    # On crée le graphe G que nous allons retourner et d'autres variables
    G = dict()
    nbSommets = 0
    nbSommetsLus = 0
    nbArcs = 0
    nbArcsLus = 0
    phase = 0 # Permet de savoir si nous somme en phase de préparation ou de lecture

    # Lecture du fichier
    with open(nomFichier, 'r') as fichier :
        for ligne in fichier :

            # Phase de préparation
            if (phase == 0) :
            # Lecture du nombre de sommets
                if ligne.startswith('Nombre sommets') :
                    e = ligne.strip().split()
                    if len(e) == 3 :
                        (s1, s2, s3) = e
                        nbSommets = int(s3)
                    else :
                        print("Problème de format lors de la lecture du nombre de sommets.")
                        return

                # Lecture du nombre d'arcs
                if ligne.startswith('Nombre arcs') :
                    e = ligne.strip().split()
                    if len(e) == 3 :
                        (s1, s2, s3) = e
                        nbArcs = int(s3)
                        phase = 1
                    else :
                        print("Problème de format lors de la lecture du nombre d'arcs.")
                        return

            # Phase de lecture des sommets et des arcs
            else :
                # Lecture d'un sommet
                if (nbSommetsLus < nbSommets) :
                    e = ligne.strip().split()
                    if len(e) == 1 :
                        G[ligne.strip()] = []
                        nbSommetsLus += 1
                    else :
                        print("Problème de format lors de la lecture d'un sommet.")
                        return

                # Lecture d'un arc
                elif (nbArcsLus < nbArcs) :
                    e = ligne.replace(',', ' ').strip('()\n').split()
                    if len(e) == 4 :
                        (s1, s2, s3, s4) = e
                        G[s1].append((s2, int(s3), int(s4)))
                        nbArcsLus += 1
                    else :
                        print("Problème de format lors de la lecture d'un arc")
                        return

    # On retourne le graphe
    return G


#------------------------------------------------------------------------------------------------------

# Méthode permettant d'afficher à l'écran un graphe condensé repertorié dans le fichier source
def showGraphe(graphe, titre = "G"):
    """ graphe : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
        titre : titre du graphe à afficher, 'G' par defaut
    """
    G = nx.DiGraph()
    origin = 0

    nbNodes = 0
    for v1 in list(graphe.keys()) :
        if (origin == 0) :
            G.add_node(v1, pos=(1, 0))
            origin = 1
        else :
            G.add_node(v1, pos = ((nbNodes % 3), - 1 - (nbNodes / 3)))
            nbNodes += 1
            

    G.add_nodes_from(list(graphe.keys()))
    for v1 in graphe.keys():
        for v2 in graphe[v1] :
            (s1, _, _) = v2
            G.add_edge(v1, s1)

    plt.title(titre)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=500, font_size = 10, node_color="skyblue")

    plt.show()

#------------------------------------------------------------------------------------------------------

# Méthode permettant d'afficher à l'écran un multigraphe orienté repertorié dans le fichier source avec les valeurs associées à chaque arc
def showGrapheLabels(graphe, titre = "G"):
    """ graphe : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
        titre : titre du graphe à afficher, 'G' par defaut
    """
    G = nx.DiGraph()
    origin = 0

    nbNodes = 0
    for v1 in list(graphe.keys()) :
        if (origin == 0) :
            G.add_node(v1, pos=(1, 0))
            origin = 1
        else :
            G.add_node(v1, pos = ((nbNodes % 3), - 1 - (nbNodes / 3)))
            nbNodes += 1
            

    G.add_nodes_from(list(graphe.keys()))
    for v1 in graphe.keys():
        for v2 in graphe[v1] :
            (s1, s2, _) = v2
            G.add_edge(v1, s1, d = s2)

    plt.title(titre)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=500, font_size = 10, node_color="skyblue")
    nx.draw_networkx_edge_labels(G, pos)

    plt.show()

#######################################################################################################
# ALGORITHMES DE RECHERCHE DE CHEMIN
#######################################################################################################

# Dans les algorithmes de recherche, on utilise des 'states' contenant :
# - la position actuelle (le sommet courant)
# - le temps actuel (le jour auquel on se trouve)
# - le père du state (le noeud précédent)

# Les states seront repertoriés sous forme de pile et explorés de manière exhaustive
# Si on trouve un state satisfaisant, on peut retracer le chemin en consultant les pères des noeuds
# jusqu'à trouver le noeud initial

#------------------------------------------------------------------------------------------------------

# Fonction permettant d'obtenir la racine d'une arborescence de state
def fatherState(state) :
    while (state[2] != None) :
        state = state[2]
    return state

#------------------------------------------------------------------------------------------------------

# Algorithme de recherche de chemin d'arrivée au plus tôt entre deux sommets d'un graphe
def cheminArriveePlusTot(graphe, start, end) :
    # On crée le state initial (voir les commentaires au-dessus pour plus de details)
    stateInit = (start, 1, None)
    pile = []

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    bestTime = None

    # On crée la pile contenant tous les noeuds accessibles depuis stateInit
    for s in graphe[start] :
        if (s[1] >= stateInit[1]) : # Si le vol associé à l'arc a lieu le jour-même où on se trouve dans le state courant ou plus tard
            pile.append((s[0], s[1] + s[2], stateInit)) # s[1] + s[2] représente l'addition du jour où le vol a lieu plus le temps du trajet
    
    # On boucle sur la pile
    while (len(pile) != 0) :
        # On récupère le noeud en tête de liste et on le supprime de la liste
        stateStudy = pile[0]
        pile = pile[1:]

        # On vérifie si l'état actuel correspond à l'état final
        if (stateStudy[0] == end) :
            # On vérifie si le temps actuel est plus intéressant que le meilleur temps trouvé (ou si aucun n'a encore été trouvé)
            if (bestTime == None) :
                bestTime = stateStudy[1] # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (bestTime > stateStudy[1]) :
                bestTime = stateStudy[1]
                bestChemin = stateStudy

        # Sinon, on étudie les autres chemins possibles
        else :
            for s in graphe[stateStudy[0]] :
                if (s[1] >= stateStudy[1]) :
                    pile.append((s[0], s[1] + s[2], stateStudy))

    # Fin de l'algorithme
    # On vérifie si on a trouvé un meilleur chemin
    if (bestChemin != None) :
        # Si oui, on le retrace à l'envers puis on le retourne
        chemin = []
        while (bestChemin != None) :
            chemin.append((bestChemin[0], bestChemin[1]))
            bestChemin = bestChemin[2]
        return chemin[::-1]

    # Sinon, on renvoie un message pour signaler qu'aucun chemin n'a pu être trouvé
    else :
        print("Aucun chemin n'a pu être trouvé dans le graphe entre " + str(start) + " et " + str(end) + ".")

#------------------------------------------------------------------------------------------------------

# Algorithme permettant de trouver le chemin de départ au plus tard entre deux sommets du graphe
def cheminArriveePlusTard(graphe, start, end) :
    # On crée la pile (le stateInit n'est pas nécessaire dans cet algorithme, voir le remplissage de pile)
    pile = []

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    latestDepart = None

    # On crée la pile contenant tous les noeuds accessibles depuis le stateInit avec les dates de départ
    # celles du date de départ des vols possibles depuis stateInit
    for s in graphe[start] :
        startingPoint = (start, s[1], None)
        pile.append((s[0], s[1] + s[2], startingPoint))

    # On boucle sur la pile
    while (len(pile) != 0) :
        # On récupère le noeud en tête de liste et on le supprime de la liste
        stateStudy = pile[0]
        pile = pile[1:]

        # On vérifie si l'état actuel correspond à l'état final
        if (stateStudy[0] == end) :
            # On récupère le temps de départ du chemin représenté par le noeud
            startTime = fatherState(stateStudy)[1]

            # On vérifie si le temps actuel est plus intéressant que le meilleur temps trouvé (ou si aucun n'a encore été trouvé)
            if (latestDepart == None) :
                latestDepart = startTime # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (latestDepart < startTime) :
                latestDepart = startTime
                bestChemin = stateStudy

        # Sinon, on étudie les autres chemins possibles
        else :
            for s in graphe[stateStudy[0]] :
                if (s[1] >= stateStudy[1]) :
                    pile.append((s[0], s[1] + s[2], stateStudy))

    # Fin de l'algorithme
    # On vérifie si on a trouvé un meilleur chemin
    if (bestChemin != None) :
        # Si oui, on le retrace à l'envers puis on le retourne
        chemin = []
        while (bestChemin != None) :
            chemin.append((bestChemin[0], bestChemin[1]))
            bestChemin = bestChemin[2]
        return chemin[::-1]

    # Sinon, on renvoie un message pour signaler qu'aucun chemin n'a pu être trouvé
    else :
        print("Aucun chemin n'a pu être trouvé dans le graphe entre " + str(start) + " et " + str(end) + ".")

#------------------------------------------------------------------------------------------------------

# Algorithme représentant la recherche du chemin le plus rapide entre deux sommets d'un graphe
def cheminPlusRapide(graphe, start, end) :
    # On crée la pile (le stateInit n'est pas nécessaire dans cet algorithme, voir le remplissage de pile)
    pile = []

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    shortestTime = None

    # On crée la pile contenant tous les noeuds accessibles depuis le stateInit avec les dates de départ
    # celles du date de départ des vols possibles depuis stateInit (on économise le plus de temps possible)
    for s in graphe[start] :
        startingPoint = (start, s[1], None)
        pile.append((s[0], s[1] + s[2], startingPoint))
    
    # On boucle sur la pile
    while (len(pile) != 0) :
        # On récupère le noeud en tête de liste et on le supprime de la liste
        stateStudy = pile[0]
        pile = pile[1:]

        # On vérifie si l'état actuel correspond à l'état final
        if (stateStudy[0] == end) :
            # On récupère le temps de départ du chemin représenté par le noeud
            timeSpent = stateStudy[1] - fatherState(stateStudy)[1]

            # On vérifie si le temps actuel est plus intéressant que le meilleur temps trouvé (ou si aucun n'a encore été trouvé)
            if (shortestTime == None) :
                shortestTime = timeSpent # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (shortestTime > timeSpent) :
                shortestTime = timeSpent
                bestChemin = stateStudy

        # Sinon, on étudie les autres chemins possibles
        else :
            for s in graphe[stateStudy[0]] :
                if (s[1] >= stateStudy[1]) :
                    pile.append((s[0], s[1] + s[2], stateStudy))

    # Fin de l'algorithme
    # On vérifie si on a trouvé un meilleur chemin
    if (bestChemin != None) :
        # Si oui, on le retrace à l'envers puis on le retourne
        chemin = []
        while (bestChemin != None) :
            chemin.append((bestChemin[0], bestChemin[1]))
            bestChemin = bestChemin[2]
        return chemin[::-1]

    # Sinon, on renvoie un message pour signaler qu'aucun chemin n'a pu être trouvé
    else :
        print("Aucun chemin n'a pu être trouvé dans le graphe entre " + str(start) + " et " + str(end) + ".")
            
            
#######################################################################################################
# TESTS
#######################################################################################################

# Fonction de lecture
grap = acquisitionGraphe("exempleGraphe.txt")

# Fonction d'affichage de graphe
showGraphe(grap)
showGrapheLabels(grap)

# Algorithme de chemin d'arrivée au plus tôt
print(cheminArriveePlusTot(grap, 'a', 'k'))
print(cheminArriveePlusTot(grap, 'c', 'k'))
print(cheminArriveePlusTot(grap, 'g', 'h'))

# Algorithme de chemin de départ au plus tard
print(cheminArriveePlusTard(grap, 'a', 'k'))
print(cheminArriveePlusTard(grap, 'b', 'l'))
print(cheminArriveePlusTard(grap, 'c', 'f'))

# Algorithme de chemin le plus rapide
print(cheminPlusRapide(grap, 'a', 'k'))
print(cheminPlusRapide(grap, 'c', 'l'))
print(cheminPlusRapide(grap, 'h', 'j'))



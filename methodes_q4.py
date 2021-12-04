


#                                   PROJET MOGPL 2021 GROUPE 3
#                                             GRAPHES
#                                  KRISNI Almehdi et ABREU Hugo
#                          https://github.com/krisninho2000/Projet_MOGPL


#######################################################################################################
# LIBRAIRIES PYTHON
#######################################################################################################

import copy
from functools import partialmethod
import numpy as np
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

# Il existe une deuxième forme de graphe: les graphes pondérés
# Ils sont sous la forme de 2 dictionnaires 
# - le premier dont les clés sont les différents sommets du graphe et les valeurs associées
# sont les listes représentant les arcs rentrants et les arcs sortants du sommet (tuple)
# - le deuxième étant le dictionnaire contenant les arcs entre les différents sommets du graphe (le dictionnaire du graphe basique)

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

#-----------------------------------------------------------------------------------------------------

# Méthode permettant de transformer un graphe classique en graphe orienté pondéré par le temps
def transformeGraphe(graphe, sortantUniquement = False) :
    # On crée le nouveau graphe
    G = dict()

    # On crée dans un premier temps l'intégralité des sommets de transition sur le même sommet du graphe original
    for i in list(graphe.keys()) : # i est un sommet
        for j in graphe[i] : # j est de la forme (cible, jour du trajet, temps de trajet)

            # On crée des variable représentant les sommet origine et cible afin de faciliter la compréhension
            origin = (i,j[1])
            target = (j[0], j[1] + j[2])

            # On vérifie si le sommet d'origine existe dans le dictionnaire en tant que clé
            if ((i,j[1]) not in G.keys()) :
                G[(i,j[1])] = ([], []) # On crée les listes des arcs rentrants et des arcs sortants du sommet i
            
            # On vérifie également que le sommet cible existe dans le dictionnaire en tant que clé
            if ((j[0], j[1] + j[2]) not in G.keys()) :
                G[(j[0], j[1] + j[2])] = ([], [])

            # On ajoute les valeurs dans les listes approriées
            G[origin][1].append(target) # L'arc sortant de l'origine vers la cible
            G[target][0].append(origin) # L'arc rentrant dans la cible depuis l'origine

    # On ajoute les arcs de transition entre les sommets dont le temps actuel est différent (on les lie dans l'ordre chronologique)
    for i in list(graphe.keys()) :
        # On regroupe toutes les clés représentant ce sommet
        sommets = []
        for j in list(G.keys()) :
            (s1, s2) = j
            if (s1 == i) :
                sommets.append(j)
        
        # On les trie de manière croissante sur les jours
        sommets.sort(key=lambda tup: tup[1])

        # On les lie de manière croissante (tant qu'il existe au moins 2 éléments à lier dans la liste)
        i = 1
        while (i < len(sommets)) :
            origin = sommets[i - 1]
            target = sommets[i]

            # On ajoute les valeurs dans les listes approriées
            G[origin][1].append(target) # L'arc sortant de l'origine vers la cible
            G[target][0].append(origin) # L'arc rentrant dans la cible depuis l'origine
            i += 1


    # On retourne le nouveau graphe (en fonction du parametres)
    if not(sortantUniquement) :
        return G
    else :
        nG = dict()
        for i in G.keys() :
            nG[i] = G[i][1]
        return nG

#------------------------------------------------------------------------------------------------------

# Méthode permettant d'obtenir la racine d'une arborescence de state
def fatherState(state) :
    while (state[2] != None) :
        state = state[2]
    return state

#------------------------------------------------------------------------------------------------------

# Méthode permettant d'obtenir la longueur d'une arborescence de state
def pathLength(state) :
    l = 0
    while (state != None) :
        l += 1
        state = state[2] 
    return l

#######################################################################################################
# ALGORITHMES DE RECHERCHE DE CHEMIN SUR LES MULTIGRAPHES (FONCTIONNE SUR LES GRAPHES DE BASE - QUESTION SUBSIDIAIRE)
#######################################################################################################

# Dans les algorithmes de recherche, on utilise des 'states' contenant :
# - la position actuelle (le sommet courant)
# - le temps actuel (le jour auquel on se trouve)
# - le père du state (le noeud précédent)

# Les states seront repertoriés sous forme de pile et explorés de manière exhaustive
# Si on trouve un state satisfaisant, on peut retracer le chemin en consultant les pères des noeuds
# jusqu'à trouver le noeud initial

#------------------------------------------------------------------------------------------------------

# ALgorithme de recherche du chemin d'arrivée au plus tôt entre deux sommets d'un graphe transformé
def cheminArriveeAuPlusTot(graphe, start, end) :
    # On crée une pile allant contenir tous les départs possibles depuis le sommet 'start'
    # On ajoute dans cette pile également tous les fils de ces départs (soit les sommets sur lesquels on peut se déplacer)
    pile = []
    
    # On vérifie si on peut commencer depuis le premier jour de 'start'
    if (start, 1) in list(graphe.keys()) :
        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Sinon, on crée une nouvelle entrée dans le graphe
    # On lie le noeud (start, 1) aux autres noeuds de la forme (start, X) du graphe
    else :
        listAcces = [(i, j) for (i, j) in list(graphe.keys()) if (i == start)]
        graphe[(start, 1)] = listAcces

        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    bestTime = None

    # On parcourt la file
    while (pile) :
        # On récupère la tête de pile et on la supprime de la liste
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

        # Sinon, on ajoute les nouvelles directions possibles dans la pile
        else :
            for (j, k) in graphe[(stateStudy[0], stateStudy[1])] :
                pile.append((j, k, stateStudy))

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

# ALgorithme de recherche du chemin d'arrivée au plus tard entre deux sommets d'un graphe transformé
def cheminDepartAuPlusTard(graphe, start, end) :
    # On crée une pile allant contenir tous les départs possibles depuis le sommet 'start'
    # On ajoute dans cette pile également tous les fils de ces départs (soit les sommets sur lesquels on peut se déplacer)
    pile = []
    
    # On vérifie si on peut commencer depuis le premier jour de 'start'
    if (start, 1) in list(graphe.keys()) :
        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Sinon, on crée une nouvelle entrée dans le graphe
    # On lie le noeud (start, 1) aux autres noeuds de la forme (start, X) du graphe
    else :
        listAcces = [(i, j) if (i == start) else None for (i, j) in list(graphe.keys())]
        print(listAcces)
        graphe[(start, 1)] = listAcces

        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    lastDeparture = None

    # On parcourt la file
    while (pile) :
        # On récupère la tête de pile et on la supprime de la liste
        stateStudy = pile[0]
        pile = pile[1:]

        # On vérifie si l'état actuel correspond à l'état final
        if (stateStudy[0] == end) :
            # On récupère le jour de départ du chemin représenté par le noeud le plus récent dont la position est 'start' dans l'arboresence
            s = stateStudy
            while (s[0] != start) :
                s = s[2]
            startTime = s[1]

            # On vérifie si le temps actuel est plus intéressant que le meilleur temps trouvé (ou si aucun n'a encore été trouvé)
            if (lastDeparture == None) :
                lastDeparture = startTime # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (lastDeparture < startTime) :
                lastDeparture = startTime
                bestChemin = stateStudy

        # Sinon, on ajoute les nouvelles directions possibles dans la pile
        else :
            for (j, k) in graphe[(stateStudy[0], stateStudy[1])] :
                pile.append((j, k, stateStudy))

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

# Algorithme de recherche du chemin d'arrivée au plus tard entre deux sommets d'un graphe transformé
def cheminPlusRapide(graphe, start, end) :
    # On crée une pile allant contenir tous les départs possibles depuis le sommet 'start'
    # On ajoute dans cette pile également tous les fils de ces départs (soit les sommets sur lesquels on peut se déplacer)
    pile = []
    
    # On vérifie si on peut commencer depuis le premier jour de 'start'
    if (start, 1) in list(graphe.keys()) :
        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Sinon, on crée une nouvelle entrée dans le graphe
    # On lie le noeud (start, 1) aux autres noeuds de la forme (start, X) du graphe
    else :
        listAcces = [(i, j) if (i == start) else None for (i, j) in list(graphe.keys())]
        print(listAcces)
        graphe[(start, 1)] = listAcces

        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    shortestTime = None

    # On parcourt la file
    while (pile) :
        # On récupère la tête de pile et on la supprime de la liste
        stateStudy = pile[0]
        pile = pile[1:]

        # On vérifie si l'état actuel correspond à l'état final
        if (stateStudy[0] == end) :
            # On récupère le temps écoulé depuis le départ
            timeSpent = stateStudy[1] - fatherState(stateStudy)[1]

            # On vérifie si le temps actuel est plus intéressant que le meilleur temps trouvé (ou si aucun n'a encore été trouvé)
            if (shortestTime == None) :
                shortestTime = timeSpent # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (shortestTime > timeSpent) :
                shortestTime = timeSpent
                bestChemin = stateStudy

        # Sinon, on ajoute les nouvelles directions possibles dans la pile
        else :
            for (j, k) in graphe[(stateStudy[0], stateStudy[1])] :
                pile.append((j, k, stateStudy))

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

# Algorithme de recherche du chemin d'arrivée au plus tard entre deux sommets d'un graphe transformé
def cheminPlusCourt(graphe, start, end) :
    # On crée une pile allant contenir tous les départs possibles depuis le sommet 'start'
    # On ajoute dans cette pile également tous les fils de ces départs (soit les sommets sur lesquels on peut se déplacer)
    pile = []

    # On vérifie si on peut commencer depuis le premier jour de 'start'
    if (start, 1) in list(graphe.keys()) :
        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Sinon, on crée une nouvelle entrée dans le graphe
    # On lie le noeud (start, 1) aux autres noeuds de la forme (start, X) du graphe
    else :
        listAcces = [(i, j) if (i == start) else None for (i, j) in list(graphe.keys())]
        print(listAcces)
        graphe[(start, 1)] = listAcces

        for (j, k) in graphe[(start, 1)] :
            pile.append((j, k, (start, 1, None))) # Le deuxième tuple représente le state du sommet 'start'

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    fewestMoves = None

    # On parcourt la file
    while (pile) :
        # On récupère la tête de pile et on la supprime de la liste
        stateStudy = pile[0]
        pile = pile[1:]

        # On vérifie si l'état actuel correspond à l'état final
        if (stateStudy[0] == end) :
            # On récupère le nombre déplacements effectués
            differentPlaces = [] # Les différents lieux par lesquels on est passé sur le chemin jusqu'à 'end'
            s = stateStudy
            while (s) :
                differentPlaces.append(s[0])
                s = s[2]
            numberMoves = len(np.unique(np.asarray(differentPlaces)))

            # On vérifie si le temps actuel est plus intéressant que le meilleur temps trouvé (ou si aucun n'a encore été trouvé)
            if (fewestMoves == None) :
                fewestMoves = numberMoves # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (fewestMoves > numberMoves) :
                fewestMoves = numberMoves
                bestChemin = stateStudy

        # Sinon, on ajoute les nouvelles directions possibles dans la pile
        else :
            for (j, k) in graphe[(stateStudy[0], stateStudy[1])] :
                pile.append((j, k, stateStudy))

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
# ALGORITHMES DE RECHERCHE DE CHEMIN SUR LES MULTIGRAPHES (FONCTIONNE SUR LES GRAPHES DE BASE - QUESTION SUBSIDIAIRE)
#######################################################################################################

# Algorithme de recherche de chemin d'arrivée au plus tôt entre deux sommets d'un graphe
def cheminArriveePlusTotV2(graphe, start, end) :
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
def cheminDepartPlusTardV2(graphe, start, end) :
    # On crée la pile (le stateInit n'est pas nécessaire dans cet algorithme, voir le remplissage de pile)
    pile = []

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    lastDeparture = None

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
            if (lastDeparture == None) :
                lastDeparture = startTime # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (lastDeparture < startTime) :
                lastDeparture = startTime
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
def cheminPlusRapideV2(graphe, start, end) :
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
            # On récupère le temps écoulé depuis le départ
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

#------------------------------------------------------------------------------------------------------

# Algorithme représentant la recherche du plus court chemin entre deux sommets d'un graphe
def plusCourtCheminV2(graphe, start, end) :
    # On crée le state initial et la pile
    stateInit = (start, 1, None)
    pile = []

    # Variables de sauvegarde de meilleur chemin
    bestChemin = None
    shortestDistance = None

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
            if (shortestDistance == None) :
                shortestDistance = pathLength(stateStudy) # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (shortestDistance > pathLength(stateStudy)) :
                shortestDistance = pathLength(stateStudy)
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
grap = acquisitionGraphe("Repertoire_Graphes/exempleGraphe.txt")

# Fonction de transformation de graphe
G = transformeGraphe(grap, sortantUniquement=True)
# for i in G.keys() :
#     print(str(i) + " : " + str(G[i]))

# Fonction d'affichage de graphe
# showGraphe(grap)
# showGrapheLabels(grap)

# # Algorithme de chemin d'arrivée au plus tôt
# print(cheminArriveeAuPlusTot(G, 'a', 'k'))
# print(cheminArriveeAuPlusTot(G, 'c', 'k'))
# print(cheminArriveeAuPlusTot(G, 'g', 'h'))

# # Algorithme de chemin de départ au plus tard
# print(cheminDepartAuPlusTard(G, 'a', 'k'))
# print(cheminArriveeAuPlusTard(G, 'b', 'l'))
# print(cheminArriveeAuPlusTard(G, 'c', 'f'))

# # Algorithme de chemin le plus rapide
# print(cheminPlusRapide(G, 'a', 'k'))
# print(cheminPlusRapide(G, 'c', 'l'))
# print(cheminPlusRapide(G, 'h', 'j')

# Algorithme de plus court chemin
# print(cheminPlusCourt(G, 'a', 'k'))
# print(plusCourtChemin(G, 'c', 'l'))
# print(plusCourtChemin(G, 'h', 'j'))




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
import util as ut

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
            timeSpent = stateStudy[1] - ut.fatherState(stateStudy)[1]

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
        listAcces = [(i, j) for (i, j) in list(graphe.keys()) if (i == start) ]
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
def cheminArriveePlusTotV2(graphe, start, end, test = True) :
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
        if test:
            return True
        else:
            return chemin[::-1]

    # Sinon, on renvoie un message pour signaler qu'aucun chemin n'a pu être trouvé
    else :
        if test:
            return False
        else:
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
            startTime = ut.fatherState(stateStudy)[1]

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
            timeSpent = stateStudy[1] - ut.fatherState(stateStudy)[1]

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
                shortestDistance = ut.pathLength(stateStudy) # Le meilleur temps
                bestChemin = stateStudy # Le meilleur chemin (on le dépile en fin d'algorithme)

            elif (shortestDistance > ut.pathLength(stateStudy)) :
                shortestDistance = ut.pathLength(stateStudy)
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

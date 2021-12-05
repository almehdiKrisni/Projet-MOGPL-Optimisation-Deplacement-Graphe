


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

# Méthode permettant d'obtenir un graphe statique condensé à partir d'un graphe classique
def transformeGrapheCondense(graphe) :
    # On crée un nouveau dictionnaire et on crée une entrée pour chaque sommet du graphe
    G = dict()
    for s in list(graphe.keys()) :
        G[s] = []

    # On parcourt le graphe initial et on ajoute dans la liste de chaque sommet les sommets vers lesquels on peut se déplacer
    for s in list(graphe.keys()) :
        for (i, _, _) in graphe[s] :
            if (i not in G[s]) :
                G[s].append(i)

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
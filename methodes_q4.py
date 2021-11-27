


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

# Méthode permettant d'afficher à l'écran un graphe non orienté et, éventuellement, un titre
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
            (s1, s2, _) = v2
            G.add_edge(v1, s1, d = s2)

    plt.title(titre)
    pos = nx.get_node_attributes(G, 'pos')
    edge_labels = nx.get_edge_attributes(G,'d')
    nx.draw(G, pos, with_labels=True, node_size=500, font_size = 10, node_color="skyblue")
    nx.draw_networkx_edge_labels(G, pos)

    plt.show()
            
            
#######################################################################################################
# TESTS
#######################################################################################################

# Fonction de lecture
grap = acquisitionGraphe("exempleGraphe.txt")
showGraphe(grap)



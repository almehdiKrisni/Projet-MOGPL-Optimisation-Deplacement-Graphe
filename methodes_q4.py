


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
    nbSommets = 0, nbSommetsLus = 0
    nbArcs = 0, nbArcsLus = 0
    phase = 0

    # Lecture du fichier
    with open(nomFichier, 'r') as fichier :
        for ligne in fichier :

            # Lecture du nombre de sommets
            if ligne.startswith('Nombre sommets') :
                e = ligne.strip().split()
                if len(e) == 3 :
                    (s1, s2, s3) = e
                    nbSommets = s3
                continue

            # Lecture du nombre d'arcs
            if ligne.startswith('Nombre arcs') :
                e = ligne.strip().split()
                if len(e) == 3 :
                    (s1, s2, s3) = e
                    nbArcs = s3
                    phase = 1
                continue

            # Lecture des sommets et des arcs
            if phase == 1 :
                # Lecture d'un sommet
                if (nbSommetsLus < nbSommets) :
                    e = ligne.strip().split()
                    if len(e) == 1 :
                        (s) = e
                        G[s] = []
                        nbSommetsLus += 1
                    else :
                        print("Problème de format lors de la lecture d'un sommet.")
                        exit

                # Lecture d'un arc
                elif (nbArcsLus < nbArcs) :
                    e = ligne.strip().split()
                    if len(e) == 4 :
                        (s1, s2, s3, s4) = e
                        G[s1].append((s2, s3, s4))
                        nbArcsLus += 1
                    else :
                        print("Problème de format lors de la lecture d'un sommet")
            
            
            






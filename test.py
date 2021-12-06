


#                                   PROJET MOGPL 2021 GROUPE 3
#                                             GRAPHES
#                                  KRISNI Almehdi et ABREU Hugo
#                          https://github.com/krisninho2000/Projet_MOGPL


#######################################################################################################
# IMPORT DES FICHERS PYTHON
#######################################################################################################

import algorithmesChemin as ach
import optimisation as opt
import util as ut
import random as rand
import time

#######################################################################################################
# TESTS DES METHODES
#######################################################################################################

# Valeurs permettant d'effectuer ou non certaines séries de tests
testUT = True
testACH = False
testOPT = True

# Parametre permettant de choisir si la sélection des sommets sera aléatoire ou non
randomSelection = True

# Tests des méthodes de util.py
if (testUT) :
    # Génération de graphe aléatoire
    g1 = ut.generationMultigraphe(25,50,25)

    # Génération de graphe depuis un fichier texte
    g2 = ut.acquisitionGraphe("Repertoire_Graphes/exempleGraphe.txt")

    # Transformation d'un graphe en graphe transformé (utilisé pour les méthodes du fichier algorithmeChemin utilisant les graphes transformés)
    g3 = ut.transformeGraphe(g1, sortantUniquement=True)

    # Transformation d'un graphe en graphe condensé dans le temps
    g4 = ut.transformeGrapheCondense(g1)
    

# Tests des méthodes de algorithmesChemin.py
if (testACH) :
    # On choisit le graphe allant être utilisé
    G = g3
    print(G)

    # On choisit les sommets allant être utilisés dans les tests ci-dessous
    if (randomSelection) :
        start = list(G.keys())[rand.randint(0, len(list(G.keys())) - 1)][0]
        end = list(G.keys())[rand.randint(0, len(list(G.keys())) - 1)][0]
    else :
        start = 'a'
        end = 'k'

    # On affiche l'état du graphe utilisé
    print("Le graphe utilisé est de la forme :")
    for i in list(G.keys()) :
        print(i, G[i])
    print()

    # Test des méthodes utilisant les graphes transformés
    # Algorithme de chemin d'arrivée au plus tôt
    print("Graphe transformé - Un chemin d'arrivée au plus tôt entre", start, "et", end, "est :", ach.cheminArriveeAuPlusTot(G, start, end), "\n")

    # Algorithme de chemin de départ au plus tard
    print("Graphe transformé - Un chemin de départ au plus tard entre", start, "et", end, "est :", ach.cheminDepartAuPlusTard(G, start, end), "\n")

    # Algorithme de chemin le plus rapide
    print("Graphe transformé - Un chemin le plus rapide entre", start, "et", end, "est :", ach.cheminPlusRapide(G, start, end), "\n")

    # Algorithme de plus court chemin
    print("Graphe transformé - Le plus court chemin entre", start, "et", end, "est :", ach.cheminPlusCourt(G, start, end), "\n")

# Tests des méthodes de optimisation.py
if (testOPT) :
    # On choisit le graphe allant être utilisé
    G = g4

    # On choisit les sommets allant être utilisés dans les tests ci-dessous
    if (randomSelection) :
        start = list(G.keys())[rand.randint(0, len(list(G.keys())) - 1)]
        end = list(G.keys())[rand.randint(0, len(list(G.keys())) - 1)]
        print(start, end)
    else :
        start = 'a'
        end = 'k'

    # On affiche l'état du graphe utilisé
    print("Le graphe utilisé est de la forme :")
    for i in list(G.keys()) :
        print(i, G[i])
    print()

    # Résolution par optimisation
    opt.optPlusCourtChemin(G, start, end)

#######################################################################################################
# CALCULS DE TEMPS D'EXECUTION
#######################################################################################################

# On récupère le graphe venant d'un fichier du répertoire Répertoires_Graphes
g5 = ut.acquisitionGraphe("Repertoire_Graphes/exempleGraphe.txt")



#######################################################################################################
# COMPARAISONS D'ALGORITHMES
#######################################################################################################

# On récupère le graphe venant d'un fichier du répertoire Répertoires_Graphes
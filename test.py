


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
testOPT = False
testComp = True

# Parametre permettant de choisir si la sélection des sommets sera aléatoire ou non
randomSelection = False

# Tests des méthodes de util.py
if (testUT) :
    # Génération de graphe aléatoire
    g1 = ut.generationMultigraphe(40,60,25)

    # Génération de graphe depuis un fichier texte
    g2 = ut.acquisitionGraphe("Repertoire_Graphes/exempleGraphe.txt")

    # Transformation d'un graphe en graphe transformé (utilisé pour les méthodes du fichier algorithmeChemin utilisant les graphes transformés)
    g3 = ut.transformeGraphe(g2, sortantUniquement=True)

#######################################################################################################
# TEST DE CALCUL DES CHEMINS AVEC LES ALGORITHMES
#######################################################################################################    

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

#######################################################################################################
# TEST DE CALCUL DES CHEMINS AVEC L'OPTIMISATION
#######################################################################################################

# Tests des méthodes de optimisation.py
if (testOPT) :
    oG = g2 # Graphe d'origine que nous allant transformer pour obtenir un graphe utilisable dans l'optimisation

    # On choisit les sommets allant être utilisés dans les tests ci-dessous
    if (randomSelection) :
        start = list(oG.keys())[rand.randint(0, len(list(oG.keys())) - 1)]
        end = list(oG.keys())[rand.randint(0, len(list(oG.keys())) - 1)]
    else :
        start = 'a'
        end = 'z'

    # On crée le graphe allant être utilisé
    G = ut.transformeGrapheOptimisation(oG, start)

    # On affiche l'état du graphe utilisé
    # print("Le graphe utilisé est de la forme :")
    # for i in list(G.keys()) :
    #     print(i, G[i])
    # print()

    # Résolution par optimisation
    opt.PlusCourtChemin(G, start, end)

#######################################################################################################
# COMPARAISONS D'ALGORITHMES
#######################################################################################################

# On vérifie si on effectue ou non les tests de comparaison
if (testComp) :

    # On crée une variable représentant le nombre de graphe différents que nous allons utiliser
    numberG = 3

    # On réalise une série de calculs de n chemins et on sauvegarde le temps de calcul pour l'algorithme Type4 et l'optimisation
    nTest = 3
    optTime = []
    optPath = []
    algTime = []
    algPath = []

    # Variable de sauvegarde des chemins et du temps
    execTime = 0
    pathStudied = []

    # On effectue la série de tests
    for n in range(numberG) :
        # On récupère le graphe venant d'un fichier du répertoire Répertoires_Graphes ou on le crée de manière aléatoire
        g6 = ut.generationMultigraphe(10 * (n + 1), 15 * (n + 1), 5 * (n + 1))
        # g6 = ut.acquisitionGraphe("Repertoire_Graphes/exempleGraphe.txt")

        # On prépare le graphe allant être utilisé par l'algorithme
        algG = ut.transformeGraphe(g6, sortantUniquement=True)

        for i in range(nTest) :
            # On choisit 2 sommets du graphe au hasard avec la condition qu'il existe un chemin entre eux
            start = list(g6.keys())[rand.randint(0, len(list(g6.keys())) - 1)]
            end = list(g6.keys())[rand.randint(0, len(list(g6.keys())) - 1)]

            while (ut.testExistanceChemin(g6, start, end) == False) :
                start = list(g6.keys())[rand.randint(0, len(list(g6.keys())) - 1)]
                end = list(g6.keys())[rand.randint(0, len(list(g6.keys())) - 1)]

            # On ajoute le chemin à la liste
            pathStudied.append("Chemin de " + str(start) + " à " + str(end))

            # On calcule le temps d'exécution pour l'algorithme
            execTime = time.time()
            res = ach.cheminPlusCourt(algG, start, end)
            execTime = time.time() - execTime

            # On sauvegarde les résultats
            algPath.append(res)
            algTime.append(execTime)

            # On prépare le graphe allant être utilisé par la résolution par optimisation
            optG = ut.transformeGrapheOptimisation(g6, start)

            # On calcule le temps d'exécution
            execTime = time.time()
            res = opt.PlusCourtChemin(optG, start, end, printInfos=False)
            execTime = time.time() - execTime

            # On sauvegarde les résultats
            optPath.append(res)
            optTime.append(execTime)

        # On affiche les résultats
        # On affiche les dimensions du graphe
        print("Dimension du graphe\nNombre de sommets = " + str(10 * (n + 1)) + " - Nombre d'arcs = " + str(15 * (n + 1)) + " - Nombre de jours maximum =" + str(5 * (n + 1)) + "\n")

        # On affiche tous les résultats de l'algorithme
        print("Résultats de l'algorithme :")
        print("Chemin recherché\t\tTemps d'exécution\t\tSolution")
        for i in range(nTest) :
            print(pathStudied[i], "\t\t", "{:.6f}".format(algTime[i]), "\t\t", algPath[i])
        print()

        # On affiche les résultats pour l'optimisation
        print("Résultats de l'optimisation :")
        print("Chemin recherché\t\tTemps d'exécution\t\tSolution")
        for i in range(nTest) :
            print(pathStudied[i], "\t\t", "{:.6f}".format(optTime[i]), "\t\t", optPath[i])
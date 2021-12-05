


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

#######################################################################################################
# TESTS DES METHODES
#######################################################################################################

testUT = True
testACH = True
testOPT = True

# Tests des méthodes de util.py
if (testUT) :
    # Génération de graphe aléatoire
    g1 = ut.generationMultigraphe(10,15,10)

    # Génération de graphe depuis un fichier texte
    g2 = ut.acquisitionGraphe("Repertoire_Graphes/exempleGraphe.txt")

    # Transformation d'un graphe en graphe transformé (utilisé pour les méthodes du fichier algorithmeChemin utilisant les graphes transformés)
    g3 = ut.transformeGraphe(g2, sortantUniquement=True)

    # Transformation d'un graphe en graphe condensé dans le temps
    g4 = ut.transformeGrapheCondense(g2)
    

# Tests des méthodes de algorithmesChemin.py
if (testACH) :
    # On choisit les sommets allant être utilisés dans les tests ci-dessous
    start = 'a'
    end = 'k'

    # On affiche l'état du graphe utilisé
    print("Le graphe utilisé est de la forme :")
    for i in list(g3.keys()) :
        print(i, g3[i])
    print()

    # Test des méthodes utilisant les graphes transformés
    # Algorithme de chemin d'arrivée au plus tôt
    print("Graphe transformé - Un chemin d'arrivée au plus tôt entre", start, "et", end, "est :", ach.cheminArriveeAuPlusTot(g3, 'a', 'k'), "\n")

    # Algorithme de chemin de départ au plus tard
    print("Graphe transformé - Un chemin de départ au plus tard entre", start, "et", end, "est :", ach.cheminDepartAuPlusTard(g3, 'a', 'k'), "\n")

    # Algorithme de chemin le plus rapide
    print("Graphe transformé - Un chemin le plus rapide entre", start, "et", end, "est :", ach.cheminPlusRapide(g3, 'a', 'k'), "\n")

    # Algorithme de plus court chemin
    print("Graphe transformé - Le plus court chemin entre", start, "et", end, "est :", ach.cheminPlusCourt(g3, 'a', 'k'), "\n")

# Tests des méthodes de optimisation.py
if (testOPT) :
    # On choisit les sommets allant être utilisés dans la résolution par optimisation
    start = 'a'
    end = 'k'

    # On affiche l'état du graphe utilisé
    print("Le graphe utilisé est de la forme :")
    for i in list(g4.keys()) :
        print(i, g4[i])
    print()

    # Résolution par optimisation
    opt.optPlusCourtChemin(g4, start, end)
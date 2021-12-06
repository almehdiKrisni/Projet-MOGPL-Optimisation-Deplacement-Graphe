


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
import sys

#######################################################################################################
# PARTIE EXECUTABLE
#######################################################################################################

# Dans le main, on fait appel par paramètre à un fichier dans lequel se trouve un graphe au format texte
# On effectue ensuite le calcul des 4 types de chemin avec ce graphe pour des sommets que l'on passe en paramètre

# Le format de l'exécution du fichier 'main.py' doit être de la forme :
# python main.py 'filepath' 'name of start node' 'name of end node'

# On s'occupe de vérifier que le bon nombre de paramètres a été donné
if (len(sys.argv) != 4) :
    print("Le format de l'exécution du fichier 'main.py' doit être de la forme :\npython main.py 'filepath' 'name of start node' 'name of end node'")
    exit(-1)
filename = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]

# On lit le fichier et créer le graphe au format dictionnaire
G = ut.acquisitionGraphe(filename)
G = ut.transformeGraphe(G)

# Présentation
print("KRISNI Almehdi et ABREU Hugo - PROJET MOGPL 2021 GROUPE 3\n")
print("Le graphe utilisé est lié au fichier lié au path :", filename)
print("Calcul du chemin entre", start, "et", end, "avec différents algorithmes de recherches :\n")

# Algorithme de chemin d'arrivée au plus tôt
print("Graphe transformé - Un chemin d'arrivée au plus tôt entre", start, "et", end, "est :", ach.cheminArriveeAuPlusTot(G, start, end), "\n")

# Algorithme de chemin de départ au plus tard
print("Graphe transformé - Un chemin de départ au plus tard entre", start, "et", end, "est :", ach.cheminDepartAuPlusTard(G, start, end), "\n")

# Algorithme de chemin le plus rapide
print("Graphe transformé - Un chemin le plus rapide entre", start, "et", end, "est :", ach.cheminPlusRapide(G, start, end), "\n")

# Algorithme de plus court chemin
print("Graphe transformé - Le plus court chemin entre", start, "et", end, "est :", ach.cheminPlusCourt(G, start, end), "\n")

# Fin du main
exit(0)
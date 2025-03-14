from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
from pprint import pprint

# Fonction pour créer un taux de survie en fonction de l'âge
def createSurvivalRate():
    a = 2.478
    b = -0.8764
    h = [float(0) for _ in range(10)]
    for i in range(10):
        h[i] = abs(a * b * (i + 1) ** (b - 1))  # Calcul basé sur une formule mathématique
    ecart = (0.95 - h[1]) / 2  # Ajustement du premier taux pour éviter une chute brutale
    h[0] = 0.95 - ecart
    deathRate = {0: 0.75, 70: 0}  # Définition des taux de décès pour les âges spécifiques
    deathRate.update(dict(zip([i for i in range(60, 70)], h)))  # Ajout des taux calculés
    deathRate.update({key: 0.95 for key in range(1, 60)})  # Taux de survie constant avant 60 ans
    return deathRate

if __name__ == "__main__":
    # Création des taux de survie
    values = createSurvivalRate()
    survivalRate = 1  # Probabilité initiale de survie (100%)
    survivalPerYear = {}  # Stockage des taux de survie cumulés par année
    
    # Calcul de la probabilité de survie cumulative
    for i in range(61):
        survivalRate *= values[i]
        survivalPerYear[i] = survivalRate
    
    pprint(survivalPerYear)  # Affichage des résultats

    # Conversion des données en DataFrame pour une meilleure visualisation
    df = pd.DataFrame(list(survivalPerYear.items()), columns=["Year", "Survival Rate"])
    
    # Tri des données par année (optionnel, utile si le dictionnaire n'était pas ordonné)
    df = df.sort_values(by="Year").reset_index(drop=True)
    
    # Affichage d'un graphique en nuage de points du taux de survie
    df.plot.scatter(x="Year", y="Survival Rate", title="Taux de survie par année")
    print(df)  # Affichage du DataFrame
    plt.show()  # Affichage du graphique

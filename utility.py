import matplotlib.pyplot as plt
import random
from pprint import pprint
# 
# Fonction de Bernoulli pour simuler un événement aléatoire avec une probabilité donnée
def bernoulli(probability):
    return random.random() < probability

# Fonction pour afficher les graphiques à partir d'un DataFrame
def showGraphs(df):
    print(df.to_string())
    print(df.columns)
    df.plot.scatter(x='Age', y='Total Number', title="Année 1")
    df.plot.scatter(x='Age.1', y='Total Number.1', title="Année 2")
    plt.show()

# Constantes définissant la population et le taux de naissance
POPULATION_1 = 2486
POPULATION_2 = 2325
POPULATION_TOTALE = 11000
BIRTH_RATE = 2 / 7
AJUSTEMENT_TIME = 200
AJUSTEMENT_RATE = 0.001

# Fonction pour créer un taux de survie des éléphants en fonction de l'âge
def createSurvivalRate():
    a = 2.478
    b = -0.8764
    h = [float(0) for _ in range(10)]
    for i in range(10):
        h[i] = abs(a * b * (i + 1) ** (b - 1))
    ecart = (0.95 - h[1]) / 2
    h[0] = 0.95 - ecart
    deathRate = {0: 0.75, 70: 0}
    deathRate.update(dict(zip([i for i in range(60, 70)], h)))
    deathRate.update({key: 0.95 for key in range(1, 60)})
    return deathRate



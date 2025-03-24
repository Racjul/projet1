#Application permettant de calculer le nombre de dards à distribuer
import pandas as pd
import matplotlib.pyplot as plt
import random
import copy
from population import Population
from elephant import Elephant
import math
from utilities import *

if __name__ == "__main__":
    # Lecture des données initiales depuis un fichier CSV
    df = pd.read_csv('elephants.csv')
    df = df.drop(str(df.columns[4]), axis=1)  # Suppression d'une colonne inutile
    population = Population()

    # Calcul de la distribution d'âge de la population initiale
    for index, row in df.iterrows():
        population.distribution[row["Age"]] = (row["Total Number"] + row["Total Number.1"]) / (POPULATION_1 + POPULATION_2)

    # Remplit la population de départ en fonction de la distribution d'âge
    for age in population.distribution:
        for x in range(math.ceil(population.distribution[age] * 11000)):
            population.add(Elephant(age, random.randint(0, 1)))
    population.defaultLenght = population.lenght()

    ajustement = population.findAjustement()

    # Trouve le nombre de dards
    nbFecund = population.findFecundNumber()
    nbDard = BIRTH_RATE*nbFecund - ajustement*nbFecund
    print("Nombre d'éléphant fertile:", nbFecund)
    print("Nombre de dards:", nbDard)



    

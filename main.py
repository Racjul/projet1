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

    # Trouve le nombre de dards 
    nbFecund = population.findFecundNumber()
    nbDard = BIRTH_RATE*nbFecund - AJUSTED_RATE*nbFecund

    #Ajuste le taux manuellement suite aux tests
    #Cela évite de refaire les calculs à chaque fois
    #population.setAjustement(BIRTH_RATE-AJUSTED_RATE)

    #Crée des copies de la population
    copyA = copy.deepcopy(population)
    copyB = copy.deepcopy(population)
    copyC = copy.deepcopy(population)

    #Extermination des populations
    copyA.exterminate(8000)
    copyB.exterminate(5000)
    copyC.exterminate(3000)


    #Trouve le nombre de d'élephants fertiles
    nbFecundA = population.findFecundNumber()
    nbFecundB = population.findFecundNumber()
    nbFecundC = population.findFecundNumber()

    #Ajuste le birth rate en fonction du nombre de dard initial
    # A décommenter pour les simulations avec contrôle non proportionné
    #copyA.setAjustement(BIRTH_RATE-nbDard/nbFecundA)
    #copyB.setAjustement(BIRTH_RATE-nbDard/nbFecundB)
    #copyC.setAjustement(BIRTH_RATE-nbDard/nbFecundB)


    # Simulation de la population sur 100 ans
    for i in range(400):
        print(f"Année {i}")
        copyA.passYear()
        copyB.passYear()
        copyC.passYear()
        if(copyA.lenght() >= 10900):
            copyA.setAjustement(BIRTH_RATE-AJUSTED_RATE)
        if(copyB.lenght() >= 10900):
            copyB.setAjustement(BIRTH_RATE-AJUSTED_RATE)
        if(copyC.lenght() >= 10900):
            copyC.setAjustement(BIRTH_RATE-AJUSTED_RATE)
        #Sauvegarde les données à l'année
        copyA.numberElephant[i+1] = copyA.lenght()
        copyB.numberElephant[i+1] = copyB.lenght()
        copyC.numberElephant[i+1] = copyC.lenght()

    # Affichage des populations finales
    dfA = pd.DataFrame(copyA.numberElephant.items())
    dfB = pd.DataFrame(copyB.numberElephant.items())
    dfC = pd.DataFrame(copyC.numberElephant.items())

    dfA.columns = ['Année', 'Éléphants']
    dfB.columns = ['Année', 'Éléphants']
    dfC.columns = ['Année', 'Éléphants']

    plt.scatter(x=dfA["Année"], y=dfA["Éléphants"],color='g', label="Population initiale 3000")
    plt.scatter(x=dfB["Année"], y=dfB["Éléphants"],color='b', label="Population initiale 6000")
    plt.scatter(x=dfC["Année"], y=dfC["Éléphants"], color='r',label="Population initiale 8000")

    plt.tight_layout()
    plt.xlabel('Année')
    plt.ylabel('Nombre d\'éléphants')
    plt.legend()
    plt.title("Nombre d'éléphants en fonction du temps avec contrôle à partir de la population ciblée")

    plt.show()


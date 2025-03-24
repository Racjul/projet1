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

    # Affichage de la population initiale
    population.addSuperimposeGraph("année 0")
    #population.saveState()


    # Trouve le nombre de dards
    nbFecund = population.findFecundNumber()
    nbDard = BIRTH_RATE*nbFecund - AJUSTED_RATE*nbFecund
    print("Nombre d'éléphant fertile:", nbFecund)
    print("Nombre de dards:", nbDard)

    #Permet de trouver l'ajustement du taux de naissance et l'ajuste
    #population.findAjustement()

    #Ajuste le taux manuellement suite aux tests
    #Cela évite de refaire les calculs à chaque fois
    population.setAjustement(BIRTH_RATE-AJUSTED_RATE)

    #Extermination de la population
    #for _ in range(8000):
    #   population.killRandomElephant()

    #Calcul dajustement du birth rate avec le nb de dard
    #nbFecund = population.findFecundNumber()
    #population.setAjustement(BIRTH_RATE-nbDard/nbFecund)
    #print(population.ajustement)

    #count = 0
    #while(True):
    #    if(population.lenght() >= 10900):
    #        break
    #    population.passYear()
    #    population.numberElephant[count] = population.lenght()
    #    count+=1

    # Simulation de la population sur 100 ans
    for i in range(100):
        population.passYear()
        print(f"Année {i}")
        #if(population.lenght() >= 10900):
            #population.setAjustement(BIRTH_RATE-AJUSTED_RATE)
        #Sauvegarde les données à l'année
        if(i==29):
            population.addSuperimposeGraph("année 30")
        if(i==59):
            population.addSuperimposeGraph("année 60")
        population.numberElephant[i+1] = population.lenght()

    population.showSuperimposeGraph("Courbe démographique avec dard")
    # Affichage de la population finale
    #df = pd.DataFrame(population.numberElephant.items())
    #population.saveState()
    #df.columns = ['Année', 'Éléphants']
    #df.plot.scatter(x="Année", y="Éléphants", title=f"Éléphant par année (En distribuant les dards à partir de 10900 éléphants)")
    #population.showInfo()

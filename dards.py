#Application permettant de calculer le nombre de dards à distribuer
import pandas as pd
import matplotlib.pyplot as plt
import random
import copy
from population import Population
from elephant import Elephant
import math
from utilities import *
AJUSTED_RATE_A = 0.20971428571428563
AJUSTED_RATE_B =0.2757142857142857
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

    copyA = copy.deepcopy(population)
    copyB = copy.deepcopy(population)

    population.setAjustement(BIRTH_RATE-AJUSTED_RATE)
    copyA.setAjustement(BIRTH_RATE-AJUSTED_RATE_A)
    copyB.setAjustement(BIRTH_RATE-AJUSTED_RATE_B)
    pprint(population.survivalRate)
    for key in copyA.survivalRate:
        if copyA.survivalRate[key] != 0:
            copyA.survivalRate[key] += 0.005
    for key in copyB.survivalRate:
        if copyB.survivalRate[key] >= 0.005:
            copyB.survivalRate[key] -= 0.005
    pprint(population.survivalRate)
    #ajustement = population.findAjustement()
    #
    # Trouve le nombre de dards
    nbFecund = population.findFecundNumber()
    # ajustedRate =  BIRTH_RATE - ajustement

    #print("Nombre d'éléphant fertile:", nbFecund)
    #print("Nombre de dards:", nbDard)
 # Simulation de la population sur 100 ans
    for i in range(60):
        print(f"Année {i}")
        population.passYear()
        copyA.passYear()
        copyB.passYear()
        #Sauvegarde les données à l'année
        copyA.numberElephant[i+1] = copyA.lenght()
        copyB.numberElephant[i+1] = copyB.lenght()
        population.numberElephant[i+1] = population.lenght()

    df = pd.DataFrame.from_records([s.to_dict() for s in population.liste])
    df_count = df['age'].value_counts().reset_index()
    df_count.columns = ['age', 'percentage']
    total_population = df_count['percentage'].sum()
    df_count['percentage'] = df_count['percentage'] / total_population * 100


    dfA = pd.DataFrame.from_records([s.to_dict() for s in copyA.liste])
    df_countA = dfA['age'].value_counts().reset_index()
    df_countA.columns = ['age', 'percentage']
    total_population = df_countA['percentage'].sum()
    df_countA['percentage'] = df_countA['percentage'] / total_population * 100


    dfB= pd.DataFrame.from_records([s.to_dict() for s in copyB.liste])
    df_countB = dfB['age'].value_counts().reset_index()
    df_countB.columns = ['age', 'percentage']
    total_population = df_countB['percentage'].sum()
    df_countB['percentage'] = df_countB['percentage'] / total_population * 100
    plt.scatter(x=df_countA["age"], y=df_countA["percentage"],color='g', label="Taux de survie +0.005")
    plt.scatter(x=df_countB["age"], y=df_countB["percentage"],color='b', label=" Taux de survie -0.005")
    plt.scatter(x=df_count["age"], y=df_count["percentage"], color='r',label="Taux de survie initiale")

    plt.tight_layout()
    plt.xlabel('Âge')
    plt.ylabel('Pourcentage')
    plt.legend()
    plt.title("Propotion de la population en fonction de l'âge avec différents taux de survie")
    plt.show()
 # Affichage des populations finales
    # dfA = pd.DataFrame(copyA.numberElephant.items())
    # dfB = pd.DataFrame(copyB.numberElephant.items())
    # dfC = pd.DataFrame(population.numberElephant.items())
    #
    # dfA.columns = ['Année', 'Éléphants']
    # dfB.columns = ['Année', 'Éléphants']
    # dfC.columns = ['Année', 'Éléphants']
    #
    # plt.scatter(x=dfA["Année"], y=dfA["Éléphants"],color='g', label="Taux de survie +0.005")
    # plt.scatter(x=dfB["Année"], y=dfB["Éléphants"],color='b', label=" Taux de survie -0.005")
    # plt.scatter(x=dfC["Année"], y=dfC["Éléphants"], color='r',label="Taux de survie initiale")
    #
    # plt.tight_layout()
    # plt.xlabel('Année')
    # plt.ylabel('Nombre d\'éléphants')
    # plt.legend()
    # plt.title("Nombre d'éléphants en fonction du temps avec différents taux de survie")
    #
    # plt.show()


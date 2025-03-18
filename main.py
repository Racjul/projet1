import pandas as pd
import matplotlib.pyplot as plt
import random
import math
from pprint import pprint
import copy
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
AJUSTEMENT_TIME = 300
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

# Classe représentant un éléphant avec un âge et un sexe
class Elephant:
    def __init__(self, age, sexe) -> None:
        self.age = age
        self.sexe = sexe  # 1 pour mâle, 0 pour femelle
        self.dard = False

    def __str__(self):
        return "Age:" + str(self.age) + ", Sexe:" + str(self.sexe)

    def to_dict(self):
        return {
            "age": self.age,
            "sexe": self.sexe,
            "dard": self.dard
        }

# Classe représentant la population d'éléphants et sa dynamique au fil des ans
class Population:
    def __init__(self) -> None:
        self.liste = []  # Liste des éléphants
        self.number = 0
        self.distribution = {}  # Distribution d'âge
        self.defaultLenght = 0  # Taille initiale de la population
        self.year = 0  # Année courante
        self.survivalRate = createSurvivalRate()
        self.newElephant = {}  # Nouveau-nés par année
        self.elephantDeath = {}  # Décès par année
        self.numberElephant= {}
        self.ajustement  = 0 #Ajustement
    
    def findAjustement(self):
        count =0 
        while(True):
            self.ajustement+=AJUSTEMENT_RATE
            copyPopulation = copy.deepcopy(self)
            print("Test pour ajustement: ",   BIRTH_RATE - self.ajustement)
            while(count <= AJUSTEMENT_TIME):
                copyPopulation.passYear()
                count+=1
                if count == AJUSTEMENT_TIME and abs(copyPopulation.lenght() - population.defaultLenght) < 500:
                    print("Success")
                    print("Population initiale: ", self.defaultLenght)
                    print("Population finale: ", copyPopulation.lenght())
                    return
                if count == AJUSTEMENT_TIME and abs(copyPopulation.lenght() - population.defaultLenght) >= 500:
                    count = 0
                    print("Fail")
                    print("Population initiale: ", self.defaultLenght)
                    print("Population finale: ", copyPopulation.lenght())
                    break


    def lenght(self):
        return len(self.liste)

    def add(self, elephant):
        self.liste.append(elephant)

    # Sauvegarde l'état actuel de la population et affiche un graphique
    def saveState(self):
        df = pd.DataFrame.from_records([s.to_dict() for s in self.liste])
        df_count = df['age'].value_counts().reset_index()
        df_count.columns = ['age', 'count']
        df_count.plot.scatter(x="age", y="count", title=f"population année {self.year}")

    # Gère la mortalité des éléphants
    def death(self):
        deathCount = 0
        count = 0
        for elephant in self.liste:
            if not bernoulli(self.survivalRate[elephant.age]):
                deathCount += 1
                self.liste.pop(count)  # Supprime l'éléphant s'il ne survit pas
            else:
                elephant.age += 1  # Vieillissement des éléphants survivants
            count += 1
        self.elephantDeath[self.year] = deathCount

    # Gère les naissances dans la population
    def birth(self):
        count = 0
        for elephant in self.liste:
            if elephant.sexe == True and bernoulli(BIRTH_RATE-self.ajustement) and elephant.age >=12 and elephant.age <=60:
                if bernoulli(0.0135):  # Probabilité d'avoir un deuxième éléphant
                    count += 1
                    self.add(Elephant(0, random.randint(0, 1)))
                self.add(Elephant(0, random.randint(0, 1)))
                count += 1
        self.newElephant[self.year] = count

    # Simule le passage d'une année
    def passYear(self):
        self.birth()
        self.death()
        self.year += 1

    # Affiche les informations finales sur la population après simulation
    def showInfo(self):
        print("Nombre de nouveau-nés morts:")
        pprint(self.newElephant)
        print("Nombre d'éléphants morts:")
        pprint(self.elephantDeath)
        print(f"Population initiale: {self.defaultLenght}")
        print(f"Population finale: {self.lenght()}")
        plt.show()

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
    population.saveState()

    #Permet de trouver l'ajustement du taux de naissance et l'ajuste
    population.findAjustement()

    # Simulation de la population sur 100 ans
    for i in range(200):
        population.passYear()
        print(f"Année {i}")
        population.numberElephant[i+1] = population.lenght()


    # Affichage de la population finale
    df = pd.DataFrame(population.numberElephant.items())
    population.saveState()
    df.columns = ['Année', 'Éléphants']
    df.plot.scatter(x="Année", y="Éléphants", title=f"Croissance de la population")
    population.showInfo()
    print(BIRTH_RATE-population.ajustement)

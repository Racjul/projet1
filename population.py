import random
import copy
import pandas as pd
import matplotlib.pyplot as plt
from elephant import Elephant
from utilities import *
import copy

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
        self.numberElephant = {}
        self.ajustement = 0  # Ajustement
        self.superimposeGraph = []

    # Constructeur de copie profonde
    def __deepcopy__(self, memo):
        # Crée une nouvelle instance de Population
        new_population = Population()
    
        # Copie profonde des attributs nécessaires
        new_population.liste = copy.deepcopy(self.liste, memo)
        new_population.number = self.number
        new_population.distribution = copy.deepcopy(self.distribution, memo)
        new_population.defaultLenght = self.defaultLenght
        new_population.year = self.year
        new_population.survivalRate = copy.deepcopy(self.survivalRate, memo)
        new_population.newElephant = copy.deepcopy(self.newElephant, memo)
        new_population.elephantDeath = copy.deepcopy(self.elephantDeath, memo)
        new_population.numberElephant = copy.deepcopy(self.numberElephant, memo)
        new_population.ajustement = self.ajustement
        new_population.superimposeGraph = copy.deepcopy(self.superimposeGraph, memo)
    
        return new_population
    def findFecundNumber(self):
        count = 0
        for elephant in self.liste:
            if elephant.sexe == True and 12 <= elephant.age <= 60:
                count += 1
        return count

    def killRandomElephant(self):
        randomIndex = random.randint(0, len(self.liste) - 1)
        self.liste.pop(randomIndex)

    def exterminate(self,number):
        for _ in range(number):
            self.killRandomElephant()

    def killPercentage(self, percentage):
        to_kill = int(len(self.liste) * percentage / 100)
        self.exterminate(to_kill)
    def findAjustement(self):
        count = 0
        while True:
            self.ajustement += AJUSTEMENT_RATE
            copyPopulation = copy.deepcopy(self)
            print("Test pour ajustement: ", BIRTH_RATE - self.ajustement)
            while count <= AJUSTEMENT_TIME:
                copyPopulation.passYear()
                print(f"{count}:{copyPopulation.lenght()}")
                count += 1
                if count == AJUSTEMENT_TIME and abs(copyPopulation.lenght() - self.defaultLenght) < 500:
                    print("Success")
                    print("Population initiale: ", self.defaultLenght)
                    print("Population finale: ", copyPopulation.lenght())
                    return self.ajustement
                if count == AJUSTEMENT_TIME and abs(copyPopulation.lenght() - self.defaultLenght) >= 500:
                    count = 0
                    print("Fail")
                    print("Population initiale: ", self.defaultLenght)
                    print("Population finale: ", copyPopulation.lenght())
                    break

    def lenght(self):
        return len(self.liste)

    def add(self, elephant):
        self.liste.append(elephant)

    def setAjustement(self, ajustement):
        self.ajustement = ajustement

    def saveState(self):
        df = pd.DataFrame.from_records([s.to_dict() for s in self.liste])
        df_count = df['age'].value_counts().reset_index()
        df_count.columns = ['age', 'percentage']
        total_population = df_count['percentage'].sum()
        df_count['percentage'] = df_count['percentage'] / total_population * 100
        df_count.plot.scatter(x="age", y="percentage", title=f"Répartition de la population à l'année {self.year} avec dard", color="g")

    def death(self):
        deathCount = 0
        count = 0
        for elephant in self.liste:
            if not bernoulli(self.survivalRate[elephant.age]):
                deathCount += 1
                self.liste.pop(count)
            else:
                elephant.age += 1
            count += 1
        self.elephantDeath[self.year] = deathCount

    def birth(self):
        count = 0
        for elephant in self.liste:
            if elephant.sexe == True and bernoulli(BIRTH_RATE - self.ajustement) and 12 <= elephant.age <= 60:
                if bernoulli(0.0135):
                    count += 1
                    self.add(Elephant(0, random.randint(0, 1)))
                self.add(Elephant(0, random.randint(0, 1)))
                count += 1
        self.newElephant[self.year] = count

    def passYear(self):
        self.birth()
        self.death()
        self.year += 1

    def showInfo(self):
        print(f"Population initiale: {self.defaultLenght}")
        print(f"Population finale: {self.lenght()}")
        plt.show()

    def addSuperimposeGraph(self, label):
        df = pd.DataFrame.from_records([s.to_dict() for s in self.liste])
        df_count = df['age'].value_counts().reset_index()
        df_count.columns = ['âge', 'pourcentage']
        total_population = df_count['pourcentage'].sum()
        df_count['pourcentage'] = df_count['pourcentage'] / total_population * 100
        self.superimposeGraph.append([label, df_count.copy()])

    def showSuperimposeGraph(self, title):
        for pair in self.superimposeGraph:
            df = pair[1]
            label = pair[0]
            color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
            plt.scatter(df['âge'], df['pourcentage'], color=color, label=label)
        plt.tight_layout()
        plt.xlabel("Âge")
        plt.ylabel("Pourcentage")
        plt.legend()
        plt.title(title)
        plt.show()
    

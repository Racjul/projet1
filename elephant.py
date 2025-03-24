import random

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

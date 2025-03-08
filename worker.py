import random


class Worker:
    def __init__(self, worker_id, image):

        first_names = ["Aether", "Agnes", "Edith", "Margery", "Odilia", "Ella", "Reina",
                       "Joachim", "Alistair", "Bennett", "Conrad", "Drake", "Josh", "Percival", "Warner",
                       "Constantine", "Daisy", "Merry", "Robin", "Gregory"]
        last_names = ["Payne", "Fletcher", "Cook", "Brown", "Baker", "Bennett", "Mason", "Hughes", "Gregory", "Hayward",
                      "Forester", "Kilner", "Webster", "Wright"]

        random_gen = random.randint(0, len(first_names) - 1)
        random_gen2 = random.randint(0, len(last_names) - 1)

        self.firstname = first_names[random_gen]
        self.lastname = last_names[random_gen2]
        self.worker_id = worker_id
        self.clickingXP = 0
        self.clickingLevel = 0
        self.gatheringXP = 0
        self.gatheringLevel = 0
        self.gatheringBase = 1
        self.miningXP = 0
        self.miningLevel = 0
        self.miningBase = 0.1
        self.current_activity = "Gathering"
        self.itemLimit = 1
        self.items = []
        self.button = None
        self.name = "John Doe"
        self.icon = "N/A"
        self.image = image

    def calculate_val(self):
        if self.current_activity == "Gathering":
            return (self.gatheringLevel + 1) * self.gatheringBase
        elif self.current_activity == "Mining":
            return (self.miningLevel + 1) * self.miningBase


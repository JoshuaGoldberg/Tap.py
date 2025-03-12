import random
from item import *

class Worker:
    def __init__(self, worker_id, image, game, fps):

        first_names = ["Aether", "Agnes", "Edith", "Margery", "Odilia", "Ella", "Reina",
                       "Joachim", "Alistair", "Bennett", "Conrad", "Drake", "Josh", "Percival", "Warner",
                       "Constantine", "Daisy", "Merry", "Robin", "Gregory"]
        last_names = ["Payne", "Fletcher", "Cook", "Brown", "Baker", "Bennett", "Mason", "Hughes", "Gregory", "Hayward",
                      "Forester", "Kilner", "Webster", "Wright"]
        self.levels = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400,
                       2600, 2800, 3000,
                       3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 10000, 12000, 14000, 16000, 18000,
                       20000, 22000, 24000, 26000,
                       28000, 30000, 50000, 100000, 150000, 300000, 450000, 600000, 1000000, 1500000, 2000000, 10000000]

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
        self.game = game
        self.fps = fps

    def calculate_val(self):
        random_gen = random.randint(0, 10000)
        if self.current_activity == "Gathering":
            self.gatheringXP += (1 * self.game.gatheringXPBoost) / 10
            if self.gatheringXP >= self.levels[self.gatheringLevel]:
                self.gatheringXP = 0
                self.gatheringLevel += 1
            if random_gen == 2 and self.game.inventory_unlocked is True:
                self.game.new_item = True
                blue_item_img = pygame.image.load('assets/blue_berry.png').convert_alpha()
                BlueBerry = Item(blue_item_img, "Blue Berry",
                                 "A blue berry. "
                                 "Note: not a red berry, although it's easy to get confused",
                                 lambda: None, lambda: None, self)
                self.game.consumable_inventory.append(BlueBerry)
            return (self.gatheringLevel + 1) * self.gatheringBase
        elif self.current_activity == "Mining":
            self.miningXP += 1 / 10
            if self.miningXP >= self.levels[self.miningLevel]:
                self.miningXP = 0
                self.miningLevel += 1
            return (self.miningLevel + 1) * self.miningBase

    def get_xp_and_level(self):
        if self.current_activity == "Gathering":
            return (self.gatheringXP, self.levels[self.gatheringLevel]), self.gatheringLevel
        elif self.current_activity == "Mining":
            return (self.miningXP, self.levels[self.miningLevel]), self.miningLevel

import random
from item import *


class Worker:
    def __init__(self, worker_id, image, game, fps, item_manager):

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
        self.item_manager = item_manager

        self.firstname = first_names[random_gen]
        self.lastname = last_names[random_gen2]
        self.worker_id = worker_id
        self.clickingXP = 0
        self.clickingLevel = 0
        self.gatheringXP = 0
        self.gatheringLevel = 0
        self.working_bases = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.item_bonuses = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.miningXP = 0
        self.miningLevel = 0
        self.current_activity = "Gathering"
        self.itemLimit = 1
        self.items = [None, None, None, None, None]
        self.button = None
        self.name = "John Doe"
        self.icon = "N/A"
        self.image = image
        self.game = game
        self.fps = fps
        self.slot_count = 1
        self.equip_sound = pygame.mixer.Sound('sounds/equip.wav')
        self.total_seal_bonus = 1

    def handle_equip(self, index):
        if self.game.select_for_equip is not None:
            if self.items[index] is not None:
                self.items[index].equipped_by = None
                self.items[index] = None
            self.items[index] = self.game.select_for_equip
            self.game.select_for_equip.equipped_by = self
            self.game.select_for_equip = None
            self.equip_sound.play()
        else:
            if self.items[index] is not None:
                self.items[index].equipped_by = None
                self.items[index] = None
            else:
                if self.game.inventory_unlocked:
                    self.game.set_inventory_tab("Accessories")
                    self.game.access_inventory()

    def remove_items(self):
        for item in self.items:
            if item is not None:
                item.equipped_by = None

    def update_loot(self):
        random_gen = random.randint(0, 3)
        if self.current_activity == "Gathering":
            if random_gen == 2 and self.game.inventory_unlocked is True:
                pool = self.item_manager.gather_lp
                item = pool[random.randint(0, len(pool) - 1)]

                self.game.add_item(item)
        elif self.current_activity == "Mining":
            if random_gen == 2 and self.game.inventory_unlocked is True:
                pool = self.item_manager.mining_lp
                item = pool[random.randint(0, len(pool) - 1)]
                self.game.add_item(item)

    def update_xp(self):
        if self.current_activity == "Gathering":
            self.gatheringXP += (1 * self.game.gatheringXPBoost) / 10
            if self.gatheringXP >= self.levels[self.gatheringLevel]:
                self.gatheringXP = 0
                self.gatheringLevel += 1
        elif self.current_activity == "Mining":
            self.miningXP += 1 / 10
            if self.miningXP >= self.levels[self.miningLevel]:
                self.miningXP = 0
                self.miningLevel += 1

    def calculate_val(self):
        self.total_seal_bonus = 1
        for i in range(0, len(self.item_bonuses)):
            self.item_bonuses[i] = 1
        for item in self.items:
            if isinstance(item, Item):
                self.total_seal_bonus += item.calculate_seal_bonus()
        for item in self.items:
            if isinstance(item, Item):
                for effect in item.equip_action:
                    effect.action(self)
                for seal in item.seals:
                    if isinstance(seal, EffectSeal):
                        for effect in seal.effects:
                            effect.action(self)

        if self.current_activity == "Gathering":
            return (self.gatheringLevel + 1) * self.working_bases[0] * self.item_bonuses[0]
        elif self.current_activity == "Mining":
            return (self.miningLevel + 1) * self.working_bases[1] * self.item_bonuses[1]

    def get_xp_and_level(self):
        if self.current_activity == "Gathering":
            return (self.gatheringXP, self.levels[self.gatheringLevel]), self.gatheringLevel
        elif self.current_activity == "Mining":
            return (self.miningXP, self.levels[self.miningLevel]), self.miningLevel

    def add_bonus_slots(self, amt):
        self.game.add_bonus_slots(amt * self.total_seal_bonus)

    def boost_stat(self, value, category):
        self.item_bonuses[category] *= (value * self.total_seal_bonus)

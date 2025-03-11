import pygame
from worker import Worker
from upgradeDefinitions import get_upgrades
import random
from item import Item


class Game:

    def __init__(self, width, height, fps):
        self.fps = fps
        self.width = width
        self.height = height
        self.value = 0
        self.total_value = 0
        self.base_click = 100000
        self.click_power = 1
        self.base_click_progress = 0
        self.click_progress = 0
        self.workers_enabled = False
        self.workers = []
        self.curr_id = 0
        self.worker_page = 1
        self.selectedWorker = None
        self.gatheringXPBoost = 1
        self.unlockedRenown = False
        self.renown = 0
        self.layer = 0
        self.layers = []
        self.inventory_page = 1
        blue_item_img = pygame.image.load('assets/blue_berry.png').convert_alpha()
        strange_rock_img = pygame.image.load('assets/strange_rock.png').convert_alpha()

        BlueBerry = Item(blue_item_img, "Blue Berry",
                         "A blue berry. "
                         "Note: not a red berry, although it's easy to get confused",
                         lambda: None, lambda: None, self)
        StrangeRock = Item(strange_rock_img, "Strange Rock",
                           "Should it look like this? It really shouldn't look like this."
                           " Really I wouldn't trust a rock that looks like that something is most certainly off."
                           " The last guy who touched a rock like that vanished without a trace, that's all I'll say."
                           " But hey, it's your life, touch the rock, see what I care.",
                           lambda: None, lambda: None, self)
        BlueBerry2 = Item(blue_item_img, "Bluer Berry", "A bluer berry. Maybe don't trust this one. Bad vibes.",
                          lambda: None, lambda: None, self)

        self.accessories_inventory = []
        self.item_inventory = [StrangeRock]
        self.consumable_inventory = []
        self.INVENTORY_LAYER = 1
        self.inventory_tab = "Accessories"
        self.inventory_unlocked = False
        self.max_workers = 10
        self.selected_item = None

        self.upgrades = []
        self.future_upgrades, self.bought_upgrades = get_upgrades()

    def inv_back(self):
        if self.inventory_page > 1:
            self.inventory_page -= 1

    def inv_forward(self):
        curr_tab = "Accessories"
        if self.inventory_tab == "Accessories":
            curr_tab = self.accessories_inventory
        elif self.inventory_tab == "Items":
            curr_tab = self.item_inventory
        elif self.inventory_tab == "Consumables":
            curr_tab = self.consumable_inventory

        if len(curr_tab) > self.inventory_page * 40:
            self.inventory_page += 1

    def set_inventory_tab(self, tab_name):
        self.inventory_tab = tab_name
        self.inventory_page = 1

    def get_total_levels(self, activity):
        total = 0
        for worker in self.workers:
            if activity == "Gathering":
                total += worker.gatheringLevel
        return total

    def update_clicks(self, amount):
        self.value += amount
        self.total_value += amount

    def double_base_clicks(self):
        self.base_click *= 2
        self.base_click_progress += 1

    def double_gathering_xp(self):
        self.gatheringXPBoost *= 2

    def increase_click_power(self):
        self.click_power += 1
        self.click_progress += 1

    def enable_workers(self):
        self.workers_enabled = True

    def access_inventory(self):
        if self.layer == 0:
            self.inventory_page = 1
            self.layers.insert(0, self.INVENTORY_LAYER)
        elif self.layer == 1:
            self.layers.pop(0)

    def exit_layer(self):
        if len(self.layers) > 0:
            self.layers.pop(0)

    def unlock_inventory(self):
        self.inventory_unlocked = True

    def set_selected_item(self, item):
        self.selected_item = item

    def add_worker(self):
        cost = int(100 * (1.1 ** len(self.workers)))

        random_face = random.randint(1, 4)
        worker_face_string = 'null'
        if random_face == 1:
            worker_face_string = 'assets/workerIcon.png'
        elif random_face == 2:
            worker_face_string = 'assets/worker_red.png'
        elif random_face == 3:
            worker_face_string = 'assets/worker_blue.png'
        elif random_face == 4:
            worker_face_string = 'assets/worker_green.png'

        if self.value >= cost and len(self.workers) < self.max_workers:
            self.value -= cost
            worker_img = pygame.image.load(worker_face_string).convert_alpha()
            worker = Worker(self.curr_id, worker_img, self, self.fps)
            self.workers.append(worker)
            self.curr_id += 1

    def sell_worker(self, worker):

        index = 0
        for worker2 in self.workers:
            if worker2 == worker:
                break
            else:
                index += 1

        self.workers.remove(worker)

        if len(self.workers) >= index + 1:
            self.selectedWorker = self.workers[index]
        else:
            self.selectedWorker = None

    def process_upgrade(self, upgrade):
        if self.value >= upgrade.cost:
            self.value -= upgrade.cost
            upgrade.execute(self)
            self.upgrades.remove(upgrade)
            self.bought_upgrades.append(upgrade)

    def select_worker(self, worker):
        self.selectedWorker = worker

    def set_worker_status(self, status):
        self.selectedWorker.current_activity = status

    def forward_page(self):
        if len(self.workers) > self.worker_page * 45:
            self.worker_page += 1

    def back_page(self):
        if self.worker_page > 1:
            self.worker_page -= 1

    def update(self):
        if len(self.layers) > 0:
            self.layer = self.layers[0]
        else:
            self.layer = 0

        for worker in self.workers:
            self.value += worker.calculate_val() / 10

        self.check_upgrades()

    def check_upgrades(self):

        for upgrade in self.future_upgrades:
            if self.total_value >= 50:
                if upgrade.name == "Iron Grip":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

            if self.total_value >= 250:
                if self.base_click_progress >= 1:
                    if upgrade.name == "Magic Stones":
                        self.future_upgrades.remove(upgrade)
                        self.upgrades.append(upgrade)

                    if upgrade.name == "Strength Training":
                        self.future_upgrades.remove(upgrade)
                        self.upgrades.append(upgrade)

            if self.total_value >= 1000:
                if any(upgrade2.name == "Strength Training" for upgrade2 in self.bought_upgrades):
                    if upgrade.name == "Medicinal Herbs":
                        self.future_upgrades.remove(upgrade)
                        self.upgrades.append(upgrade)

            if self.total_value >= 5000:
                if any(upgrade2.name == "Medicinal Herbs" for upgrade2 in self.bought_upgrades):
                    if upgrade.name == "Multi-finger mode":
                        self.future_upgrades.remove(upgrade)
                        self.upgrades.append(upgrade)

            if self.total_value >= 12000:
                if upgrade.name == "Job Listings":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

            if self.total_value >= 7500 and self.workers_enabled is True and self.get_total_levels("Gathering") >= 5:
                if upgrade.name == "Berry Baskets":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

            if self.value >= 2500 and self.workers_enabled is True:
                if upgrade.name == "Personal Chest":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

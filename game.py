import pygame
from worker import Worker
from upgradeDefinitions import get_upgrades
import random


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

        self.upgrades = []
        self.future_upgrades, self.bought_upgrades = get_upgrades()

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

        if self.value >= cost:
            self.value -= cost
            worker_img = pygame.image.load(worker_face_string).convert_alpha()
            worker = Worker(self.curr_id, worker_img, self, self.fps)
            self.workers.append(worker)
            self.curr_id += 1

    def sell_worker(self, worker):
        self.workers.remove(worker)
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
            self.value += worker.calculate_val() / self.fps

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

            if self.total_value >= 7500 and self.workers_enabled is True:
                if upgrade.name == "Berry Baskets":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

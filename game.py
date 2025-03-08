import pygame
from worker import Worker
from upgradeDefinitions import get_upgrades
import random


class Game:
    def __init__(self, width, height):
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

        self.upgrades = []
        self.future_upgrades, self.bought_upgrades = get_upgrades()

    def update_clicks(self, amount):
        self.value += amount
        self.total_value += amount

    def double_base_clicks(self):
        self.base_click *= 2
        self.base_click_progress += 1

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
            worker = Worker(self.curr_id, worker_img)
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

        for worker in self.workers:
            self.value += worker.calculate_val() / 60

        self.check_upgrades()

    def check_upgrades(self):

        if self.total_value >= 50:
            for upgrade in self.future_upgrades:
                if upgrade.name == "Iron Grip":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

        if self.total_value >= 250:
            if self.base_click_progress >= 1:
                for upgrade in self.future_upgrades:
                    if upgrade.name == "Magic Stones":
                        self.future_upgrades.remove(upgrade)
                        self.upgrades.append(upgrade)

            for upgrade in self.future_upgrades:
                if upgrade.name == "Strength Training":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

        if self.total_value >= 1000:
            if any(upgrade.name == "Strength Training" for upgrade in self.bought_upgrades):
                for upgrade in self.future_upgrades:
                    if upgrade.name == "Medicinal Herbs":
                        self.future_upgrades.remove(upgrade)
                        self.upgrades.append(upgrade)

        if self.total_value >= 5000:
            if any(upgrade.name == "Medicinal Herbs" for upgrade in self.bought_upgrades):
                for upgrade in self.future_upgrades:
                    if upgrade.name == "Multi-finger mode":
                        self.future_upgrades.remove(upgrade)
                        self.upgrades.append(upgrade)

        if self.total_value >= 12000:
            for upgrade in self.future_upgrades:
                if upgrade.name == "Job Listings":
                    self.future_upgrades.remove(upgrade)
                    self.upgrades.append(upgrade)

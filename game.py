import copy

import pygame

import itemDefinitions
from worker import Worker
from upgradeDefinitions import get_upgrades
import random
from itemDefinitions import *
import time
from datetime import datetime, timedelta


class Game:

    def __init__(self, width, height, fps):
        self.number_titles = ["Million", "Billion", "Trillion",
                              "Quadrillion", "Quintillion", "Sextillion",
                              "Septillion", "Octillion", "Nonillion",
                              "Decillion", "Undecillion", "Duodecillion",
                              "Tredecillion", "Quattuordecillion",
                              "Quindecillion", "Sexdecillion",
                              "Septdecillion", "Octodecillion",
                              "Novemdecillion", "Vigintillion"]
        self.fps = fps
        self.width = width
        self.height = height
        self.value = 0
        self.total_value = 0
        self.base_click = 100000000
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
        self.new_item = False
        blue_item_img = pygame.image.load('assets/blue_berry.png').convert_alpha()
        strange_rock_img = pygame.image.load('assets/strange_rock.png').convert_alpha()

        BlueBerry = Item(blue_item_img, "Blue Berry",
                         "A blue berry. "
                         "Note: not a red berry, although it's easy to get confused", "Consumables",
                         lambda: None, lambda: None, 10)
        StrangeRock = Item(strange_rock_img, "Strange Rock",
                           "Should it look like this? It really shouldn't look like this."
                           " Nothing good could ever happen by keeping this around, I'm sure of it.",
                           "Items",
                           lambda: None, lambda: None, 50)
        BlueBerry2 = Item(blue_item_img, "Bluer Berry",
                          "A bluer berry. Maybe don't trust this one. Bad vibes.",
                          "Consumables",
                          lambda: None, lambda: None, 10)

        self.game_items = ItemsManager(self)
        self.accessories_inventory = [StrangeRock, self.game_items.item_list["Dev Shovel"]]
        self.item_inventory = {}
        self.consumable_inventory = {}
        self.INVENTORY_LAYER = 1
        self.SHOP_LAYER = 2
        self.inventory_tab = "Accessories"
        self.inventory_unlocked = False
        self.max_workers = 10
        self.selected_item = None
        self.seals_inventory = []
        self.seal_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.seal_positions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.upgrades = []
        self.future_upgrades, self.bought_upgrades = get_upgrades()
        self.select_for_equip = None
        self.interval = 0.1
        self.current_time = datetime.now()
        self.next_event_time = (self.current_time + timedelta(minutes=self.interval)).replace(second=0, microsecond=0)
        self.add_seal_menu = False
        self.shop_inventory = {StrangeRock: 5, self.game_items.item_list["Dev Shovel"]: 1, BlueBerry: 25}
        self.shop_page = 1
        self.common_items_per_restock = 5
        self.uncommon_items_per_restock = 2
        self.rare_items_per_restock = 1
        self.rare_spawn_chance = 5
        self.bonus_worker_slots = 0

        self.restock_shop()

    def format_number(self, number):
        if number > 999999:
            return self.format_number_helper(number / 1000000, 0)
        else:
            return str(number)

    def format_number_helper(self, number, acc):
        if number >= 1000:
            return self.format_number_helper(number / 1000, acc + 1)
        else:
            return str(round(number, 3)) + " " + self.number_titles[acc]

    def buy_item(self, item):
        if self.value >= item.cost:
            self.value -= item.cost
            self.add_item(item)
        if item in self.shop_inventory:
            self.shop_inventory[item] -= 1
            if self.shop_inventory[item] == 0:
                del self.shop_inventory[item]

    def add_specific_seal(self, seal):
        if seal in self.item_inventory and len(self.selected_item.seals) < 5:
            self.trash_specific_item(seal)
            self.selected_item.seals.append(seal)

    def add_specific_stamp(self, stamp):
        if stamp in self.item_inventory and len(self.selected_item.stamps) < 3:
            self.trash_specific_item(stamp)
            self.selected_item.stamps.append(stamp)

    def trash_specific_item(self, item):
        if item in self.item_inventory:
            self.item_inventory[item] -= 1
            if self.item_inventory[item] == 0:
                del self.item_inventory[item]

    def toggle_seal_add(self):
        self.add_seal_menu = not self.add_seal_menu

    def buy_seal(self, item, cost, position, seal_num):
        if self.value >= cost:
            self.add_item(item)
            self.value -= cost
            self.seal_positions.remove(position)
            del self.seals_inventory[seal_num]

    def add_via_loot_pool(self, inventory, loot_pool):

        selected_item = loot_pool[random.randint(0, len(loot_pool) - 1)]
        stop_re_roll = False

        while stop_re_roll is False:
            re_roll_chance = random.randint(0, 100)
            if re_roll_chance < selected_item[1]:
                selected_item = loot_pool[random.randint(0, len(loot_pool) - 1)]
            else:
                stop_re_roll = True

        inventory.append(selected_item[0])

    def add_to_shop(self, loot_pool, limit, rarity_scaler):
        rarity = rarity_scaler
        banned_items = []
        item_count = random.randint(1, limit)
        while item_count > 0:
            if rarity == 0 or random.randint(1, rarity) == 1:
                if len(banned_items) < len(loot_pool):
                    selected_item = loot_pool[random.randint(0, len(loot_pool) - 1)]
                    while selected_item[0] in banned_items:
                        selected_item = loot_pool[random.randint(0, len(loot_pool) - 1)]
                    self.shop_inventory.update({selected_item[0]: random.randint(1, selected_item[1])})
                    banned_items.append(selected_item[0])
            item_count -= 1
            rarity *= 2

    def restock_shop(self):
        # clear the shop, then populate with new items
        self.shop_inventory.clear()

        self.add_to_shop(self.game_items.shop_common_lp, self.common_items_per_restock, 0)
        self.add_to_shop(self.game_items.shop_uncommon_lp, self.uncommon_items_per_restock, 0)
        self.add_to_shop(self.game_items.shop_rare_lp, self.rare_items_per_restock, self.rare_spawn_chance)

        seal_count = random.randint(1, 9)
        for i in range(0, 8):
            self.seal_offsets[i][0] = random.randint(-10, 10)
            self.seal_offsets[i][1] = random.randint(-10, 10)

        self.seal_positions = random.sample(range(9), seal_count)
        for i in range(0, seal_count):

            stamp_random = random.randint(0, 10)
            if stamp_random > 2:
                self.add_via_loot_pool(self.seals_inventory, self.game_items.seal_lp)
            else:
                self.add_via_loot_pool(self.seals_inventory, self.game_items.stamp_lp)

    def close_and_select(self, worker):
        self.exit_layer()
        self.select_worker(worker)

    def add_item(self, item):
        if item.classification == "Accessories":
            self.new_item = True
            self.accessories_inventory.append(item.generate_copy())
        elif item.classification == "Items":
            if item in self.item_inventory:
                self.item_inventory[item] += 1
            else:
                self.new_item = True
                self.item_inventory.update({item: 1})
        elif item.classification == "Consumables":
            if item in self.consumable_inventory:
                self.consumable_inventory[item] += 1
            else:
                self.new_item = True
                self.consumable_inventory.update({item: 1})

    def equip_select(self, item):
        self.select_for_equip = item
        self.exit_to_base()

    def use_item(self):
        item = self.selected_item
        item.use_action()
        self.trash_item()

    def value_up(self, amt):
        self.value += amt

    def trash_item(self):
        item = self.selected_item
        tab = self.inventory_tab
        if tab == "Accessories":
            self.accessories_inventory.remove(item)
            self.selected_item = None
        elif tab == "Items":
            self.item_inventory[item] -= 1
            if self.item_inventory[item] == 0:
                del self.item_inventory[item]
                self.selected_item = None
        elif tab == "Consumables":
            self.consumable_inventory[item] -= 1
            if self.consumable_inventory[item] == 0:
                del self.consumable_inventory[item]
                self.selected_item = None

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
        self.add_seal_menu = False
        if self.layer != 1:
            if self.INVENTORY_LAYER in self.layers:
                self.layers.remove(self.INVENTORY_LAYER)

            self.new_item = False
            self.inventory_page = 1
            self.layers.insert(0, self.INVENTORY_LAYER)
        elif self.layer == 1:
            if len(self.layers) > 0:
                self.layers.pop(0)

    def access_shop(self):
        if self.layer != 2:
            if self.SHOP_LAYER in self.layers:
                self.layers.remove(self.SHOP_LAYER)

            self.layers.insert(0, self.SHOP_LAYER)
        elif self.layer == 2:
            if len(self.layers) > 0:
                self.layers.pop(0)

    def exit_layer(self):
        if len(self.layers) > 0:
            self.layers.pop(0)

    def exit_to_base(self):
        self.layers.clear()

    def unlock_inventory(self):
        self.inventory_unlocked = True

    def set_selected_item(self, item):
        self.add_seal_menu = False
        self.selected_item = item

    def add_bonus_slots(self, amt):
        self.bonus_worker_slots += amt

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

        if self.value >= cost and len(self.workers) < (self.max_workers + self.bonus_worker_slots):
            self.value -= cost
            worker_img = pygame.image.load(worker_face_string).convert_alpha()
            worker = Worker(self.curr_id, worker_img, self, self.fps, self.game_items)
            self.workers.append(worker)
            self.curr_id += 1

    def sell_worker(self, worker):

        index = 0
        for worker2 in self.workers:
            if worker2 == worker:
                break
            else:
                index += 1
        worker.remove_items()
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

    def forward_shop_page(self):
        if len(self.shop_inventory) > self.shop_page * 18:
            self.shop_page += 1

    def back_shop_page(self):
        if self.shop_page > 1:
            self.shop_page -= 1

    def update(self):

        # time based detection
        self.bonus_worker_slots = 0
        self.current_time = datetime.now()
        if self.current_time >= self.next_event_time:
            self.restock_shop()
            self.next_event_time += timedelta(minutes=self.interval)

        if len(self.layers) > 0:
            self.layer = self.layers[0]
        else:
            self.layer = 0

        for worker in self.workers:
            self.value += worker.calculate_val() / 10
            worker.update_xp()
            worker.update_loot()

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

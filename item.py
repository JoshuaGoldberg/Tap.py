import copy
import random

import pygame

from numberFormatter import format_number


class Item:
    pressed = False
    ID = 0

    def __init__(self, image, name, description, classification, use_action, equip_action, cost):
        self.classification = classification
        self.image = image
        self.name = name
        self.description = description
        self.use_action = use_action
        self.equip_action = equip_action
        self.equipped_by = None
        self.seals = []
        self.stamps = []
        self.cost = cost
        self.id = self.ID
        self.ID += 1

    def generate_copy(self):
        new_item = Item(self.image, self.name, self.description, self.classification, self.use_action,
                        self.equip_action, self.cost)
        new_item.id = self.ID
        self.ID += 1
        return new_item

    def __key(self):
        return self.name, self.description, self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.__key() == other.__key()
        return NotImplemented

    def calculate_seal_bonus(self):
        total = 0
        for seal in self.seals:
            total += seal.seal_bonus
        return total

    def provide_additional_text(self):
        if self.calculate_seal_bonus() > 0:
            return "\nSeal amplification: x" + str(self.calculate_seal_bonus() + 1)
        else:
            return ""

    def item_description_text(self):
        text = self.description
        bonus = self.calculate_seal_bonus()
        for action in self.equip_action:
            text = text + action.provide_text(bonus + 1) + "\n"
        for seal in self.seals:
            if isinstance(seal, EffectSeal):
                for effect in seal.effects:
                    text = text + effect.provide_text(bonus + 1) + "\n"
        text = text + self.provide_additional_text()

        return text


class Seal(Item):
    def __init__(self, image, name, description, classification, use_action, equip_action, cost, seal_bonus):
        super().__init__(image, name, description, classification, use_action, equip_action, cost)
        self.seal_bonus = seal_bonus

    def generate_copy(self):
        new_item = Seal(self.image, self.name, self.description, self.classification, self.use_action,
                        self.equip_action, self.cost, self.seal_bonus)
        new_item.id = self.ID
        self.ID += 1
        return new_item


class EffectSeal(Seal):
    def __init__(self, image, name, description, classification, use_action, equip_action, cost, seal_bonus,
                 effect_pool, max_effects, rand):
        super().__init__(image, name, description, classification, use_action, equip_action, cost, seal_bonus)
        self.effects = []
        self.effect_pool = effect_pool
        self.max_effects = max_effects
        self.rand = rand

    def generate_copy(self):
        new_item = EffectSeal(self.image, self.name, self.description, self.classification, self.use_action,
                              self.equip_action, self.cost, self.seal_bonus, self.effect_pool, self.max_effects,
                              self.rand)
        new_item.id = self.ID
        new_item.effects.clear()

        if self.rand:
            num_effects = random.randint(1, self.max_effects)
        else:
            num_effects = self.max_effects

        while num_effects > 0:
            selected_item = self.effect_pool[random.randint(0, len(self.effect_pool) - 1)]
            stop_re_roll = False

            while stop_re_roll is False:
                re_roll_chance = random.randint(0, 100)
                if re_roll_chance < selected_item[1]:
                    selected_item = self.effect_pool[random.randint(0, len(self.effect_pool) - 1)]
                else:
                    stop_re_roll = True

            new_item.effects.append(selected_item[0])
            num_effects -= 1

        self.ID += 1
        return new_item


class BaseBoost:
    def __init__(self, skill, category, value):
        self.skill = skill
        self.value = value
        self.action = lambda worker: worker.boost_stat(self.value, category)

    def provide_text(self, amp):
        return "Boosts base " + self.skill + " by " + format_number(self.value * amp) + "."


class BonusSlot:
    def __init__(self, value):
        self.value = value
        self.action = lambda worker: worker.add_bonus_slots(self.value)

    def provide_text(self, amp):
        if self.value * amp == 1:
            return "Provides an additional worker slot."
        else:
            return "Provides " + format_number(self.value * amp) + " additional worker slots."

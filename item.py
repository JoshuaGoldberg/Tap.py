import copy

import pygame


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
        new_item = copy.copy(self)
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

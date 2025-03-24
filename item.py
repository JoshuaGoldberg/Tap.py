import pygame


class Item:

    pressed = False

    def __init__(self, image, name, description, classification, use_action, equip_action):
        self.classification = classification
        self.image = image
        self.name = name
        self.description = description
        self.use_action = use_action
        self.equip_action = equip_action
        self.equipped_by = None
        self.seals = []

    def __key(self):
        return self.name, self.description

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.__key() == other.__key()
        return NotImplemented

    def boost_stat(self, value, category):
        self.equipped_by.item_bonuses[category] *= value

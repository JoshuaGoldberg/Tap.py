import pygame


class Item:

    pressed = False

    def __init__(self, image, name, description, use_action, equip_action, game):
        self.image = image
        self.name = name
        self.description = description
        self.use_action = use_action
        self.equip_action = equip_action
        self.game = game

    def __key(self):
        return self.name, self.description

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.__key() == other.__key()
        return NotImplemented

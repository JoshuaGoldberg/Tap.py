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

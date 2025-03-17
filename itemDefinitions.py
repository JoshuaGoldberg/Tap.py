import pygame

from item import Item


def get_items():
    shovel_img = pygame.image.load('assets/shovel.png').convert_alpha()
    shovel = Item(shovel_img, "Dev Shovel", "The long lost developer shovel."
                                            " Boosts gathering value by 10 trillion",
                  "Accessories",
                  None,
                  lambda: shovel.boost_stat(10000000000000, 0))

    return [shovel]

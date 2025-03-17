import pygame

from item import Item


class ItemsManager:

    def __init__(self, game):
        self.game = game
        shovel_img = pygame.image.load('assets/shovel.png').convert_alpha()
        twig_img = pygame.image.load('assets/twig.png').convert_alpha()

        shovel = Item(shovel_img, "Dev Shovel", "The long lost developer shovel."
                                                " Boosts gathering value by 10 trillion",
                      "Accessories",
                      None,
                      lambda: shovel.boost_stat(10000000000000, 0))

        twig = Item(twig_img, "Twig", "A loose twig found in the forest.",
                    "Items",
                    None,
                    None)

        blue_item_img = pygame.image.load('assets/blue_berry.png').convert_alpha()
        blueberry = Item(blue_item_img, "Blue Berry",
                         "A blue berry. "
                         "Note: not a red berry, although it's easy to get confused",
                         "Consumables",
                         lambda: self.game.value_up(1000000000), lambda: None)

        self.item_list = {shovel.name: shovel,
                          twig.name: twig,
                          blueberry.name: blueberry}

        self.gather_lp = [twig, blueberry]

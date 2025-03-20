import pygame

from item import Item


class ItemsManager:

    def __init__(self, game):
        self.game = game
        shovel_img = pygame.image.load('assets/shovel.png').convert_alpha()
        twig_img = pygame.image.load('assets/twig.png').convert_alpha()
        iron_ore_img = pygame.image.load('assets/iron_ore.png').convert_alpha()
        stone_img = pygame.image.load('assets/stone.png').convert_alpha()

        shovel = Item(shovel_img, "Dev Shovel", "The long lost developer shovel."
                                                " Boosts gathering value by 10 trillion",
                      "Accessories",
                      None,
                      lambda: shovel.boost_stat(10000000000000, 0))

        twig = Item(twig_img, "Twig", "A loose twig found in the forest.",
                    "Items",
                    None,
                    None)

        iron_ore = Item(iron_ore_img, "Iron Ore",
                        "A rock with a chunk of iron ore. Could someday be something greater.",
                        "Items",
                        None,
                        None)

        stone = Item(stone_img, "Iron Ore",
                     "Stone, from deep within the mines. "
                     "Unremarkable, but nevertheless a vital building block for your journey.",
                     "Items",
                     None,
                     None)

        blue_item_img = pygame.image.load('assets/blue_berry.png').convert_alpha()
        blueberry = Item(blue_item_img, "Blue Berry",
                         "A blue berry. "
                         "Note: not a red berry, although it's easy to get confused",
                         "Consumables",
                         lambda: self.game.value_up(1000000000), lambda: None)

        red_seal_img = pygame.image.load('assets/red_seal.png').convert_alpha()
        red_seal = Item(red_seal_img, "Red Seal",
                        "A red seal common in these parts. Used to show prestige and boost a persons"
                        " accessories.",
                        "Consumables",
                        lambda: None, lambda: None)

        gold_seal_img = pygame.image.load('assets/gold_seal.png').convert_alpha()
        gold_seal = Item(gold_seal_img, "Gold Seal",
                         "A gold seal. Lesser seen, and by extension signifies "
                         "more value upon items it decorates.",
                         "Consumables",
                         lambda: None, lambda: None)

        self.item_list = {shovel.name: shovel,
                          twig.name: twig,
                          blueberry.name: blueberry,
                          iron_ore.name: iron_ore,
                          stone.name: stone,
                          red_seal.name: red_seal,
                          gold_seal.name: gold_seal}

        self.gather_lp = [twig, blueberry]
        self.mining_lp = [iron_ore, stone]
        self.seal_lp = [red_seal, gold_seal]

import pygame

from item import *


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
                      lambda worker: worker.boost_stat(10000000000000, 0), 9999999)

        twig = Item(twig_img, "Twig", "A loose twig found in the forest.",
                    "Items",
                    None,
                    lambda: None, 25)

        iron_ore = Item(iron_ore_img, "Iron Ore",
                        "A rock with a chunk of iron ore. Could someday be something greater.",
                        "Items",
                        None,
                        None, 150)

        stone = Item(stone_img, "Stone",
                     "Stone, from deep within the mines. "
                     "Unremarkable, but nevertheless a vital building block for your journey.",
                     "Items",
                     None,
                     None, 50)

        blue_item_img = pygame.image.load('assets/blue_berry.png').convert_alpha()
        blueberry = Item(blue_item_img, "Blue Berry",
                         "A blue berry. "
                         "Note: not a red berry, although it's easy to get confused",
                         "Consumables",
                         lambda: self.game.value_up(1000000000), lambda: None, 1)

        red_seal_img = pygame.image.load('assets/red_seal.png').convert_alpha()
        red_seal = Item(red_seal_img, "Red Seal",
                        "A red seal common in these parts. Used to show prestige and boost a persons"
                        " accessories.",
                        "Items",
                        lambda: None, lambda: None, 5000)

        gold_seal_img = pygame.image.load('assets/gold_seal.png').convert_alpha()
        gold_seal = Item(gold_seal_img, "Gold Seal",
                         "A gold seal. Lesser seen, and by extension signifies "
                         "more value upon items it decorates.",
                         "Items",
                         lambda: None, lambda: None, 50000)

        shadow_seal_img = pygame.image.load('assets/shadow_seal.png').convert_alpha()
        shadow_seal = Item(shadow_seal_img, "Shadow Seal",
                           "A dark shadowy seal. Typically symbolic of some sort of dark power or "
                           "other malicious intent.",
                           "Items",
                           lambda: None, lambda: None, 65000000)

        crystal_seal_img = pygame.image.load('assets/crystal_seal.png').convert_alpha()
        crystal_seal = Item(crystal_seal_img, "Crystal Seal",
                            "A odd seal decorated with a crystalline appearance. Shimmers under the light. "
                            "Such craftsmanship is not typical to these lands. Perhaps the winds of trade brought it "
                            "here"
                            "from afar.",
                            "Items",
                            lambda: None, lambda: None, 8000000000)

        mystic_stamp_img = pygame.image.load('assets/c_mystic_stamp.png').convert_alpha()
        mystic_stamp = Item(mystic_stamp_img, "Mystic Stamp",
                            "A stamp imbued with magical energy. A mages answers to the royal stamp"
                            " system. However, you can benefit from using both.",
                            "Items",
                            lambda: None, lambda: None, 150000)

        void_caller_stamp_img = pygame.image.load('assets/voidcaller_stamp.png').convert_alpha()
        voidcaller_stamp = Item(void_caller_stamp_img, "Voidcaller Stamp",
                                "A stamp imbued with magical energy. In particular, this one"
                                " has been altered with dark energy by radical mages of the kingdom. Great power, "
                                "but also great risk...",
                                "Items",
                                lambda: None, lambda: None, 900000000)

        primo_img = pygame.image.load('assets/primo.png').convert_alpha()
        primo_stamp = Item(primo_img, "Primordial Stamp",
                           "A crystalline stamp with an odd shimmer. The material is not from these lands, "
                           "perhaps brought from overseas. Whatever it does will surely be unique!",
                           "Items",
                           lambda: None, lambda: None, 15000000000)

        self.item_list = {shovel.name: shovel,
                          twig.name: twig,
                          blueberry.name: blueberry,
                          iron_ore.name: iron_ore,
                          stone.name: stone,
                          red_seal.name: red_seal,
                          gold_seal.name: gold_seal,
                          shadow_seal.name: shadow_seal,
                          mystic_stamp.name: mystic_stamp,
                          voidcaller_stamp.name: voidcaller_stamp,
                          primo_stamp.name: primo_stamp,
                          crystal_seal.name: crystal_seal}

        self.gather_lp = [twig, blueberry]
        self.mining_lp = [iron_ore, stone]
        self.seal_lp = [[red_seal, 0], [gold_seal, 75], [shadow_seal, 95], [crystal_seal, 50]]
        self.stamp_lp = [[mystic_stamp, 0], [voidcaller_stamp, 50], [primo_stamp, 75]]
        self.shop_common_lp = [[blueberry, 15], [stone, 25]]
        self.shop_uncommon_lp = [[iron_ore, 5]]
        self.shop_rare_lp = [[shovel, 1]]

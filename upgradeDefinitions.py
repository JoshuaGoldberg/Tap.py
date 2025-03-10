import pygame

from upgrade import Upgrade


def double_base_clicks_wrapper(game):
    game.double_base_clicks()


def increase_click_power_wrapper(game):
    game.increase_click_power()


def enable_workers_wrapper(game):
    game.enable_workers()


def double_gather_xp_wrapper(game):
    game.double_gathering_xp()


def inv_Wrapper(game):
    game.unlock_inventory()


def get_upgrades():
    iron_grip_img = pygame.image.load('assets/iron_upgrade.png').convert_alpha()
    magic_stone_img = pygame.image.load('assets/magic_stone.png').convert_alpha()
    strength_img = pygame.image.load('assets/strength.png').convert_alpha()
    herbs_img = pygame.image.load('assets/herbs.png').convert_alpha()
    double_img = pygame.image.load('assets/double_click.png').convert_alpha()
    jobs_img = pygame.image.load('assets/jobs.png').convert_alpha()
    basket_img = pygame.image.load('assets/basket.png').convert_alpha()
    chest_upg_img = pygame.image.load('assets/chest_upg.png').convert_alpha()

    future_upgrades = []
    bought_upgrades = []

    base_click_double_1 = Upgrade(
        150,
        "Iron Grip",
        "Cost: " + str(150) + "\nDoubles value per click.\nIt turns out the secret to success is all in the handwork.",
        double_base_clicks_wrapper,
        iron_grip_img
    )
    base_click_double_2 = Upgrade(
        1000,
        "Magic Stones",
        "Cost: " + str(1000) + "\nDoubles value per click.\nForest pebbles are apparently magically blessed.",
        double_base_clicks_wrapper,
        magic_stone_img
    )
    flat_click_power_1 = Upgrade(
        1000,
        "Strength Training",
        "Cost: " + str(1000) + "\n+1 to click power.\nClicking through the power of lifting.",
        increase_click_power_wrapper,
        strength_img
    )
    flat_click_power_2 = Upgrade(
        2500,
        "Medicinal Herbs",
        "Cost: " + str(2500) + "\n+1 to click power.\n9/10 Mages recommend!",
        increase_click_power_wrapper,
        herbs_img
    )
    flat_click_power_3 = Upgrade(
        10000,
        "Multi-finger mode",
        "Cost: " + str(10000) + "\n+1 to click power.\n+1 finger equates to +1 click power",
        increase_click_power_wrapper,
        double_img
    )

    enable_workers = Upgrade(
        15000,
        "Job Listings",
        "Cost: " + str(15000) +
        "\nAllows hiring of workers\nA small flier in the town square ought to attract attention",
        enable_workers_wrapper,
        jobs_img
    )

    baskets = Upgrade(
        10000,
        "Berry Baskets",
        "Cost: " + str(10000) +
        "\nDouble Gathering XP Rate\n\"Storage innovations mean workers can hold more for longer\"",
        double_gather_xp_wrapper,
        basket_img
    )

    inventory = Upgrade(
        5000,
        "Personal Chest",
        "Cost: " + str(5000) +
        "\nUnlock Inventory\n\"Now you can collect all those priceless items you've been throwing away!\"",
        inv_Wrapper,
        chest_upg_img
    )

    future_upgrades.extend([
        base_click_double_1, base_click_double_2, flat_click_power_1,
        flat_click_power_2, flat_click_power_3, enable_workers, baskets,
        inventory
    ])
    return future_upgrades, bought_upgrades

from game import *
from uiElement import *
from button import Button
from popup import *


class UpgradeUI:
    def __init__(self, x, y, game):
        self.offset = (x, y)
        self.game = game
        upgrade_background_img = pygame.image.load('assets/upgradeBase.png').convert_alpha()
        self.upgradeBase = UIElement(175 + x, 335 + y, upgrade_background_img, 8.0)

    def draw(self, surface, layer):

        offset_x = 0
        offset_y = 50

        self.upgradeBase.draw(surface)

        tempStore = []

        for upgrade in self.game.upgrades:

            upgradeButton = Button(self.offset[0] + offset_x + 10, self.offset[1] + offset_y + 10,
                                   upgrade.image, 2.0, lambda: self.game.process_upgrade(upgrade),
                                   display_popup(upgrade.name, upgrade.blurb), 0)
            tempStore.append(upgradeButton)
            upgradeButton.draw(surface, layer)
            offset_x += 82
            if offset_x >= 400:
                offset_x = 0
                offset_y += 80



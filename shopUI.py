from uiElement import *
from button import Button
from popup import *


class ShopUI:
    def __init__(self, x, y, game):
        self.offset = (x, y)
        self.game = game
        shop_background_img = pygame.image.load('assets/shop.png').convert_alpha()
        self.upgradeBase = UIElement(0 + x, 0 + y, shop_background_img, 8.15)

    def draw(self, surface, layer):
        self.upgradeBase.draw(surface)
        x_img = pygame.image.load('assets/x.png').convert_alpha()
        exitButton = Button(self.offset[0] + 720, self.offset[1] - 425, x_img, 2.0,
                            lambda: self.game.exit_layer(), None, 2)
        exitButton.draw(surface, layer)


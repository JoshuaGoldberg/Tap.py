from game import *
from uiElement import *
from button import Button
from popup import *


class InventoryUI:
    def __init__(self, x, y, game):
        self.offset = (x, y)
        self.game = game
        inventory_base_img = pygame.image.load('assets/inventory.png').convert_alpha()
        self.inventoryBase = UIElement(x, y, inventory_base_img, 8.0)

    def draw(self, surface, layer):
        offset_x = 0
        offset_y = 50

        self.inventoryBase.draw(surface)

        x_img = pygame.image.load('assets/x.png').convert_alpha()
        exitButton = Button(self.offset[0] + 720, self.offset[1] - 415, x_img, 2.0,
                            lambda: self.game.exit_layer(), None, 1)
        exitButton.draw(surface, layer)

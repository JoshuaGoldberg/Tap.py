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

        offset_x = 0
        offset_y = 0
        row_count = 0
        seal_num = 0

        for i in range(0, 9):

            if i in self.game.seal_positions and seal_num < len(self.game.seals_inventory):
                seal_for_sale = Button(self.offset[0] + 620 + offset_x + self.game.seal_offsets[i][0],
                                       self.offset[1] + 150 + offset_y + self.game.seal_offsets[i][1],
                                       self.game.seals_inventory[seal_num].image, 6.0,
                                       lambda: self.game.buy_seal(self.game.seals_inventory[seal_num],
                                                                  5000,
                                                                  i,
                                                                  seal_num), None, 2)

                seal_for_sale.draw(surface, layer)
                seal_num += 1

            offset_x += 55
            row_count += 1
            if row_count >= 3:
                row_count = 0
                offset_x = 0
                offset_y += 120


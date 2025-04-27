from uiElement import *
from button import Button
from popup import *


class ShopUI:
    def __init__(self, x, y, game):
        self.offset = (x, y)
        self.game = game
        shop_background_img = pygame.image.load('assets/shop.png').convert_alpha()
        self.upgradeBase = UIElement(0 + x, 0 + y, shop_background_img, 8.15)
        self.seals = []
        self.seal_positions = []
        self.seal_offsets = []
        self.cached_seals = None
        self.small_font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 24)

    def update_seals(self):
        if self.cached_seals != self.game.seals_inventory:
            self.seals = self.game.seals_inventory[:]
            self.seal_positions = self.game.seal_positions[:]
            self.seal_offsets = self.game.seal_offsets[:]
            self.cached_seals = self.seals[:]

    def draw(self, surface, layer):
        self.upgradeBase.draw(surface)
        x_img = pygame.image.load('assets/x.png').convert_alpha()
        exitButton = Button(self.offset[0] + 720, self.offset[1] - 425, x_img, 2.0,
                            lambda: self.game.exit_layer(), None, 2)
        exitButton.draw(surface, layer)
        self.update_seals()

        back_img = pygame.image.load('assets/inv_back.png').convert_alpha()
        back_button = Button(1430, 928, back_img, 2.5,
                             lambda: self.game.back_shop_page(), None, 2)
        back_button.draw(surface, layer)

        forward_img = pygame.image.load('assets/inv_forward.png').convert_alpha()
        forward_button = Button(1520, 928, forward_img, 2.5,
                                lambda: self.game.forward_shop_page(), None, 2)
        forward_button.draw(surface, layer)

        offset_x = 0
        offset_y = 0
        row_count = 0
        seal_num = 0
        tempStore = []

        # render in seals
        for i in range(0, 9):

            seal = None
            if seal_num < len(self.seals) and self.seals[seal_num] is not None:
                seal = self.seals[seal_num].image

            if i in self.seal_positions and seal_num < len(self.seals):
                seal_for_sale = Button(self.offset[0] + 620 + offset_x + self.seal_offsets[i][0],
                                       self.offset[1] + 150 + offset_y + self.seal_offsets[i][1],
                                       seal,
                                       6.0,
                                       lambda: self.game.buy_seal(self.seals[seal_num],
                                                                  self.seals[seal_num].cost,
                                                                  i,
                                                                  seal_num),
                                       display_popup(self.seals[seal_num].name, self.seals[seal_num].description + "\n\nCost: "
                                                     + self.game.format_number(self.seals[seal_num].cost) + " Value"), 2)

                seal_for_sale.draw(surface, layer)
                seal_num += 1

            offset_x += 55
            row_count += 1
            if row_count >= 3:
                row_count = 0
                offset_x = 0
                offset_y += 120

        offset_x = 0
        offset_y = 50
        num = 1
        base = (self.game.shop_page - 1) * 18
        curr_inventory = copy.copy(self.game.shop_inventory)

        # render in shop items
        for item in curr_inventory:
            if base < num <= base + 18:
                itemButton = Button(291 + offset_x + 10, self.offset[1] + offset_y + 81,
                                    item.image, 6.0, lambda: self.game.buy_item(item),
                                    display_popup(item.name,
                                                  item.description + "\n\nCost: "
                                                  + self.game.format_number(item.cost) + " Value"), 2)

                tempStore.append(itemButton)
                itemButton.draw(surface, layer)

                if item in curr_inventory:
                    if curr_inventory[item] > 1:
                        number_of_item = self.small_font.render(str(curr_inventory[item]), True, (255, 255, 255))
                        surface.blit(number_of_item, (247 + offset_x, self.offset[1] + 105 + offset_y))

                offset_x += 147
                if offset_x >= 1300:
                    offset_x = 0
                    offset_y += 147

            num += 1

        for button in tempStore:
            button.handlePopup(surface, layer)

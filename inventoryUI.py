import text_wrapper
from game import *
from uiElement import *
from button import Button
from popup import *
from text_wrapper import *


class InventoryUI:
    def __init__(self, x, y, game):
        self.offset = (x, y)
        self.game = game
        inventory_base_img = pygame.image.load('assets/inventory.png').convert_alpha()
        self.inventoryBase = UIElement(x, y, inventory_base_img, 8.15)
        self.item_border_img = pygame.image.load('assets/item_border.png').convert_alpha()

    def draw(self, surface, layer):
        offset_x = 0
        offset_y = 0

        self.inventoryBase.draw(surface)
        font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 24)
        sub_font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 20)

        font2 = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 48)
        tab_text = font2.render(self.game.inventory_tab, True, (0, 0, 0))
        surface.blit(tab_text, (self.offset[0] - 785, self.offset[1] - 355))
        x_img = pygame.image.load('assets/x.png').convert_alpha()
        exitButton = Button(self.offset[0] + 720, self.offset[1] - 425, x_img, 2.0,
                            lambda: self.game.exit_layer(), None, 1)

        curr_page = self.game.inventory_page
        curr_inventory = []
        if self.game.inventory_tab == "Accessories":
            curr_inventory = self.game.accessories_inventory
        elif self.game.inventory_tab == "Items":
            curr_inventory = self.game.item_inventory
        elif self.game.inventory_tab == "Consumables":
            curr_inventory = self.game.consumable_inventory

        accessory_img = pygame.image.load('assets/accessory.png').convert_alpha()
        accessory_tab = Button(1625 + offset_x, 137 + offset_y, accessory_img, 3.0,
                               lambda: self.game.set_inventory_tab("Accessories"), None, 1)
        accessory_tab.draw(surface, layer)

        item_img = pygame.image.load('assets/item.png').convert_alpha()
        item_tab = Button(1500 + offset_x, 137 + offset_y, item_img, 3.0,
                          lambda: self.game.set_inventory_tab("Items"), None, 1)
        item_tab.draw(surface, layer)

        consumables_img = pygame.image.load('assets/consumable.png').convert_alpha()
        consumable_tab = Button(1375 + offset_x, 137 + offset_y, consumables_img, 3.0,
                                lambda: self.game.set_inventory_tab("Consumables"), None, 1)
        consumable_tab.draw(surface, layer)

        back_img = pygame.image.load('assets/inv_back.png').convert_alpha()
        back_button = Button(1140 + offset_x, 1020 + offset_y, back_img, 3.0,
                             lambda: self.game.inv_back(), None, 1)
        back_button.draw(surface, layer)

        forward_img = pygame.image.load('assets/inv_forward.png').convert_alpha()
        forward_button = Button(1370 + offset_x, 1020 + offset_y, forward_img, 3.0,
                                lambda: self.game.inv_forward(), None, 1)
        forward_button.draw(surface, layer)

        page_text = font2.render("Page " + str(self.game.inventory_page), True, (0, 0, 0))
        exitButton.draw(surface, layer)
        surface.blit(page_text, (self.offset[0] - 785, self.offset[1] + 420))

        item_in_row = 0
        item_num = (curr_page - 1) * 40
        curr_num = 0
        for item in curr_inventory:
            if item_num <= curr_num < item_num + 40:
                itemButton = Button(302 + offset_x, 340 + offset_y, item.image, 6.0,
                                    lambda: self.game.set_selected_item(item), None, 1)

                if self.game.selected_item == item:
                    border = UIElement(302 + offset_x, 340 + offset_y, self.item_border_img, 9)
                    border.draw(surface)

                itemButton.draw(surface, layer)
                item_in_row += 1
                offset_x += 146.5

                if item_in_row >= 8:
                    offset_x = 0
                    item_in_row = 0
                    offset_y += 146.5
            curr_num += 1

        if self.game.selected_item is not None:
            item_icon = Button(1620, 360, self.game.selected_item.image, 9.0,
                               lambda: None, None, 1)
            item_icon.draw(surface, layer)
            item_name = font.render(self.game.selected_item.name, True, (255, 255, 255))
            surface.blit(item_name, (self.offset[0] + 470, self.offset[1] - 15))
            text = text_wrapper.render_text_list(
                text_wrapper.wrap_text(self.game.selected_item.description, sub_font, 275), sub_font)
            surface.blit(text, (self.offset[0] + 470, self.offset[1] + 50))



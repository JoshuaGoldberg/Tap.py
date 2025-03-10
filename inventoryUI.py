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
        font = pygame.font.SysFont(None, 48)
        tab_text = font.render(self.game.inventory_tab, True, (0, 0, 0))
        surface.blit(tab_text, (self.offset[0] - 785, self.offset[1] - 330))
        x_img = pygame.image.load('assets/x.png').convert_alpha()
        exitButton = Button(self.offset[0] + 720, self.offset[1] - 415, x_img, 2.0,
                            lambda: self.game.exit_layer(), None, 1)

        curr_inventory = []
        if self.game.inventory_tab == "Accessories":
            curr_inventory = self.game.accessories_inventory
        elif self.game.inventory_tab == "Items":
            curr_inventory = self.game.item_inventory
        elif self.game.inventory_tab == "Consumables":
            curr_inventory = self.game.consumable_inventory

        item_in_row = 0
        for item in curr_inventory:
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

        if self.game.selected_item is not None:
            item_icon = Button(1620, 360, self.game.selected_item.image, 9.0,
                               lambda: None, None, 1)
            item_icon.draw(surface, layer)
            item_name = font.render(self.game.selected_item.name, True, (255, 255, 255))
            surface.blit(item_name, (self.offset[0] + 470, self.offset[1]))
            text = text_wrapper.render_text_list(
                text_wrapper.wrap_text(self.game.selected_item.description, font, 280), font)
            surface.blit(text, (self.offset[0] + 470, self.offset[1] + 50))

        exitButton.draw(surface, layer)

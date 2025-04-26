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
        seal_menu_img = pygame.image.load('assets/seal_menu.png').convert_alpha()
        self.seal_add_menu = UIElement(x + 605, y + 150, seal_menu_img, 13.15)
        self.item_border_img = pygame.image.load('assets/item_border.png').convert_alpha()
        self.locked_img = pygame.image.load('assets/locked_seal.png').convert_alpha()
        self.locked_stamp_img = pygame.image.load('assets/locked_stamp.png').convert_alpha()

    def draw(self, surface, layer):
        offset_x = 0
        offset_y = 0

        self.inventoryBase.draw(surface)
        font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 24)
        sub_font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 20)
        small_font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 24)

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

                if curr_inventory == self.game.consumable_inventory or curr_inventory == self.game.item_inventory:
                    if curr_inventory[item] > 1:
                        number_of_item = small_font.render(str(curr_inventory[item]), True, (255, 255, 255))
                        surface.blit(number_of_item, (250 + offset_x, 365 + offset_y))

                if item.equipped_by is not None:
                    worker = item.equipped_by
                    equipped_icon = Button(352 + offset_x, 290 + offset_y, item.equipped_by.image, 1.5,
                                           lambda: self.game.close_and_select(item.equipped_by),
                                           display_popup("Equipped by:", worker.firstname + " " + worker.lastname), 1)
                    equipped_icon.draw(surface, layer)

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

            if self.game.selected_item in self.game.accessories_inventory:
                add_seal_img = pygame.image.load('assets/add_seal.png').convert_alpha()
                add_seal = Button(1610 + 146.5, 280, add_seal_img, 3.0,
                                  lambda: self.game.toggle_seal_add(), None, 1)
                add_seal.draw(surface, layer)

            offset_x = 0
            for seal in self.game.selected_item.seals:
                seal_button = Button(1502 + offset_x, 475, seal.image, 6.0,
                                     lambda: None, None, 1)
                seal_button.draw(surface, layer)
                offset_x += 60

            stamp_x = 1502
            stamp_y = 285
            counter = 0
            for stamp in self.game.selected_item.stamps:

                if counter == 1:
                    stamp_x = 1567
                    stamp_y = 300
                elif counter == 2:
                    stamp_x = 1522
                    stamp_y = 355

                stamp_button = Button(stamp_x, stamp_y, pygame.transform.rotate(stamp.image, 0), 6.0,
                                      lambda: None, None, 1)
                stamp_button.draw(surface, layer)
                counter += 1

            if self.game.selected_item.equipped_by is None:

                if self.game.selected_item in self.game.consumable_inventory:
                    use_img = pygame.image.load('assets/use.png').convert_alpha()

                    use_button = Button(1380 + 146.5, 975, use_img, 3.0,
                                        lambda: self.game.use_item(), None, 1)
                    use_button.draw(surface, layer)

                if self.game.selected_item in self.game.accessories_inventory:
                    equip_img = pygame.image.load('assets/equip.png').convert_alpha()

                    equip_button = Button(1380 + 146.5, 975, equip_img, 3.0,
                                          lambda: self.game.equip_select(self.game.selected_item), None, 1)
                    equip_button.draw(surface, layer)

                trash_img = pygame.image.load('assets/trash.png').convert_alpha()
                trash_button = Button(1570 + 146.5, 975, trash_img, 3.0,
                                      lambda: self.game.trash_item(), None, 1)
                trash_button.draw(surface, layer)

            if self.game.add_seal_menu is True:

                self.seal_add_menu.draw(surface)

                offset_x = 0
                for seal_list in self.game.game_items.seal_lp:
                    seal = seal_list[0]
                    if seal in self.game.item_inventory:
                        seal_add = Button(1475 + offset_x, 600, seal.image, 6.0,
                                          lambda: self.game.add_specific_seal(
                                              seal),
                                          None, 1)
                        seal_add.draw(surface, layer)
                    else:
                        seal_locked = Button(1475 + offset_x, 600, self.locked_img, 6.0,
                                             lambda: None,
                                             None, 1)
                        seal_locked.draw(surface, layer)
                    offset_x += 60

                offset_x = 0
                for stamp_list in self.game.game_items.stamp_lp:
                    stamp = stamp_list[0]
                    if stamp in self.game.item_inventory:
                        stamp_add = Button(1475 + offset_x, 850, stamp.image, 6.0,
                                           lambda: self.game.add_specific_stamp(
                                               stamp),
                                           None, 1)
                        stamp_add.draw(surface, layer)
                    else:
                        stamp_locked = Button(1475 + offset_x, 850, self.locked_stamp_img, 6.0,
                                              lambda: None,
                                              None, 1)
                        stamp_locked.draw(surface, layer)
                    offset_x += 70

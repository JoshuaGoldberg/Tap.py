from uiElement import *
from button import Button
from popup import *


class InfoUI:
    def __init__(self, x, y, game):
        self.offset = (x, y)
        self.game = game
        upgrade_background_img = pygame.image.load('assets/info_base.png').convert_alpha()
        self.upgradeBase = UIElement(0 + x, 0 + y, upgrade_background_img, 8.0)

    def draw(self, surface, layer):
        self.upgradeBase.draw(surface)
        font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 32)
        if self.game.selectedWorker is not None:
            worker_image = Button(self.offset[0] + 148, self.offset[1] - 430, self.game.selectedWorker.image, 2.0,
                                  lambda: None, None, 0)
            worker_image.draw(surface, layer)
            name_text = font.render(
                "Name: " + self.game.selectedWorker.firstname + " " + self.game.selectedWorker.lastname, True,
                (0, 0, 0))
            surface.blit(name_text, (self.offset[0] - 230, self.offset[1] - 330))
            line_text = font.render("Activity: " + self.game.selectedWorker.current_activity, True, (0, 0, 0))
            surface.blit(line_text, (self.offset[0] - 230, self.offset[1] - 280))
            gather_img = pygame.image.load('assets/gathering.png').convert_alpha()
            gatheringButton = Button(self.offset[0] - 200, self.offset[1] - 200, gather_img, 2.0,
                                     lambda: self.game.set_worker_status("Gathering"), None, 0)
            mining_img = pygame.image.load('assets/mining.png').convert_alpha()
            miningButton = Button(self.offset[0] - 125, self.offset[1] - 200, mining_img, 2.0,
                                  lambda: self.game.set_worker_status("Mining"), None, 0)
            gatheringButton.draw(surface, layer)
            miningButton.draw(surface, layer)
            retire_img = pygame.image.load('assets/retire.png').convert_alpha()
            retireButton = Button(self.offset[0] + 160, self.offset[1] + 400, retire_img, 2.0,
                                  lambda: self.game.sell_worker(self.game.selectedWorker), None, 0)
            retireButton.draw(surface, layer)

            if self.game.selectedWorker is not None:
                worker_xp, work_level = self.game.selectedWorker.get_xp_and_level()
                rounded_xp = str(int(worker_xp[0]))
                level_str = str(work_level)
                xp_text = font.render("XP: " + rounded_xp + "/" + str(worker_xp[1]), True, (0, 0, 0))
                level_text = font.render("Level: " + level_str + "/50", True, (0, 0, 0))
                surface.blit(xp_text, (self.offset[0] - 230, self.offset[1] - 150))
                surface.blit(level_text, (self.offset[0] - 230, self.offset[1] - 110))

                slot_img = pygame.image.load('assets/worker_item_slot.png').convert_alpha()
                slot_offset_x = 0
                slot_num = 0
                temp = []

                # item slot rendering
                for x in range(self.game.selectedWorker.slot_count):
                    worker_slot = Button(self.offset[0] - 180 + slot_offset_x, self.offset[1] + 290, slot_img, 6.0,
                                         lambda: self.game.selectedWorker.handle_equip(slot_num), None, 0)
                    worker_slot.draw(surface, layer)
                    select_item = self.game.selectedWorker.items[slot_num]
                    if isinstance(select_item, Item):
                        slotted_item = Button(self.offset[0] - 180 + slot_offset_x, self.offset[1] + 290,
                                              select_item.image, 5.0,
                                              lambda: None, display_popup(select_item.name, select_item.item_description_text() +
                                                                          "\n" + "Click to unequip."), 0)
                        temp.append(slotted_item)
                        slotted_item.draw(surface, layer)
                    slot_offset_x += 120
                    slot_num += 1

                for button in temp:
                    button.handlePopup(surface, layer)

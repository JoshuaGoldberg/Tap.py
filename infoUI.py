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
        font = pygame.font.SysFont(None, 48)
        if self.game.selectedWorker is not None:
            worker_image = Button(self.offset[0] + 148, self.offset[1] - 430, self.game.selectedWorker.image, 2.0,
                                  lambda: None, None, layer)
            worker_image.draw(surface, layer)
            name_text = font.render(
                "Name: " + self.game.selectedWorker.firstname + " " + self.game.selectedWorker.lastname, True,
                (0, 0, 0))
            surface.blit(name_text, (self.offset[0] - 230, self.offset[1] - 330))
            line_text = font.render("Activity: " + self.game.selectedWorker.current_activity, True, (0, 0, 0))
            surface.blit(line_text, (self.offset[0] - 230, self.offset[1] - 280))
            gather_img = pygame.image.load('assets/gathering.png').convert_alpha()
            gatheringButton = Button(self.offset[0] - 200, self.offset[1] - 200, gather_img, 2.0,
                                     lambda: self.game.set_worker_status("Gathering"), None, layer)
            mining_img = pygame.image.load('assets/mining.png').convert_alpha()
            miningButton = Button(self.offset[0] - 125, self.offset[1] - 200, mining_img, 2.0,
                                  lambda: self.game.set_worker_status("Mining"), None, layer)
            gatheringButton.draw(surface, layer)
            miningButton.draw(surface, layer)
            retire_img = pygame.image.load('assets/retire.png').convert_alpha()
            retireButton = Button(self.offset[0] + 160, self.offset[1] + 400, retire_img, 2.0,
                                  lambda: self.game.sell_worker(self.game.selectedWorker), None, layer)
            retireButton.draw(surface, layer)
            if self.game.selectedWorker is not None:
                worker_xp, work_level = self.game.selectedWorker.get_xp_and_level()
                rounded_xp = str(int(worker_xp[0]))
                level_str = str(work_level)
                xp_text = font.render("XP: " + rounded_xp + "/" + str(worker_xp[1]), True, (0, 0, 0))
                level_text = font.render("Level: " + level_str + "/50", True, (0, 0, 0))
                surface.blit(xp_text, (self.offset[0] - 230, self.offset[1] - 150))
                surface.blit(level_text, (self.offset[0] - 230, self.offset[1] - 110))

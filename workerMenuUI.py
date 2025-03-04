from game import *
from uiElement import *
from button import Button
from popup import *


class WorkerMenuUI:
    def __init__(self, x, y, game):
        self.offset = (x, y)
        self.game = game
        worker_background_img = pygame.image.load('assets/worker_base.png').convert_alpha()
        self.workerBase = UIElement(0 + x, 0 + y, worker_background_img, 8.0)

    def draw(self, surface, layer):

        offset_x = 0
        offset_y = 0

        self.workerBase.draw(surface)

        for worker in self.game.workers:

            if worker.page() == self.game.worker_page:
                workerButton = Button(875 + offset_x, 300 + offset_y, worker.image, 2.0, lambda: None, None, 0)
                workerButton.draw(surface, layer)

            offset_x += 75

            if offset_x == 375:
                offset_x = 0
                offset_y += 75

            if offset_y == 675:
                offset_x = 0
                offset_y = 0

        back_img = pygame.image.load('assets/backpage.png').convert_alpha()
        front_img = pygame.image.load('assets/frontpage.png').convert_alpha()

        backPageButton = Button(self.offset[0] - 150, self.offset[1] + 400, back_img, 2.0, lambda: self.game.back_page(), None, 0)
        backPageButton.draw(surface, layer)

        frontPageButton = Button(self.offset[0] + 150, self.offset[1]+ 400, front_img, 2.0, lambda: self.game.forward_page(), None, 0)
        frontPageButton.draw(surface, layer)

import pygame
from workerMenuUI import *
from button import *
from upgradeUI import *


class UI:
    def __init__(self, width, height, screen, game):
        self.width = width
        self.height = height
        self.screen = screen
        self.game = game
        self.layer = 0

        self.font = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)
        self.font_popup = pygame.font.SysFont(None, 25)
        self.MIDDLE_SECTION_VALUES = (200, 75)

        self.button_width = 150
        self.button_height = 60

        click_button_img = pygame.image.load('assets/click_me.png').convert_alpha()
        worker_button_img = pygame.image.load('assets/buy_worker.png').convert_alpha()

        self.click_button = Button(100, 120, click_button_img, 5.0,
                                   lambda: self.game.update_clicks(self.game.base_click * self.game.click_power), None,
                                   0)

        self.worker_button = Button(100, 220, worker_button_img, 2.5,
                                    lambda: self.game.add_worker(), None, 0)

        self.worker_menu_next_page = pygame.Rect(1800, 1000, 50, 50)
        self.worker_menu_prev_page = pygame.Rect(1550, 1000, 50, 50)

        self.BUTTON_COLOR = (70, 130, 180)
        self.BUTTON_HOVER_COLOR = (100, 149, 237)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        self.displayed_popup = None

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.layer == 0:

                if self.game.workers_enabled:

                    for worker in self.game.workers:
                        if worker.page() == self.game.worker_page:
                            if worker.button is not None and worker.button.collidepoint(mouse_pos):
                                self.game.selectedWorker = worker

    def draw(self):

        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((30, 30, 30))
        backdrop_img = pygame.image.load('assets/backdrop.png').convert_alpha()
        backdrop = UIElement(960, 540, backdrop_img, 17.0)
        backdrop.draw(self.screen)

        self.click_button.draw(self.screen, self.layer)

        rounded_value = str(int(self.game.value))
        value_text = self.font.render(f"Value: {rounded_value}", True, (255, 255, 255))
        self.screen.blit(value_text, (25, 25))

        if self.game.total_value >= 50:
            upgradeScreen = UpgradeUI(300, 250, self.game)
            upgradeScreen.draw(self.screen, self.layer)

        if self.game.workers_enabled:

            self.worker_button.draw(self.screen, self.layer)
            workerScreen = WorkerMenuUI(850 + 175, 250 + 335, self.game)
            workerScreen.draw(self.screen, self.layer)



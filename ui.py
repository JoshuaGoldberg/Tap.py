import pygame
from workerMenuUI import *
from button import *
from upgradeUI import *
from infoUI import *
from inventoryUI import *
from shopUI import *


class UI:
    def __init__(self, width, height, screen, game):
        self.width = width
        self.height = height
        self.screen = screen
        self.game = game

        self.font = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 32)
        self.font_small = pygame.font.SysFont(None, 32)
        self.font_popup = pygame.font.SysFont(None, 25)
        self.cursor_img = pygame.image.load('assets/cursor.png').convert_alpha()
        self.cursor_img2 = pygame.image.load('assets/cursor_2.png').convert_alpha()
        alert_img = pygame.image.load('assets/alert.png').convert_alpha()
        self.alert = UIElement(107.5, 985, alert_img, 4)
        self.inventoryScreen = InventoryUI(1019, 560, self.game)
        self.shopScreen = ShopUI(1019, 560, self.game)

        self.button_width = 150
        self.button_height = 60

        click_button_img = pygame.image.load('assets/click_me.png').convert_alpha()
        worker_button_img = pygame.image.load('assets/buy_worker.png').convert_alpha()
        inventory_button_img = pygame.image.load('assets/inventory_button.png').convert_alpha()
        shop_button_img = pygame.image.load('assets/shop_button.png').convert_alpha()

        self.click_button = Button(100, 120, click_button_img, 5.0,
                                   lambda: self.game.update_clicks(self.game.base_click * self.game.click_power), None,
                                   -1)

        self.worker_button = Button(100, 220, worker_button_img, 2.5,
                                    lambda: self.game.add_worker(), None, 0)

        self.inventory_button = Button(70, 1019, inventory_button_img, 2.5,
                                       lambda: self.game.access_inventory(), None, -1)

        self.shop_button = Button(100, 320, shop_button_img, 5.0,
                                  lambda: self.game.access_shop(), None, -1)

        self.worker_menu_next_page = pygame.Rect(1800, 1000, 50, 50)
        self.worker_menu_prev_page = pygame.Rect(1550, 1000, 50, 50)

        self.BUTTON_COLOR = (70, 130, 180)
        self.BUTTON_HOVER_COLOR = (100, 149, 237)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        self.displayed_popup = None

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.exit_layer()

    def draw(self):
        Button.all_buttons.clear()

        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((30, 30, 30))
        backdrop_img = pygame.image.load('assets/backdrop.png').convert_alpha()
        backdrop = UIElement(960, 540, backdrop_img, 17.0)
        backdrop.draw(self.screen)

        self.click_button.draw(self.screen, self.game.layer)

        if self.game.inventory_unlocked:
            self.inventory_button.draw(self.screen, self.game.layer)
            # TEMP
            self.shop_button.draw(self.screen, self.game.layer)
            if self.game.new_item:
                self.alert.draw(self.screen)

        rounded_value = self.game.format_number(int(self.game.value))
        value_text = self.font.render(f"Value: {rounded_value}", True, (255, 255, 255))
        self.screen.blit(value_text, (25, 5))

        if self.game.total_value >= 50:
            upgradeScreen = UpgradeUI(300, 250, self.game)
            upgradeScreen.draw(self.screen, self.game.layer)

        if self.game.workers_enabled:
            self.worker_button.draw(self.screen, self.game.layer)
            workerScreen = WorkerMenuUI(850 + 175, 250 + 335, self.game)
            workerScreen.draw(self.screen, self.game.layer)
            infoScreen = InfoUI(1575, 250 + 335, self.game)
            infoScreen.draw(self.screen, self.game.layer)

        # layer handler

        # INVENTORY MENU
        if self.game.layer == 1:
            self.inventoryScreen.draw(self.screen, self.game.layer)

        if self.game.layer == 2:
            self.shopScreen.draw(self.screen, self.game.layer)

        cursor = UIElement(mouse_pos[0] + 32, mouse_pos[1] + 32, self.cursor_img, 2.0)
        cursor.draw(self.screen)

        for button in Button.all_buttons:
            button.handlePopup(self.screen, self.game.layer)

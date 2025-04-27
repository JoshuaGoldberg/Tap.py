import popup
from game import *
from sound_loader import *


class Button:
    pressed = False
    all_buttons = []

    def __init__(self, x, y, image, scale, action, popup, layer):
        width = image.get_width()
        height = image.get_height()
        # Scale the images
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.altImage = pygame.transform.scale(image, (int(width * scale * 1.1), int(height * scale * 1.1)))
        self.rect = self.image.get_rect(center=(x, y))
        self.alt_rect = self.altImage.get_rect(center=(x, y))
        self.action = action
        self.clicked = False
        self.popup = popup
        self.layer = layer

    def draw(self, surface, currLayer):
        self.all_buttons.append(self)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            surface.blit(self.altImage, self.alt_rect)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and (
                    currLayer == self.layer or self.layer == -1) and Button.pressed is False:
                self.clicked = True
                Button.pressed = True
                click_sound.play()
                self.action()
        else:
            surface.blit(self.image, self.rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            Button.pressed = False

    def handlePopup(self, surface, layer):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.layer == layer:
            if self.popup is not None:
                x_pos = 60
                y_pos = 0
                if pos[0] > 1605:
                    x_pos = -315
                if pos[1] + self.popup.get_height() > 1070:
                    y_pos = pos[1] + self.popup.get_height() - 1070
                surface.blit(self.popup, (pos[0] + x_pos, pos[1] - y_pos))

from game import *


class Button:
    pressed = False

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
        self.click_sound = pygame.mixer.Sound('sounds/soft_click.wav')

    def draw(self, surface, currLayer):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            surface.blit(self.altImage, self.alt_rect)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and (
                    currLayer == self.layer or self.layer == -1) and Button.pressed is False:
                self.clicked = True
                Button.pressed = True
                self.click_sound.play()
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
                surface.blit(self.popup, (pos[0] + 60, pos[1]))

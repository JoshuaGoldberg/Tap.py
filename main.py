import pygame
from game import Game
from ui import UI


def main():
    FPS = 144
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clicker")

    game = Game(WIDTH, HEIGHT, FPS)
    ui = UI(WIDTH, HEIGHT, SCREEN, game)

    clock = pygame.time.Clock()
    running = True
    pygame.mouse.set_visible(False)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)

        game.update()
        ui.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()

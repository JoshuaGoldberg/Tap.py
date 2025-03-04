import pygame
from game import Game
from ui import UI


def main():
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clicker")

    game = Game(WIDTH, HEIGHT)
    ui = UI(WIDTH, HEIGHT, SCREEN, game)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
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

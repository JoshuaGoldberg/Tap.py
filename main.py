import pygame
from game import Game
from ui import UI


def main():
    FPS = 144
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Yet Another Clicker Game")

    game = Game(WIDTH, HEIGHT, FPS)
    ui = UI(WIDTH, HEIGHT, SCREEN, game)

    clock = pygame.time.Clock()
    running = True
    pygame.mouse.set_visible(False)
    last_update_time_ui = pygame.time.get_ticks()
    last_update_time_logic = pygame.time.get_ticks()

    update_interval_ui = 7
    update_interval_logic = 100
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)

        current_time = pygame.time.get_ticks()
        if current_time - last_update_time_logic >= update_interval_logic:
            game.update()
            last_update_time_logic = current_time

        if current_time - last_update_time_ui >= update_interval_ui:
            last_update_time_ui = current_time
            ui.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()

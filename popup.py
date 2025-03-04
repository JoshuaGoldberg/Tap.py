import pygame


def display_popup(text, blurb):
    font_popup = pygame.font.SysFont(None, 25)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    popup_height = 50 + (20 * len(blurb))
    popup_window = pygame.Surface((300, popup_height))
    popup_window.fill((200, 200, 200))
    name_text = font_popup.render(text, True, BUTTON_TEXT_COLOR)
    popup_window.blit(name_text, (5, 5))

    offset = 0

    for line in blurb:
        offset += 20
        line_text = font_popup.render(line, True, BUTTON_TEXT_COLOR)
        popup_window.blit(line_text, (5, 15 + offset))

    return popup_window

import pygame

import text_wrapper


def display_popup(text, blurb):
    font_popup = pygame.font.SysFont(None, 25)
    BUTTON_TEXT_COLOR = (0, 0, 0)
    blurb_text = text_wrapper.wrap_text(blurb, font_popup, 280)

    popup_height = 50 + (20 * len(blurb_text))
    text2 = text_wrapper.render_text_list(blurb_text, font_popup, (0, 0, 0))

    popup_window = pygame.Surface((300, popup_height))
    popup_window.fill((177, 143, 107))
    name_text = font_popup.render(text, True, BUTTON_TEXT_COLOR)
    popup_window.blit(name_text, (5, 5))

    popup_window.blit(text2, (5, 35))

    return popup_window

import pygame

import text_wrapper


def draw_texture(dest_surf, tex, tile=True):
    if tile:
        tex_w, tex_h = tex.get_size()
        for y in range(0, dest_surf.get_height(), tex_h):
            for x in range(0, dest_surf.get_width(), tex_w):
                dest_surf.blit(tex, (x, y))
    else:
        stretched = pygame.transform.smoothscale(tex, dest_surf.get_size())
        dest_surf.blit(stretched, (0, 0))


def display_popup(text, blurb):
    texture = pygame.image.load("assets/popup_texture.png").convert_alpha()
    font_popup = pygame.font.Font("grand9k_pixel/Grand9K Pixel.ttf", 16)
    BUTTON_TEXT_COLOR = (0, 0, 0)
    blurb_text = text_wrapper.wrap_text(blurb, font_popup, 280)

    popup_height = 50 + (25 * len(blurb_text))
    text2 = text_wrapper.render_text_list(blurb_text, font_popup, (0, 0, 0))

    popup_border = pygame.Surface((310, popup_height + 10))
    popup_border.fill((0, 0, 0))

    popup_window = pygame.Surface((300, popup_height))
    draw_texture(popup_window, texture, tile=True)
    name_text = font_popup.render(text, True, BUTTON_TEXT_COLOR)
    popup_window.blit(name_text, (5, 5))

    popup_window.blit(text2, (5, 35))
    popup_border.blit(popup_window, (5, 5))

    return popup_border

import pygame
from FrontEnd.ui.Styles import MENU_BG_COLOR, MENU_TITLE_COLOR, MENU_TEXT_COLOR, MENU_QUIT_COLOR

class Menu:
    def __init__(self, virtual_width, virtual_height):
        self.virtual_width = virtual_width
        self.virtual_height = virtual_height
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
            if event.key == pygame.K_ESCAPE:
                return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = False
        return True

    def draw(self, surface):
        surface.fill(MENU_BG_COLOR)

        font_title = pygame.font.SysFont(None, 100)
        font_sub = pygame.font.SysFont(None, 50)

        title = font_title.render("PUZZLE BOBBLE", True, MENU_TITLE_COLOR)
        tx = self.virtual_width // 2 - title.get_width() // 2
        surface.blit(title, (tx, 150))

        sub = font_sub.render("Clique ou appuie sur ENTREE pour jouer", True, MENU_TEXT_COLOR)
        sx = self.virtual_width // 2 - sub.get_width() // 2
        surface.blit(sub, (sx, 320))

        quit_text = font_sub.render("ECHAP pour quitter", True, MENU_QUIT_COLOR)
        qx = self.virtual_width // 2 - quit_text.get_width() // 2
        surface.blit(quit_text, (qx, 400))
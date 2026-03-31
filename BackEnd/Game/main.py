
from puzzle_bobble.BackEnd.Game.Game import Game
from puzzle_bobble.BackEnd.Grid import Grid
from puzzle_bobble.FrontEnd.ui.Styles import BUBBLE_COLORS
import pygame
BASE_WIDTH = 800
BASE_HEIGHT = 600

def main():
    pygame.init()

    # resolución del usuario
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puzzle Bubble L2")

    clock = pygame.time.Clock()

    # superficie interna (IMPORTANTE)
    game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

    game = Game()

    running = True
    while running:
        # limpiar superficie interna
        game_surface.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # dibujar juego en superficie base
        game.draw(game_surface)

        # =========================
        # ESCALADO RESPONSIVE
        # =========================
        scale = min(screen_width / BASE_WIDTH, screen_height / BASE_HEIGHT)

        new_width = int(BASE_WIDTH * scale)
        new_height = int(BASE_HEIGHT * scale)

        scaled_surface = pygame.transform.scale(game_surface, (new_width, new_height))

        # centrar en pantalla
        x_offset = (screen_width - new_width) // 2
        y_offset = (screen_height - new_height) // 2

        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, (x_offset, y_offset))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
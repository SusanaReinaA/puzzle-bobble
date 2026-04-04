import pygame
from Game import Game
from Menu import Menu

if __name__ == "__main__":
    pygame.init()

    game = Game()
    menu = Menu(game.virtual_width, game.virtual_height)

    # boucle menu
    while menu.active and game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            result = menu.handle_event(event)
            if not result:
                game.running = False

        menu.draw(game.surface)
        scaled = pygame.transform.scale(
            game.surface,
            (game.screen.get_width(), game.screen.get_height())
        )
        game.screen.blit(scaled, (0, 0))
        pygame.display.flip()

    # lancer le jeu
    if game.running:
        game.run()
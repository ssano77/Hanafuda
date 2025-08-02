# main.py
# This will be the main entry point for the game.

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_controller import GameController
from ui_manager import UIManager

def main():
    """Main function to run the game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hanafuda Koikoi")
    clock = pygame.time.Clock()

    game_controller = GameController()
    ui_manager = UIManager(screen, game_controller)

    game_controller.start_game()

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            ui_manager.handle_event(event)

        # Game logic update
        game_controller.update()

        # Drawing
        ui_manager.draw()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

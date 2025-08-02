# ui_manager.py
# Handles all rendering and user input.

import pygame
from constants import *

class UIManager:
    def __init__(self, screen, game_controller):
        self.screen = screen
        self.game_controller = game_controller
        self.font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 24)
        self.hovered_card = None

    def draw(self):
        """Draws the entire game state to the screen."""
        self.screen.fill(GREEN)
        self.draw_field()
        self.draw_player_hand()
        self.draw_cpu_hand()
        self.draw_captured_piles()
        self.draw_deck()
        self.draw_ui_elements()

    def draw_layout_areas(self):
        """Draws rectangles for the different game areas for clarity."""
        # Optional: for debugging layout
        pygame.draw.rect(self.screen, (0, 80, 0), (50, 50, 700, 200), 2) # CPU Area
        pygame.draw.rect(self.screen, (0, 80, 0), (50, 300, 700, 250), 2) # Field Area
        pygame.draw.rect(self.screen, (0, 80, 0), (50, SCREEN_HEIGHT - 220, 700, 200), 2) # Player Area
        pygame.draw.rect(self.screen, (0, 80, 0), (SCREEN_WIDTH - 220, 50, 200, SCREEN_HEIGHT - 100), 2) # Info Area

    def draw_field(self):
        """Draws the cards on the field."""
        for i, card in enumerate(self.game_controller.field.cards):
            card.rect.topleft = (100 + (i % 8) * (CARD_WIDTH * 0.7), 250 + (i // 8) * (CARD_HEIGHT + 5))
            card.draw(self.screen)

    def draw_player_hand(self):
        """Draws the human player's hand."""
        hand_width = len(self.game_controller.player.hand) * (CARD_WIDTH + 10)
        start_x = (SCREEN_WIDTH - hand_width) / 2
        for i, card in enumerate(self.game_controller.player.hand):
            card.rect.topleft = (start_x + i * (CARD_WIDTH + 10), SCREEN_HEIGHT - CARD_HEIGHT - 20)
            card.draw(self.screen)
            if card == self.hovered_card:
                pygame.draw.rect(self.screen, (255, 255, 0), card.rect, 3) # Highlight hovered card

    def draw_cpu_hand(self):
        """Draws the CPU's hand (face down)."""
        hand_width = len(self.game_controller.cpu.hand) * (CARD_WIDTH + 10)
        start_x = (SCREEN_WIDTH - hand_width) / 2
        for i, card in enumerate(self.game_controller.cpu.hand):
             pygame.draw.rect(self.screen, CARD_BACK_COLOR, (start_x + i * (CARD_WIDTH + 10), 20, CARD_WIDTH, CARD_HEIGHT))
             pygame.draw.rect(self.screen, BLACK, (start_x + i * (CARD_WIDTH + 10), 20, CARD_WIDTH, CARD_HEIGHT), 2)

    def _draw_card_pile(self, surface, cards, position, title):
        """Helper to draw a pile of captured cards."""
        # Use small font for these titles to save space
        title_text = self.small_font.render(title, True, WHITE)
        surface.blit(title_text, (position[0], position[1]))

        if not cards:
            # Draw an empty box placeholder to maintain layout
            placeholder_rect = pygame.Rect(position[0], position[1] + 25, (CARD_WIDTH // 2 + 5) * 4 - 5, CARD_HEIGHT // 2)
            pygame.draw.rect(surface, (0, 60, 0), placeholder_rect, 1)
            return

        for i, card in enumerate(cards):
            # Display captured cards smaller and overlapping
            card_small_img = pygame.transform.scale(card.image, (CARD_WIDTH // 2, CARD_HEIGHT // 2))
            surface.blit(card_small_img, (position[0] + (i % 4) * (CARD_WIDTH // 2 + 5), position[1] + 25 + (i // 4) * (CARD_HEIGHT//4)))

    def draw_captured_piles(self):
        """Draws the cards captured by each player, sorted by category."""
        players_info = [
            {"player": self.game_controller.player, "base_pos": (50, 520), "name": "Player"},
            {"player": self.game_controller.cpu, "base_pos": (50, 50), "name": "CPU"}
        ]
        categories = ['hikari', 'tane', 'tan', 'kasu']

        for info in players_info:
            player = info["player"]
            base_pos = info["base_pos"]
            name = info["name"]

            categorized_cards = {cat: [] for cat in categories}
            for card in player.captured_cards:
                if card.category in categorized_cards:
                    categorized_cards[card.category].append(card)

            # Calculate horizontal spacing for the piles
            # A pile can be up to 4 small cards wide.
            pile_width = 4 * (CARD_WIDTH // 2 + 5) - 5
            horizontal_spacing = pile_width + 25 # Add some padding

            for i, category in enumerate(categories):
                pos = (base_pos[0] + i * horizontal_spacing, base_pos[1])
                title = f"{name} {category.capitalize()}"
                self._draw_card_pile(self.screen, categorized_cards[category], pos, title)

    def draw_deck(self):
        """Draws the deck."""
        if not self.game_controller.deck.is_empty():
            deck_pos = (SCREEN_WIDTH - CARD_WIDTH - 50, 350)
            pygame.draw.rect(self.screen, CARD_BACK_COLOR, (*deck_pos, CARD_WIDTH, CARD_HEIGHT))
            pygame.draw.rect(self.screen, BLACK, (*deck_pos, CARD_WIDTH, CARD_HEIGHT), 2)
            deck_text = self.small_font.render(f"Deck: {len(self.game_controller.deck.cards)}", True, WHITE)
            self.screen.blit(deck_text, (deck_pos[0], deck_pos[1] + CARD_HEIGHT + 5))

    def draw_ui_elements(self):
        """Draws scores and game state information."""
        turn_text_str = f"Turn: {self.game_controller.current_player.name}"
        turn_text = self.font.render(turn_text_str, True, WHITE)
        self.screen.blit(turn_text, (SCREEN_WIDTH - 250, 50))

        # Display player yaku
        player_yaku_str = f"Player Yaku: {self.game_controller.player.yaku_list}"
        player_yaku_text = self.small_font.render(player_yaku_str, True, WHITE)
        self.screen.blit(player_yaku_text, (SCREEN_WIDTH - 250, 100))

        # Display CPU yaku
        cpu_yaku_str = f"CPU Yaku: {self.game_controller.cpu.yaku_list}"
        cpu_yaku_text = self.small_font.render(cpu_yaku_str, True, WHITE)
        self.screen.blit(cpu_yaku_text, (SCREEN_WIDTH - 250, 130))

    def handle_event(self, event):
        """Handles user input events."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered_card = None
            if self.game_controller.game_state == GAME_STATE_PLAYER_TURN:
                for card in self.game_controller.player.hand:
                    if card.rect.collidepoint(event.pos):
                        self.hovered_card = card
                        break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered_card:
                self.game_controller.player_plays_card(self.hovered_card)
                self.hovered_card = None # Reset hover after click

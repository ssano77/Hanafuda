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
        if not self.game_controller.field.cards:
            # Draw placeholder for empty field
            field_rect = pygame.Rect(100, 250, 600, 200)
            pygame.draw.rect(self.screen, (0, 80, 0), field_rect, 2)
            empty_text = self.small_font.render("Field (Empty)", True, WHITE)
            self.screen.blit(empty_text, (field_rect.x + 10, field_rect.y + 10))
            return
            
        for i, card in enumerate(self.game_controller.field.cards):
            x = 100 + (i % 8) * (CARD_WIDTH * 0.8)
            y = 250 + (i // 8) * (CARD_HEIGHT * 0.6)
            card.rect.topleft = (x, y)
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
        if self.game_controller.current_player:
            turn_text_str = f"Turn: {self.game_controller.current_player.name}"
            turn_text = self.font.render(turn_text_str, True, WHITE)
            self.screen.blit(turn_text, (SCREEN_WIDTH - 250, 50))

        # Display game state
        state_text = self.small_font.render(f"State: {self.game_controller.game_state}", True, WHITE)
        self.screen.blit(state_text, (SCREEN_WIDTH - 250, 80))

        # Display round info
        round_text = self.small_font.render(f"Round: {self.game_controller.current_month}/12", True, WHITE)
        self.screen.blit(round_text, (SCREEN_WIDTH - 250, 100))

        # Display scores
        player_score_text = self.small_font.render(f"Player Score: {self.game_controller.player.total_score}", True, WHITE)
        self.screen.blit(player_score_text, (SCREEN_WIDTH - 250, 120))
        
        cpu_score_text = self.small_font.render(f"CPU Score: {self.game_controller.cpu.total_score}", True, WHITE)
        self.screen.blit(cpu_score_text, (SCREEN_WIDTH - 250, 140))

        # Display player yaku
        if self.game_controller.player.yaku_list:
            player_yaku_str = f"Player Yaku: {[y[0] for y in self.game_controller.player.yaku_list]}"
            player_yaku_text = self.small_font.render(player_yaku_str, True, WHITE)
            self.screen.blit(player_yaku_text, (SCREEN_WIDTH - 250, 170))

        # Display CPU yaku
        if self.game_controller.cpu.yaku_list:
            cpu_yaku_str = f"CPU Yaku: {[y[0] for y in self.game_controller.cpu.yaku_list]}"
            cpu_yaku_text = self.small_font.render(cpu_yaku_str, True, WHITE)
            self.screen.blit(cpu_yaku_text, (SCREEN_WIDTH - 250, 190))

        # Draw Koikoi choice dialog
        if self.game_controller.game_state == GAME_STATE_KOIKOI_CHOICE:
            self.draw_koikoi_choice()

        # Draw round end/game end messages
        if self.game_controller.game_state == GAME_STATE_ROUND_END:
            self.draw_round_end()
        elif self.game_controller.game_state == GAME_STATE_GAME_END:
            self.draw_game_end()

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
            
            # Handle Koikoi choice buttons
            if self.game_controller.game_state == GAME_STATE_KOIKOI_CHOICE:
                self.handle_koikoi_choice(event)
            
            # Handle round end/game end buttons
            if self.game_controller.game_state == GAME_STATE_ROUND_END:
                self.handle_round_end(event)
            elif self.game_controller.game_state == GAME_STATE_GAME_END:
                self.handle_game_end(event)

    def draw_koikoi_choice(self):
        """Draws the Koikoi choice dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw dialog box
        dialog_width, dialog_height = 400, 200
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, WHITE, dialog_rect)
        pygame.draw.rect(self.screen, BLACK, dialog_rect, 3)
        
        # Draw text
        yaku_text = self.font.render("You achieved a Yaku!", True, BLACK)
        choice_text = self.font.render("Choose your action:", True, BLACK)
        
        self.screen.blit(yaku_text, (dialog_x + 20, dialog_y + 20))
        self.screen.blit(choice_text, (dialog_x + 20, dialog_y + 60))
        
        # Draw buttons
        self.koikoi_button = pygame.Rect(dialog_x + 50, dialog_y + 120, 120, 40)
        self.shobu_button = pygame.Rect(dialog_x + 230, dialog_y + 120, 120, 40)
        
        pygame.draw.rect(self.screen, (100, 255, 100), self.koikoi_button)
        pygame.draw.rect(self.screen, (255, 100, 100), self.shobu_button)
        pygame.draw.rect(self.screen, BLACK, self.koikoi_button, 2)
        pygame.draw.rect(self.screen, BLACK, self.shobu_button, 2)
        
        koikoi_text = self.font.render("Koikoi", True, BLACK)
        shobu_text = self.font.render("Shobu", True, BLACK)
        
        self.screen.blit(koikoi_text, (self.koikoi_button.x + 25, self.koikoi_button.y + 10))
        self.screen.blit(shobu_text, (self.shobu_button.x + 25, self.shobu_button.y + 10))

    def handle_koikoi_choice(self, event):
        """Handles clicking on Koikoi choice buttons."""
        if hasattr(self, 'koikoi_button') and self.koikoi_button.collidepoint(event.pos):
            self.game_controller.player_chooses_koikoi()
        elif hasattr(self, 'shobu_button') and self.shobu_button.collidepoint(event.pos):
            self.game_controller.player_chooses_shobu()

    def draw_round_end(self):
        """Draws the round end screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        dialog_width, dialog_height = 500, 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, WHITE, dialog_rect)
        pygame.draw.rect(self.screen, BLACK, dialog_rect, 3)
        
        # Display round results
        winner = self.game_controller.winner_of_round
        if winner:
            winner_text = self.font.render(f"Round {self.game_controller.current_month} Winner: {winner.name}", True, BLACK)
            score_text = self.font.render(f"Points gained: {winner.monthly_score}", True, BLACK)
        else:
            winner_text = self.font.render(f"Round {self.game_controller.current_month}: Draw", True, BLACK)
            score_text = self.font.render("No points awarded", True, BLACK)
        
        total_score_text = self.font.render(f"Total Scores - Player: {self.game_controller.player.total_score}, CPU: {self.game_controller.cpu.total_score}", True, BLACK)
        
        self.screen.blit(winner_text, (dialog_x + 20, dialog_y + 20))
        self.screen.blit(score_text, (dialog_x + 20, dialog_y + 60))
        self.screen.blit(total_score_text, (dialog_x + 20, dialog_y + 100))
        
        # Next round button
        self.next_round_button = pygame.Rect(dialog_x + 200, dialog_y + 200, 100, 40)
        pygame.draw.rect(self.screen, (100, 255, 100), self.next_round_button)
        pygame.draw.rect(self.screen, BLACK, self.next_round_button, 2)
        
        next_text = self.font.render("Next", True, BLACK)
        self.screen.blit(next_text, (self.next_round_button.x + 25, self.next_round_button.y + 10))

    def handle_round_end(self, event):
        """Handles clicking on round end buttons."""
        if hasattr(self, 'next_round_button') and self.next_round_button.collidepoint(event.pos):
            self.game_controller.next_round()

    def draw_game_end(self):
        """Draws the game end screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        dialog_width, dialog_height = 500, 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, WHITE, dialog_rect)
        pygame.draw.rect(self.screen, BLACK, dialog_rect, 3)
        
        # Display final results
        game_end_text = self.font.render("Game Over!", True, BLACK)
        player_score = self.game_controller.player.total_score
        cpu_score = self.game_controller.cpu.total_score
        
        if player_score > cpu_score:
            winner_text = self.font.render("You Win!", True, BLACK)
        elif cpu_score > player_score:
            winner_text = self.font.render("CPU Wins!", True, BLACK)
        else:
            winner_text = self.font.render("It's a Tie!", True, BLACK)
        
        final_score_text = self.font.render(f"Final Scores - Player: {player_score}, CPU: {cpu_score}", True, BLACK)
        
        self.screen.blit(game_end_text, (dialog_x + 180, dialog_y + 20))
        self.screen.blit(winner_text, (dialog_x + 180, dialog_y + 60))
        self.screen.blit(final_score_text, (dialog_x + 50, dialog_y + 100))
        
        # Restart button
        self.restart_button = pygame.Rect(dialog_x + 200, dialog_y + 200, 100, 40)
        pygame.draw.rect(self.screen, (100, 255, 100), self.restart_button)
        pygame.draw.rect(self.screen, BLACK, self.restart_button, 2)
        
        restart_text = self.font.render("Restart", True, BLACK)
        self.screen.blit(restart_text, (self.restart_button.x + 15, self.restart_button.y + 10))

    def handle_game_end(self, event):
        """Handles clicking on game end buttons."""
        if hasattr(self, 'restart_button') and self.restart_button.collidepoint(event.pos):
            self.game_controller.restart_game()

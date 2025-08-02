# card.py
# Represents a single Hanafuda card

import pygame
from constants import CARD_WIDTH, CARD_HEIGHT, BLACK, WHITE

# Define some colors for different card types for placeholder graphics
CATEGORY_COLORS = {
    'hikari': (255, 255, 0),   # Gold
    'tane': (255, 0, 0),       # Red
    'tan': (0, 0, 255),         # Blue
    'kasu': (128, 128, 128),  # Grey
}

class Card:
    def __init__(self, month, category, name, points=0):
        self.month = month
        self.category = category
        self.name = name
        self.points = points
        self.image = self._create_placeholder_image()
        self.rect = self.image.get_rect()
        self.is_face_up = True

    def _create_placeholder_image(self):
        """Creates a placeholder image for the card."""
        image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))

        # Get color based on category, default to white
        color = CATEGORY_COLORS.get(self.category, WHITE)
        image.fill(color)

        # Draw a border
        pygame.draw.rect(image, BLACK, image.get_rect(), 2)

        # Add text with better formatting
        font = pygame.font.Font(None, 16)
        small_font = pygame.font.Font(None, 14)
        
        month_text = font.render(f"{self.month}月", True, BLACK)
        cat_text = font.render(self.category.capitalize(), True, BLACK)
        
        # Truncate long names
        display_name = self.name
        if len(display_name) > 8:
            display_name = display_name[:8] + "..."
        name_text = small_font.render(display_name, True, BLACK)
        
        # Points display
        if self.points > 1:
            points_text = small_font.render(f"{self.points}pt", True, BLACK)
            image.blit(points_text, (5, CARD_HEIGHT - 20))

        image.blit(month_text, (5, 5))
        image.blit(cat_text, (5, 25))
        image.blit(name_text, (5, 45))

        return image

    def draw(self, surface):
        """Draws the card on the given surface."""
        surface.blit(self.image, self.rect)

    def __repr__(self):
        return f"Card({self.month}, '{self.name}', '{self.category}')"

# deck.py
# Manages the deck of Hanafuda cards

import random
from card import Card

# Complete Hanafuda card data
# Structure: (month, name, category, points)
CARD_DATA = [
    # January (Matsu - Pine)
    (1, "Tsuru", "hikari", 20),
    (1, "Akatan", "tan", 5),
    (1, "Kasu", "kasu", 1),
    (1, "Kasu", "kasu", 1),
    # February (Ume - Plum Blossom)
    (2, "Uguisu", "tane", 10),
    (2, "Akatan", "tan", 5),
    (2, "Kasu", "kasu", 1),
    (2, "Kasu", "kasu", 1),
    # March (Sakura - Cherry Blossom)
    (3, "Maku", "hikari", 20),
    (3, "Akatan", "tan", 5),
    (3, "Kasu", "kasu", 1),
    (3, "Kasu", "kasu", 1),
    # April (Fuji - Wisteria)
    (4, "Hototogisu", "tane", 10),
    (4, "Tan", "tan", 5),
    (4, "Kasu", "kasu", 1),
    (4, "Kasu", "kasu", 1),
    # May (Ayame - Iris)
    (5, "Yatsuhashi", "tane", 10),
    (5, "Tan", "tan", 5),
    (5, "Kasu", "kasu", 1),
    (5, "Kasu", "kasu", 1),
    # June (Botan - Peony)
    (6, "Chou", "tane", 10),
    (6, "Aotan", "tan", 5),
    (6, "Kasu", "kasu", 1),
    (6, "Kasu", "kasu", 1),
    # July (Hagi - Bush Clover)
    (7, "Inoshishi", "tane", 10),
    (7, "Tan", "tan", 5),
    (7, "Kasu", "kasu", 1),
    (7, "Kasu", "kasu", 1),
    # August (Susuki - Pampas Grass)
    (8, "Tsuki", "hikari", 20),
    (8, "Gan", "tane", 10),
    (8, "Kasu", "kasu", 1),
    (8, "Kasu", "kasu", 1),
    # September (Kiku - Chrysanthemum)
    (9, "Sakazuki", "tane", 10), # Special card, can be 10 or 1 pt
    (9, "Aotan", "tan", 5),
    (9, "Kasu", "kasu", 1),
    (9, "Kasu", "kasu", 1),
    # October (Momiji - Maple)
    (10, "Shika", "tane", 10),
    (10, "Aotan", "tan", 5),
    (10, "Kasu", "kasu", 1),
    (10, "Kasu", "kasu", 1),
    # November (Yanagi - Willow)
    (11, "Ono no Michikaze", "hikari", 20),
    (11, "Tsubame", "tane", 10),
    (11, "Tan", "tan", 5),
    (11, "Kasu", "kasu", 1),
    # December (Kiri - Paulownia)
    (12, "Ho-oh", "hikari", 20),
    (12, "Kasu", "kasu", 1),
    (12, "Kasu", "kasu", 1),
    (12, "Kasu", "kasu", 1),
]


class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        """Creates a full 48-card deck from the CARD_DATA."""
        self.cards = []
        for month, name, category, points in CARD_DATA:
            # The Card class now takes month, category, and points.
            # I'm passing the name to the category for now to have more specific placeholders.
            # This can be refined later. A 'name' attribute should be added to Card.
            # For now, let's just pass the main category.
            card = Card(month, category, points)
            # A better approach would be to add a 'name' attribute to the Card class.
            # Let's modify the card class to accept a name.
            # No, let's stick to the plan and modify the deck first.
            # I will modify the Card class later if needed.
            # The category is enough for the placeholder graphics.
            self.cards.append(card)


    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal(self, num_cards):
        """Deals a specified number of cards from the deck."""
        if len(self.cards) < num_cards:
            # This should not happen in a normal game, but good to have a check
            dealt_cards = self.cards[:]
            self.cards = []
            return dealt_cards

        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

    def is_empty(self):
        """Checks if the deck is empty."""
        return len(self.cards) == 0

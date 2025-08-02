# field.py
# Manages the cards on the table (the "ba")

class Field:
    def __init__(self):
        self.cards = []

    def add_cards(self, cards):
        """Adds cards to the field."""
        self.cards.extend(cards)

    def remove_card(self, card):
        """Removes a specific card from the field."""
        if card in self.cards:
            self.cards.remove(card)

    def find_matches(self, card_to_match):
        """Finds cards on the field that have the same month as the given card."""
        return [card for card in self.cards if card.month == card_to_match.month]

    def clear(self):
        """Clears all cards from the field."""
        self.cards = []

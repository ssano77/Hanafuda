# player.py
# Represents a player in the game

class Player:
    def __init__(self, name, is_parent=False, is_cpu=False):
        self.name = name
        self.is_cpu = is_cpu
        self.is_parent = is_parent
        self.hand = []  # Cards in the player's hand
        self.captured_cards = [] # Cards won by the player
        self.yaku_list = [] # List of yaku achieved in the current round
        self.monthly_score = 0 # Score for the current month/round
        self.total_score = 0 # Total score for the whole game
        self.has_koikoied = False # Flag for "koikoi"

    def add_cards_to_hand(self, cards):
        """Adds a list of cards to the player's hand."""
        self.hand.extend(cards)

    def play_card(self, card):
        """Removes a card from the hand to be played."""
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None

    def capture_cards(self, cards):
        """Adds cards to the player's captured pile."""
        self.captured_cards.extend(cards)

    def choose_card_to_play(self, field_cards):
        """
        Logic for choosing a card.
        For CPU, this will contain the AI logic.
        For a human player, this might just wait for input.
        """
        if self.is_cpu:
            # Basic AI: find the first playable card
            for hand_card in self.hand:
                for field_card in field_cards:
                    if hand_card.month == field_card.month:
                        return hand_card
            # If no match, play the first card
            return self.hand[0] if self.hand else None
        else:
            # Human player logic is handled by UIManager
            return None

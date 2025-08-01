# game_controller.py
# Manages the overall game logic and state.

from deck import Deck
from player import Player
from field import Field
from yaku import Yaku
from constants import GAME_STATE_START, GAME_STATE_PLAYER_TURN, GAME_STATE_CPU_TURN

class GameController:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player 1")
        self.cpu = Player("CPU", is_cpu=True)
        self.field = Field()
        self.yaku_checker = Yaku()
        self.current_player = self.player
        self.game_state = GAME_STATE_START
        self.setup_game()

    def setup_game(self):
        """Deals the initial cards to players and the field."""
        self.deck.shuffle()
        self.player.add_cards_to_hand(self.deck.deal(8))
        self.cpu.add_cards_to_hand(self.deck.deal(8))
        self.field.add_cards(self.deck.deal(8))
        self.game_state = GAME_STATE_PLAYER_TURN

    def update(self):
        """Main update loop for the game logic."""
        if self.game_state == GAME_STATE_CPU_TURN and self.current_player == self.cpu:
            self.execute_cpu_turn()

    def _handle_play(self, played_card, player):
        """Handles the logic of playing one card (either from hand or deck)."""
        matches = self.field.find_matches(played_card)

        if len(matches) == 1:
            # One match found, capture both cards
            match_card = matches[0]
            self.field.remove_card(match_card)
            player.capture_cards([played_card, match_card])
            print(f"{player.name} captured {played_card} and {match_card}")
        elif len(matches) > 1:
            # Multiple matches found, player must choose.
            # For now, we'll simplify and just take the first one.
            # TODO: Implement choice for the player.
            match_card = matches[0]
            self.field.remove_card(match_card)
            player.capture_cards([played_card, match_card])
            print(f"{player.name} captured {played_card} and {match_card} (chose first of multiple)")
        else:
            # No match, add the card to the field
            self.field.add_cards([played_card])
            print(f"{played_card} added to the field.")

    def execute_turn(self, hand_card):
        """Executes a full turn for the current player using a chosen card."""
        if self.current_player.is_cpu:
            player = self.cpu
        else:
            player = self.player

        # 1. Play card from hand
        card_from_hand = player.play_card(hand_card)
        if card_from_hand:
            print(f"{player.name} plays {card_from_hand} from hand.")
            self._handle_play(card_from_hand, player)

        # 2. Draw card from deck
        if not self.deck.is_empty():
            card_from_deck = self.deck.deal(1)[0]
            print(f"{player.name} draws {card_from_deck} from deck.")
            self._handle_play(card_from_deck, player)

        # 3. Check for yaku
        self.check_for_yaku(player)

        # 4. Switch turns
        self.switch_turns()

    def execute_cpu_turn(self):
        """Carries out the CPU's turn."""
        print("\n--- CPU's Turn ---")
        card_to_play = self.cpu.choose_card_to_play(self.field.cards)
        if card_to_play:
            self.execute_turn(card_to_play)
        else:
            # CPU has no cards left, should not happen in a normal game
            self.switch_turns()

    def switch_turns(self):
        """Switches the current player."""
        if self.current_player == self.player:
            self.current_player = self.cpu
            self.game_state = GAME_STATE_CPU_TURN
        else:
            self.current_player = self.player
            self.game_state = GAME_STATE_PLAYER_TURN
        print(f"--- It's now {self.current_player.name}'s turn. ---")

    def check_for_yaku(self, player):
        """Checks for yaku for the given player and updates their score."""
        new_yaku = self.yaku_checker.check_yaku(player.captured_cards)
        if new_yaku:
            player.yaku_list = new_yaku
            # TODO: Handle scoring and koikoi logic
            print(f"{player.name} formed yaku: {new_yaku}")

    # This method is now the entry point from the UI for a player's move
    def player_plays_card(self, hand_card):
        if self.current_player == self.player and self.game_state == GAME_STATE_PLAYER_TURN:
            print(f"\n--- {self.player.name}'s Turn ---")
            self.execute_turn(hand_card)
        else:
            print("Not player's turn!")

# game_controller.py
# Manages the overall game logic and state.

import random
from deck import Deck
from player import Player
from field import Field
from yaku import Yaku
from constants import *

class GameController:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("You")
        self.cpu = Player("CPU", is_cpu=True)
        self.field = Field()
        self.yaku_checker = Yaku()

        self.current_month = 1
        self.parent_player = None
        self.current_player = None

        self.game_state = GAME_STATE_START
        self.winner_of_round = None

    def start_game(self):
        """Starts a new 12-round game."""
        self._determine_first_parent()
        self.start_round()

    def start_round(self):
        """Sets up and starts a new round (month)."""
        if self.current_month > 12:
            self.game_state = GAME_STATE_GAME_END
            return

        # Reset players and field for the new round
        self.deck = Deck()
        self.field.clear()
        for p in [self.player, self.cpu]:
            p.hand.clear()
            p.captured_cards.clear()
            p.yaku_list.clear()
            p.monthly_score = 0
            p.has_koikoied = False

        # Deal cards
        self.deck.shuffle()
        self.parent_player.add_cards_to_hand(self.deck.deal(8))
        self.get_other_player(self.parent_player).add_cards_to_hand(self.deck.deal(8))
        self.field.add_cards(self.deck.deal(8))

        # TODO: Check for initial yaku (Teyon, Kuttsuki)

        self.current_player = self.parent_player
        self.game_state = GAME_STATE_PLAYER_TURN if self.current_player == self.player else GAME_STATE_CPU_TURN
        self.winner_of_round = None

    def _determine_first_parent(self):
        """Randomly selects the parent for the first round."""
        if random.choice([True, False]):
            self.player.is_parent = True
            self.cpu.is_parent = False
            self.parent_player = self.player
        else:
            self.player.is_parent = False
            self.cpu.is_parent = True
            self.parent_player = self.cpu

    def execute_turn(self, hand_card):
        """Executes a full turn for the current player."""
        player = self.current_player

        # 1. Play card from hand
        card_from_hand = player.play_card(hand_card)
        if card_from_hand:
            self._handle_play(card_from_hand, player)

        # 2. Draw card from deck
        if not self.deck.is_empty():
            card_from_deck = self.deck.deal(1)[0]
            self._handle_play(card_from_deck, player)

        # 3. Check for yaku and decide next step
        self._check_yaku_and_decide(player)

    def _handle_play(self, played_card, player):
        """Handles the logic of matching a played card with cards on the field."""
        matches = self.field.find_matches(played_card)
        if matches:
            # TODO: Handle multiple matches - for now, take the first
            match_card = matches[0]
            self.field.remove_card(match_card)
            player.capture_cards([played_card, match_card])
        else:
            self.field.add_cards([played_card])

    def _check_yaku_and_decide(self, player):
        """Checks for yaku and transitions the game state."""
        new_yaku = self.yaku_checker.check_yaku(player.captured_cards)

        if new_yaku:
            # Check if it's a new, higher-scoring yaku combination
            current_score = sum(y[1] for y in player.yaku_list)
            new_score = sum(y[1] for y in new_yaku)

            if new_score > current_score:
                player.yaku_list = new_yaku
                player.monthly_score = new_score

                if player.is_cpu:
                    # Simple AI: CPU always calls koikoi once, then stops.
                    if player.has_koikoied:
                        self.player_chooses_shobu() # Win
                    else:
                        self.player_chooses_koikoi() # Koikoi
                else:
                    self.game_state = GAME_STATE_KOIKOI_CHOICE
                return

        # If no new yaku or player chose koikoi, switch turns
        self.switch_turns()

    def player_chooses_koikoi(self):
        """Called when the player decides to 'koikoi'."""
        self.current_player.has_koikoied = True
        self.switch_turns()

    def player_chooses_shobu(self):
        """Called when the player decides to 'shobu' (win the round)."""
        self.winner_of_round = self.current_player
        self._calculate_final_score()
        self.game_state = GAME_STATE_ROUND_END

    def _calculate_final_score(self):
        """Calculates the score at the end of a round."""
        winner = self.winner_of_round
        loser = self.get_other_player(winner)

        score = winner.monthly_score

        # Double score if opponent had called koikoi
        if loser.has_koikoied:
            score *= 2

        # Double score if yaku points are 7 or more
        if winner.monthly_score >= 7:
            score *= 2

        winner.total_score += score

    def switch_turns(self):
        """Switches the current player and checks for end-of-round conditions."""
        if not self.player.hand and not self.cpu.hand:
            # Draw game (both players out of cards)
            self.winner_of_round = self.parent_player
            self.parent_player.total_score += 6 # Parent gets 6 points
            self.game_state = GAME_STATE_ROUND_END
            return

        self.current_player = self.get_other_player(self.current_player)
        self.game_state = GAME_STATE_PLAYER_TURN if self.current_player == self.player else GAME_STATE_CPU_TURN

    def next_round(self):
        """Advances to the next month/round."""
        self.current_month += 1

        # The winner of the round becomes the next parent
        if self.winner_of_round:
            self.parent_player = self.winner_of_round
            self.parent_player.is_parent = True
            other = self.get_other_player(self.parent_player)
            other.is_parent = False
        # If it was a draw, parent does not change.

        self.start_round()

    def get_other_player(self, player):
        """Returns the other player."""
        return self.cpu if player == self.player else self.player

    # UI-facing methods
    def player_plays_card(self, hand_card):
        if self.current_player == self.player and self.game_state == GAME_STATE_PLAYER_TURN:
            self.execute_turn(hand_card)

    def cpu_turn(self):
        if self.current_player == self.cpu and self.game_state == GAME_STATE_CPU_TURN:
            card_to_play = self.cpu.choose_card_to_play(self.field.cards)
            if card_to_play:
                self.execute_turn(card_to_play)
            else:
                self.switch_turns() # CPU has no cards left

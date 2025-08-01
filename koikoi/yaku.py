# yaku.py
# Checks for winning combinations (Yaku)

class Yaku:
    def check_yaku(self, captured_cards):
        """
        Checks the player's captured cards against all yaku definitions.
        Returns a list of (yaku_name, points) tuples.
        """
        achieved_yaku = []

        # Categorize cards
        hikari = [c for c in captured_cards if c.category == 'hikari']
        tane = [c for c in captured_cards if c.category == 'tane']
        tan = [c for c in captured_cards if c.category == 'tan']
        kasu = [c for c in captured_cards if c.category == 'kasu']

        # --- Hikari Yaku (Bright Cards) ---
        # Note: This doesn't distinguish between Goko, Shiko, Ame-Shiko, and Sanko properly.
        # It just checks the count. A full implementation needs to check for the Rainman card.
        num_hikari = len(hikari)
        if num_hikari == 5:
            achieved_yaku.append(("Goko", 10))
        elif num_hikari == 4:
            # TODO: Check for Ono no Michikaze (Rainman) to distinguish Shiko and Ame-Shiko
            achieved_yaku.append(("Shiko", 8))
        elif num_hikari == 3:
            # TODO: Check for Ono no Michikaze (Rainman) to ensure it's not part of the 3
            achieved_yaku.append(("Sanko", 6))

        # --- Tane Yaku (Animal Cards) ---
        # TODO: This doesn't check for Ino-Shika-Cho (Boar-Deer-Butterfly)
        num_tane = len(tane)
        if num_tane >= 5:
            points = 1 + (num_tane - 5)
            achieved_yaku.append(("Tane", points))

        # --- Tan Yaku (Ribbon Cards) ---
        # TODO: This doesn't check for Akatan, Aotan, or specific ribbon combinations.
        num_tan = len(tan)
        if num_tan >= 5:
            points = 1 + (num_tan - 5)
            achieved_yaku.append(("Tan", points))

        # --- Kasu Yaku (Chaff Cards) ---
        num_kasu = len(kasu)
        if num_kasu >= 10:
            points = 1 + (num_kasu - 10)
            achieved_yaku.append(("Kasu", points))

        # A player can have multiple yaku, so we return all of them.
        # The game controller will decide how to combine scores.
        return achieved_yaku

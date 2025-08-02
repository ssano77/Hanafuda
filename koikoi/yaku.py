# yaku.py
# Checks for winning combinations (Yaku)

class Yaku:
    def check_yaku(self, captured_cards):
        """
        Checks the player's captured cards against all yaku definitions.
        Returns a list of (yaku_name, points) tuples.
        """
        achieved_yaku = []
        card_names = {c.name for c in captured_cards}

        # Categorize cards
        hikari = [c for c in captured_cards if c.category == 'hikari']
        tane = [c for c in captured_cards if c.category == 'tane']
        tan = [c for c in captured_cards if c.category == 'tan']
        kasu = [c for c in captured_cards if c.category == 'kasu']

        # --- Yaku Checks ---
        is_goko = self._check_goko(hikari)
        if is_goko:
            achieved_yaku.append(("Goko", 10))
        else:
            # Shiko, Ame-Shiko, and Sanko are mutually exclusive with Goko
            is_shiko, is_ame_shiko = self._check_shiko_and_ameshiko(hikari)
            if is_ame_shiko:
                achieved_yaku.append(("Ame-Shiko", 7))
            elif is_shiko:
                achieved_yaku.append(("Shiko", 8))
            else:
                is_sanko = self._check_sanko(hikari)
                if is_sanko:
                    achieved_yaku.append(("Sanko", 5)) # Corrected from 6 to 5

        if self._check_inoshikacho(tane):
            achieved_yaku.append(("Ino-Shika-Cho", 5))

        if self._check_akatan(tan):
            achieved_yaku.append(("Akatan", 5))

        if self._check_aotan(tan):
            achieved_yaku.append(("Aotan", 5))

        if self._check_hanamizake(card_names):
            achieved_yaku.append(("Hanami-de-Ippai", 5))

        if self._check_tsukimizake(card_names):
            achieved_yaku.append(("Tsukimi-de-Ippai", 5))

        # --- Point-based Yaku (can stack with others) ---
        num_tane = len(tane)
        if num_tane >= 5:
            points = 1 + (num_tane - 5)
            achieved_yaku.append(("Tane", points))

        num_tan = len(tan)
        if num_tan >= 5:
            # Akatan/Aotan bonuses are handled separately, so we just count them
            points = 1 + (num_tan - 5)
            achieved_yaku.append(("Tan", points))

        num_kasu = len(kasu)
        if num_kasu >= 10:
            points = 1 + (num_kasu - 10)
            achieved_yaku.append(("Kasu", points))

        return achieved_yaku

    def _check_goko(self, hikari_cards):
        """Checks for Goko (Five Brights)."""
        return len(hikari_cards) == 5

    def _check_shiko_and_ameshiko(self, hikari_cards):
        """Checks for Shiko (Four Brights) and Ame-Shiko (Rainy Four Brights)."""
        if len(hikari_cards) != 4:
            return False, False

        has_rainman = any(c.name == "Ono no Michikaze" for c in hikari_cards)
        if has_rainman:
            return False, True # Ame-Shiko
        else:
            return True, False # Shiko

    def _check_sanko(self, hikari_cards):
        """Checks for Sanko (Three Brights)."""
        if len(hikari_cards) != 3:
            return False
        # Must not contain the Rainman
        return not any(c.name == "Ono no Michikaze" for c in hikari_cards)

    def _check_inoshikacho(self, tane_cards):
        """Checks for Ino-Shika-Cho (Boar, Deer, Butterfly)."""
        names = {c.name for c in tane_cards}
        return {"Inoshishi", "Shika", "Chou"}.issubset(names)

    def _check_akatan(self, tan_cards):
        """Checks for Akatan (Red Poetry Ribbons)."""
        # Checks for the three 'Akatan' cards from months 1, 2, 3
        akatan_months = {c.month for c in tan_cards if c.name == 'Akatan'}
        return {1, 2, 3}.issubset(akatan_months)

    def _check_aotan(self, tan_cards):
        """Checks for Aotan (Blue Poetry Ribbons)."""
        # Checks for the three 'Aotan' cards from months 6, 9, 10
        aotan_months = {c.month for c in tan_cards if c.name == 'Aotan'}
        return {6, 9, 10}.issubset(aotan_months)

    def _check_hanamizake(self, card_names):
        """Checks for Hanami-de-Ippai (Flower Viewing)."""
        return {"Maku", "Sakazuki"}.issubset(card_names)

    def _check_tsukimizake(self, card_names):
        """Checks for Tsukimi-de-Ippai (Moon Viewing)."""
        return {"Tsuki", "Sakazuki"}.issubset(card_names)

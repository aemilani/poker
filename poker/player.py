import random


class Player:
    def __init__(self, name: str, stack: float, is_bot: bool = True, player_type: str = 'rand'):
        self.name = name
        self.stack = stack
        self.is_bot = is_bot
        self.player_type = player_type
        self.hand = []
        self.table = []
        self.placed_bet = 0

        if self.is_bot:
            if self.player_type == 'rand':
                self.tightness = random.random()
                self.aggressiveness = random.random()
            elif self.player_type == 'la':
                self.tightness = 0.1
                self.aggressiveness = 0.9
            elif self.player_type == 'lp':
                self.tightness = 0.1
                self.aggressiveness = 0.1
            elif self.player_type == 'ta':
                self.tightness = 0.9
                self.aggressiveness = 0.9
            elif self.player_type == 'tp':
                self.tightness = 0.9
                self.aggressiveness = 0.1
            else:
                print("Invalid player_type. Set to 'rand'.")
                self.tightness = random.random()
                self.aggressiveness = random.random()

    def act(self) -> str | None:
        if self.is_bot:
            cards = []
            if self.hand:
                cards.extend(self.hand)
            if self.table:
                cards.extend(self.table)
            if len(cards) == 0:
                print("Hands are not dealt yet.")
                return None
            elif len(cards) == 2:  # Pre-flop
                val = sum([card.value for card in cards])
                max_val = 24
                if val >= self.tightness * max_val:  # play
                    bet_thr = val / max_val * (1 - self.aggressiveness)
                    max_bet_amount = val / max_val * self.aggressiveness * self.stack
                    max_bet_amount = round(max_bet_amount, 2)
                    bet_rand = random.random()
                    if bet_rand >= bet_thr:
                        return f"call/raise {max_bet_amount}"
                    else:
                        return "check/fold"
                else:
                    return "check/fold"
        else:
            print("Player is not bot.")
            return None

    def bet(self, amount: float) -> None:
        self.stack -= amount
        self.placed_bet += amount

    def win(self, amount: float) -> None:
        self.stack += amount
        self.placed_bet = 0

    def lose(self) -> None:
        self.placed_bet = 0

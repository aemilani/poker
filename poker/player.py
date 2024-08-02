import random
from poker.utils import get_hand_value, get_full_hand_value
from poker.constants import ConvDict


class Player:
    def __init__(self, name: str, stack: int, is_bot: bool = True, player_type: str = 'rand'):
        self.name = name
        self.stack = stack
        self.is_bot = is_bot
        self.player_type = player_type
        self.hand = None
        self.table = None
        self.placed_bet = 0
        self.action = None

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
                val = get_hand_value(cards)
                max_val = 169
                if val >= self.tightness * max_val:  # play
                    bet_thr = 1 - val / max_val * self.aggressiveness
                    max_bet_amount = val / max_val * self.aggressiveness * self.stack
                    max_bet_amount = int(max_bet_amount)
                    bet_rand = random.random()
                    if bet_rand >= bet_thr:
                        return f"call/raise {max_bet_amount}"
                    else:
                        return "check/fold"
                else:
                    return "check/fold"
            elif 5 <= len(cards) <= 7:  # Post-flop
                combos = get_full_hand_value(cards)
                if combos[0][0] == 'high_card':
                    return "check/fold"
                elif combos[0][0] == 'pair':
                    if combos[0][1] in [ConvDict.RANK[c.rank] for c in self.hand]:
                        return "call"
                    else:
                        return "check/fold"
                elif combos[0][0] == 'two_pair':
                    if combos[0][1][0] in [ConvDict.RANK[c.rank] for c in self.hand] or \
                            combos[0][1][1] in [ConvDict.RANK[c.rank] for c in self.hand]:
                        return "call"
                    else:
                        return "check/fold"
                elif combos[0][0] == 'three_of_a_kind':
                    if combos[0][1] in [ConvDict.RANK[c.rank] for c in self.hand]:
                        return f"raise {int(0.1 * self.stack) + 1}"
                    else:
                        return "check/fold"
                elif combos[0][0] == 'straight':
                    if ConvDict.RANK[self.hand[0].rank] in combos[0][1] or \
                            ConvDict.RANK[self.hand[1].rank] in combos[0][1]:
                        return f"raise {int(0.2 * self.stack) + 1}"
                    else:
                        return "check/fold"
                elif combos[0][0] == 'full_house':
                    if combos[0][1][0] in [ConvDict.RANK[c.rank] for c in self.hand] or \
                            combos[0][1][1] in [ConvDict.RANK[c.rank] for c in self.hand]:
                        return f"raise {int(0.6 * self.stack) + 1}"
                    else:
                        return "check/fold"
                else:
                    return "all_in"
            else:
                print("Error in the number of cards dealt.")
        else:
            print("Player is not bot.")
            return None

    def bet(self, amount: int) -> None:
        if amount > self.stack:
            amount = self.stack
        self.stack -= amount
        self.placed_bet += amount

    def win(self, amount: int) -> None:
        self.stack += amount
        self.hand = []
        self.table = []
        self.placed_bet = 0

    def lose(self) -> None:
        self.hand = []
        self.table = []
        self.placed_bet = 0

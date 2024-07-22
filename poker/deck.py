import random


CLUB = '\u2663'
DIAMOND = '\u2666'
HEART = '\u2665'
SPADE = '\u2660'

RED = '\033[91m'
BLACK = '\033[90m'
RESET = '\033[0m'

suit_dict = {0: f"{BLACK}{CLUB}{RESET}", 1: f"{RED}{DIAMOND}{RESET}",
             2: f"{RED}{HEART}{RESET}", 3: f"{BLACK}{SPADE}{RESET}"}
value_dict = {9: "J", 10: "Q", 11: "K", 12: "A"}


class Card:
    def __init__(self, suit: int, value: int):
        self.suit = suit
        self.value = value

    def __repr__(self):
        if self.value in value_dict:
            return value_dict[self.value] + suit_dict[self.suit]
        else:
            return str(self.value + 2) + suit_dict[self.suit]


class Deck(list):
    def __init__(self):
        super().__init__()
        for suit in range(4):
            for value in range(13):
                self.append(Card(suit, value))

    def shuffle(self) -> None:
        random.shuffle(self)

    def deal(self, n_cards: int) -> list[Card]:
        dealt_cards = []
        for _ in range(n_cards):
            dealt_cards.append(self.pop(0))
        return dealt_cards


deck = Deck()
deck.shuffle()
whole_cards = deck.deal(2)
community_cards = deck.deal(5)
print(f"Whole cards: {whole_cards}")
print(f"Community cards: {community_cards}")

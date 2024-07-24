import random
from poker.card import Card


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

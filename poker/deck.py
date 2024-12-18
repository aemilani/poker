import random
from poker.card import Card


class Deck(list):
    def __init__(self):
        super().__init__()
        for suit in range(4):
            for value in range(2, 15):
                self.append(Card(suit, value))

    def shuffle(self) -> None:
        random.shuffle(self)

    def deal(self, n_cards: int) -> list[Card]:
        dealt_cards = []
        for _ in range(n_cards):
            dealt_cards.append(self.pop(0))
        return dealt_cards


if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    hand = deck.deal(2)
    table = deck.deal(3)
    print(hand, table)

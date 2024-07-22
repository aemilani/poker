from deck import Card


actions = ['bet', 'raise', 'call', 'check', 'fold']


class Player:
    def __init__(self, position: int, stack: float, cards: Card = None):
        self.position = position
        self.stack = stack
        self.cards = cards

    def bet(self, amount: float) -> None:
        self.stack -= amount

    def win(self, amount: float) -> None:
        self.stack += amount

from poker.constants import ConvDict


class Card:
    def __init__(self, suit: int, rank: int):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return ConvDict.RANK[self.rank] + ConvDict.SUIT[self.suit]

    def __gt__(self, other):
        return self.rank > other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __add__(self, other):
        return self.rank + other.rank

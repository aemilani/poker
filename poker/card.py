from enum import Enum


class _SuitShape(Enum):
    CLUB = '\u2663'
    DIAMOND = '\u2666'
    HEART = '\u2665'
    SPADE = '\u2660'


class _SuitColor(Enum):
    RED = '\033[91m'
    BLACK = '\033[90m'
    RESET = '\033[0m'


class Suit(Enum):
    CLUB = f"{_SuitColor.BLACK.value}{_SuitShape.CLUB.value}{_SuitColor.RESET.value}"
    DIAMOND = f"{_SuitColor.RED.value}{_SuitShape.DIAMOND.value}{_SuitColor.RESET.value}"
    HEART = f"{_SuitColor.RED.value}{_SuitShape.HEART.value}{_SuitColor.RESET.value}"
    SPADE = f"{_SuitColor.BLACK.value}{_SuitShape.SPADE.value}{_SuitColor.RESET.value}"


suit_dict = {0: Suit.CLUB.value, 1: Suit.DIAMOND.value, 2: Suit.HEART.value, 3: Suit.SPADE.value}
value_dict = {11: "J", 12: "Q", 13: "K", 14: "A"}


class Card:
    def __init__(self, suit: int, value: int):
        self.suit = suit
        self.value = value

    def __repr__(self):
        if self.value in value_dict:
            return value_dict[self.value] + suit_dict[self.suit]
        else:
            return str(self.value) + suit_dict[self.suit]

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value

    def __add__(self, other):
        return self.value + other.value

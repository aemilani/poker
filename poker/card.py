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
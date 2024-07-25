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


class ConvDict:
    SUIT = {0: Suit.CLUB.value, 1: Suit.DIAMOND.value, 2: Suit.HEART.value, 3: Suit.SPADE.value}
    SUIT_STR = {0: 'C', 1: 'D', 2: 'H', 3: 'S'}
    RANK = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A',
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

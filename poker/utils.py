import random
from poker.card import Card


def get_random_names(n: int = 5) -> list[str]:
    names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Margaret", "Anthony", "Betty", "Mark", "Sandra", "Donald", "Ashley",
        "Steven", "Dorothy", "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna",
        "Kenneth", "Michelle", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
        "Edward", "Deborah"
    ]
    random.shuffle(names)
    return names[:n]


def get_hand_value(hand: list[Card]) -> int:
    hand_str = hand_code(hand)
    hand_order = ("AA, KK, QQ, AKs, JJ, AQs, KQs, AJs, KJs, ATs, QJs, AKo, TT, KTs, QTs, JTs, 99, AQo, A9s, KQo, K9s,"
                  "T9s, A8s, J9s, Q9s, 88, A5s, AJo, A7s, A4s, A3s, KJo, A6s, QJo, 77, A2s, K8s, T8s, 98s, ATo, J8s,"
                  "Q8s, K7s, KTo, JTo, 66, QTo, K6s, 87s, K5s, 97s, 55, T7s, K4s, 76s, 44, K3s, Q7s, J7s, 33, K2s, 22,"
                  "65s, 86s, Q6s, 54s, Q5s, 75s, 96s, T9o, Q4s, T6s, A9o, Q3s, 64s, J6s, Q2s, J9o, 85s, 53s, K9o, J5s,"
                  "Q9o, J4s, A8o, 74s, J3s, 43s, 95s, J2s, T5s, A5o, 63s, T4s, A7o, T8o, T3s, A4o, 52s, 98o, 84s, T2s,"
                  "A3o, 42s, A6o, K8o, 94s, J8o, 73s, 93s, Q8o, 87o, A2o, 32s, 92s, 62s, K7o, 83s, 97o, 76o, 82s, T7o,"
                  "K6o, 72s, 65o, 86o, K5o, 54o, J7o, K4o, Q7o, 75o, K3o, 96o, K2o, Q6o, 64o, Q5o, T6o, 53o, 85o, Q4o,"
                  "J6o, Q3o, 43o, 74o, Q2o, J5o, 95o, J4o, 63o, J3o, T5o, 52o, J2o, T4o, 84o, 42o, T3o, T2o, 73o, 94o,"
                  "32o, 62o, 93o, 92o, 83o, 82o, 72o")
    hand_order = hand_order.replace(" ", "").split(",")
    try:
        return len(hand_order) - hand_order.index(hand_str)
    except ValueError:
        return len(hand_order) - hand_order.index(hand_str[1] + hand_str[0] + hand_str[2])


def card_str(card: Card) -> str:
    suit_dict = {0: "C", 1: "D", 2: "H", 3: "S"}
    value_dict = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}
    _str = ""
    _str += str(card.value) if card.value < 10 else value_dict[card.value]
    _str += suit_dict[card.suit]
    return _str


def hand_code(hand: list[Card]) -> str:
    _str = ""
    for card in hand:
        _str += card_str(card)
    vals = _str[0::2]
    if vals[0] == vals[1]:
        return vals
    else:
        suits = _str[1::2]
        if suits[0] == suits[1]:
            return vals + "s"
        else:
            return vals + "o"

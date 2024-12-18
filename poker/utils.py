import random
from poker.card import Card
from poker.constants import ConvDict


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
    order = ("AA, KK, QQ, AKs, JJ, AQs, KQs, AJs, KJs, ATs, QJs, AKo, TT, KTs, QTs, JTs, 99, AQo, A9s, KQo, K9s,"
             "T9s, A8s, J9s, Q9s, 88, A5s, AJo, A7s, A4s, A3s, KJo, A6s, QJo, 77, A2s, K8s, T8s, 98s, ATo, J8s,"
             "Q8s, K7s, KTo, JTo, 66, QTo, K6s, 87s, K5s, 97s, 55, T7s, K4s, 76s, 44, K3s, Q7s, J7s, 33, K2s, 22,"
             "65s, 86s, Q6s, 54s, Q5s, 75s, 96s, T9o, Q4s, T6s, A9o, Q3s, 64s, J6s, Q2s, J9o, 85s, 53s, K9o, J5s,"
             "Q9o, J4s, A8o, 74s, J3s, 43s, 95s, J2s, T5s, A5o, 63s, T4s, A7o, T8o, T3s, A4o, 52s, 98o, 84s, T2s,"
             "A3o, 42s, A6o, K8o, 94s, J8o, 73s, 93s, Q8o, 87o, A2o, 32s, 92s, 62s, K7o, 83s, 97o, 76o, 82s, T7o,"
             "K6o, 72s, 65o, 86o, K5o, 54o, J7o, K4o, Q7o, 75o, K3o, 96o, K2o, Q6o, 64o, Q5o, T6o, 53o, 85o, Q4o,"
             "J6o, Q3o, 43o, 74o, Q2o, J5o, 95o, J4o, 63o, J3o, T5o, 52o, J2o, T4o, 84o, 42o, T3o, T2o, 73o, 94o,"
             "32o, 62o, 93o, 92o, 83o, 82o, 72o")
    order = order.replace(" ", "").split(",")
    try:
        return len(order) - order.index(hand_str)
    except ValueError:
        return len(order) - order.index(hand_str[1] + hand_str[0] + hand_str[2])


def card_str(card: Card) -> str:
    _str = ''
    _str += ConvDict.RANK[card.rank]
    _str += ConvDict.SUIT_STR[card.suit]
    return _str


def hand_code(hand: list[Card]) -> str:
    _str = ''
    for card in hand:
        _str += card_str(card)
    vals = _str[0::2]
    if vals[0] == vals[1]:
        return vals
    else:
        suits = _str[1::2]
        if suits[0] == suits[1]:
            return vals + 's'
        else:
            return vals + 'o'


def find_indices_of_largest_connected_ones(arr: list[int]) -> list[int]:
    max_start = max_end = start = end = -1
    max_length = length = 0

    for i, num in enumerate(arr):
        if num == 1:
            if length == 0:
                start = i
            length += 1
            end = i
        else:
            if length > max_length:
                max_length = length
                max_start = start
                max_end = end
            length = 0

    # Final check in case the longest sequence ends at the end of the list
    if length > max_length:
        max_start = start
        max_end = end

    return list(range(max_start, max_end + 1))


def find_straight(cards: list[str]) -> list[str] | None:
    if len(cards) < 5:
        return None
    ranks = sorted(set([c[0] for c in cards]), key=lambda x: ConvDict.RANK[x], reverse=True)
    ranks_int = [ConvDict.RANK[r] for r in ranks]

    if ranks[0] == 'A':
        ranks_int.insert(len(ranks), 1)
    diffs = [ranks_int[i] - ranks_int[i + 1] for i in range(len(ranks_int) - 1)]
    straight_indices = find_indices_of_largest_connected_ones(diffs)
    if len(straight_indices) >= 4:
        if len(ranks) == len(ranks_int):
            return ranks[straight_indices[0]:straight_indices[-1] + 2]
        else:
            if ranks[straight_indices[0]] == 'A':
                return ranks[straight_indices[0]:straight_indices[-1] + 2]
            else:
                return ranks[straight_indices[0]:straight_indices[-1] + 1] + [ranks[0]]
    else:
        return None


def get_full_hand_value(full_hand: list[Card]) -> list[tuple[str, str, int]]:
    """
    :param full_hand:
    :return: List of hands. The tuple elements are the hand name, the card, and the hand value.
    """
    full_hand = [card_str(card) for card in full_hand]
    ranks = sorted(set([c[0] for c in full_hand]), key=lambda x: ConvDict.RANK[x], reverse=True)
    suits = set([c[1] for c in full_hand])
    rank_counts = {r: ''.join(full_hand).count(r) for r in ranks}
    rank_counts = dict(sorted(rank_counts.items(), key=lambda x: ConvDict.RANK[x[0]], reverse=True))
    suit_counts = {s: ''.join(full_hand).count(s) for s in suits}
    suit_counts = dict(sorted(suit_counts.items(), key=lambda x: x[1], reverse=True))
    straight_cards = find_straight(full_hand)
    if straight_cards:
        straight_cards = straight_cards[:5]

    hands = []

    if suit_counts[list(suit_counts.keys())[0]] >= 5:
        suit = list(suit_counts.keys())[0]
        suit_cards = sorted([c for c in full_hand if c[1] == suit], key=lambda x: ConvDict.RANK[x[0]])
        if straight_cards:
            if 'A' in straight_cards and 'K' in straight_cards:
                hands.append(('royal_flush', '', 1000))
            else:
                hands.append(('straight_flush', ''.join(straight_cards), ConvDict.RANK[straight_cards[0]] + 800))
        else:
            hands.append(('flush', ''.join([card[0] for card in suit_cards[::-1]]),
                          max([ConvDict.RANK[c[0]] for c in suit_cards[::-1]]) + 500))
        return hands

    if max(rank_counts.values()) == 4:
        hands.append(('four_of_a_kind', [rank for rank, count in rank_counts.items() if count == 4][0],
                      ConvDict.RANK[[rank for rank, count in rank_counts.items() if count == 4][0]] + 700))
        return hands

    if max(rank_counts.values()) == 3 and 2 in rank_counts.values():
        r3 = max([rank for rank, count in rank_counts.items() if count == 3], key=lambda x: ConvDict.RANK[x])
        r2 = max([rank for rank, count in rank_counts.items() if count == 2], key=lambda x: ConvDict.RANK[x])
        hands.append(('full_house', ''.join([r3, r2]), (ConvDict.RANK[r3] * 3 + ConvDict.RANK[r2] * 2) + 600))
        return hands

    if straight_cards:
        hands.append(('straight', ''.join(straight_cards), ConvDict.RANK[straight_cards[0]] + 400))
        return hands

    if max(rank_counts.values()) == 3 and 2 not in rank_counts.values():
        r3 = max([rank for rank, count in rank_counts.items() if count == 3], key=lambda x: ConvDict.RANK[x])
        hands.append(('three_of_a_kind', r3, ConvDict.RANK[r3] + 300))

    if max(rank_counts.values()) == 2:
        pairs = sorted([rank for rank, count in rank_counts.items() if count == 2], key=lambda x: ConvDict.RANK[x],
                       reverse=True)
        if len(pairs) >= 2:
            pairs = pairs[:2]
            hands.append(('two_pair', ''.join(pairs), ConvDict.RANK[pairs[0]] + ConvDict.RANK[pairs[1]] + 200))
        else:
            hands.append(('pair', pairs[0], ConvDict.RANK[pairs[0]] + 100))

    hands.append(('high_card', max(ranks, key=lambda x: ConvDict.RANK[x]), max([ConvDict.RANK[r] for r in ranks])))

    return hands


def find_winner_hand(contender_hands: list[list[Card]]) -> list[int]:
    values = []
    for full_hand in contender_hands:
        values.append(get_full_hand_value(full_hand)[0][2])
    indices = [i for i, v in enumerate(values) if v == max(values)]  # indices of the best hand
    if len(indices) == 1:  # if there is only one best hand
        return indices
    else:  # if there are more than one best hand
        final_contender_hands = []
        for idx in indices:
            final_contender_hands.append(contender_hands[idx])
        if len(get_full_hand_value(final_contender_hands[0])) == 1:  # if kicker does not count
            return indices
        else:  # if kicker counts
            kicker_values = []
            for full_hand in final_contender_hands:
                kicker_values.append(get_full_hand_value(full_hand)[1][2])
            # indices of the best kicker
            kicker_indices = [i for i, v in enumerate(kicker_values) if v == max(kicker_values)]
            final_indices = []
            for idx in kicker_indices:
                final_indices.append(indices[idx])
            return final_indices


if __name__ == "__main__":
    from poker.deck import Deck
    deck = Deck()
    deck.shuffle()
    hands = []
    for _ in range(5):
        hands.append(deck.deal(2))
    table = deck.deal(5)
    full_hands = []
    for hand in hands:
        full_hands.append(hand + table)
    winner = find_winner_hand(full_hands)
    for hand in hands:
        print(hand, table)
    print()
    print(f"Winner: {winner}")

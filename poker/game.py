from player import Player
from deck import Deck


betting_streets = ['pre-flop', 'flop', 'turn', 'river']


class Game:
    def __init__(self, sb: float, bb: float, pot: float = 0):
        self.sb = sb
        self.bb = bb
        self.players = []
        self.pot = pot

    def add_player(self, stack):
        self.players.append(Player(position=len(self.players), stack=stack))

    def play_round(self, dealer_position: int = 0):
        n_players = len(self.players)

        deck = Deck()
        deck.shuffle()

        if n_players > 2:
            self.players[dealer_position + 1].bet(self.sb)
            self.players[dealer_position + 2].bet(self.bb)
        else:
            self.players[dealer_position].bet(self.sb)
            self.players[dealer_position + 1].bet(self.bb)

        self.pot += self.sb
        self.pot += self.bb

        for i in range(n_players):
            position = (dealer_position + i) % n_players
            self.players[position].cards = deck.deal(2)

        # Pre-flop betting round

        community_cards = deck.deal(3)

        # Flop betting round

        community_cards.extend(deck.deal(1))

        # Turn betting round

        community_cards.extend(deck.deal(1))

        # River betting round

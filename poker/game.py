import random
from poker.player import Player


class Game:
    def __init__(self, sb: float, bb: float):
        self.sb = sb
        self.bb = bb
        self.players = []

    def add_player(self, name: str, stack: float, is_bot: bool = True, player_type: str = 'rand') -> None:
        self.players.append(Player(name=name, stack=stack, is_bot=is_bot, player_type=player_type))

    def print_players(self) -> None:
        print([player.name for player in self.players])

    def shuffle_players(self) -> None:
        random.shuffle(self.players)

    def reorder_players(self, position: int) -> None:
        self.players = self.players[position:] + self.players[:position]

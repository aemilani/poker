from poker.game import Game
from poker.deck import Deck
from poker.player import Player
from poker.utils import get_random_names


print_str_len = 18


def init_game(n_bots: int = 5) -> Game:
    game = Game(sb=1, bb=2)
    user_name = input("Enter your name: ")
    user_stack = float(input("Enter your stack amount: "))
    game.add_player(name=user_name, stack=user_stack, is_bot=False)

    bot_names = get_random_names(n_bots)
    for bot_name in bot_names:
        game.add_player(name=bot_name, stack=100)

    return game


def player_action_to_game_action(player: Player, player_action: str, current_bet: float) -> str:
    # Actions: check, fold, call, raise [amount]
    if player_action == 'check/fold':
        if current_bet == player.placed_bet:
            game_action = 'check'
        else:
            game_action = 'fold'
    elif player_action[:10] == 'call/raise':
        max_bet_amount = float(player_action.split(' ')[1])
        bet_diff = current_bet - player.placed_bet
        if bet_diff <= max_bet_amount:
            raise_amount = int(player.aggressiveness * (max_bet_amount - bet_diff))
            if raise_amount == 0:
                game_action = 'call'
            else:
                game_action = f'raise {raise_amount}'
        else:
            game_action = 'fold'
    else:
        game_action = player_action
    return game_action


def play_round(game: Game, dealer_position: int = 1):
    pot = 0
    n_players = len(game.players)

    game.reorder_players(dealer_position)
    print("\nPlayer positions:")
    game.print_players()

    deck = Deck()
    deck.shuffle()

    if n_players > 2:
        player = game.players[0]
        print(f"{player.name} (D) [{player.placed_bet}]:".rjust(print_str_len))
        player = game.players[1]
        player.bet(game.sb)
        print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "SB")
        player = game.players[2]
        player.bet(game.bb)
        print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "BB")
        bb_position = 2
    else:
        player = game.players[0]
        player.bet(game.sb)
        print(f"{player.name} (D) [{player.placed_bet}]:".rjust(print_str_len), "SB")
        player = game.players[1]
        player.bet(game.bb)
        print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "BB")
        bb_position = 1

    pot += game.sb
    pot += game.bb
    current_bet = game.bb

    for player in game.players:
        player.hand.extend(deck.deal(2))

    for player in game.players:
        if not player.is_bot:
            print(f"\n{player.name}'s hand:")
            print(player.hand)
            print()

    n_folded = 0

    # Pre-flop betting round
    pos = (bb_position + 1) % n_players
    while True:
        player = game.players[pos]
        if player.action and current_bet == player.placed_bet:
            break
        if player.action == 'out':
            pos += 1
            pos = pos % n_players
            continue
        if player.is_bot:
            player_action = player.act()
        else:
            player_action = input(
                f"{player.name} [{player.placed_bet}] Enter your action [check/fold, call, raise [amount]]: ")

        game_action = player_action_to_game_action(player, player_action, current_bet)
        player.action = game_action

        if player.action == 'call':
            bet_amount = current_bet - player.placed_bet
            player.bet(bet_amount)
            pot += bet_amount
            print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "Call")
        elif player.action[:5] == 'raise':
            raise_amount = int(game_action.split(' ')[1])
            bet_amount = current_bet - player.placed_bet + raise_amount
            player.bet(bet_amount)
            pot += bet_amount
            current_bet += raise_amount
            print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), f"Raise to {current_bet}")
        else:
            print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), f"{game_action.capitalize()}")

        if player.action == 'fold':
            player.action = 'out'
            n_folded += 1

        if n_folded == (n_players - 1):
            winner = [p for p in game.players if p.action != 'out'][0]
            winner.win(pot)
            print(f"{winner.name} wins!")
            losers = [p for p in game.players if p.action == 'out']
            for p in losers:
                p.lose()
            return

        pos += 1
        pos = pos % n_players

    # Flop betting round
    table_cards = deck.deal(3)
    print("\nTable cards:")
    print(table_cards)
    for player in game.players:
        player.table.extend(table_cards)

    pos = 1  # BB

    # Post-flop betting round
    for _ in range(2):
        table_cards.extend(deck.deal(1))
        print("\nTable cards:")
        print(table_cards)


if __name__ == "__main__":
    game = init_game(n_bots=5)
    game.shuffle_players()
    play_round(game=game, dealer_position=1)

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
        if bet_diff < max_bet_amount:
            bet_amount = bet_diff + player.aggressiveness * (max_bet_amount - bet_diff)
            game_action = f'raise {bet_amount}'
        else:
            game_action = 'call'
    else:
        game_action = 'fold'
    return game_action


def play_round(game: Game, dealer_position: int = 0):
    pot = 0
    pot_participants = []
    n_players = len(game.players)

    deck = Deck()
    deck.shuffle()

    if n_players > 2:
        player = game.players[dealer_position]
        print(f"{player.name} (D) [{player.placed_bet}]:".rjust(print_str_len))
        player = game.players[dealer_position + 1]
        player.bet(game.sb)
        print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "SB")
        player = game.players[dealer_position + 2]
        player.bet(game.bb)
        print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "BB")
        last_bet_position = dealer_position + 2
    else:
        player = game.players[dealer_position]
        player.bet(game.sb)
        print(f"{player.name} (D) [{player.placed_bet}]:".rjust(print_str_len), "SB")
        player = game.players[dealer_position + 1]
        player.bet(game.bb)
        print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "BB")
        last_bet_position = dealer_position + 1

    pot += game.sb
    pot += game.bb
    current_bet = game.bb

    game.reorder_players(dealer_position)
    for player in game.players:
        player.hand.extend(deck.deal(2))

    # Pre-flop betting round
    game.reorder_players(last_bet_position + 1)
    for i, player in enumerate(game.players):
        if player.is_bot:
            player_action = player.act()
        else:
            print("\nYour hand:")
            print(player.hand)
            player_action = input(
                f"{player.name} [{player.placed_bet}] Enter your action [check/fold, call, raise [amount]]: ")

        game_action = player_action_to_game_action(player, player_action, current_bet)

        if game_action != 'fold':
            pot_participants.append(player)

        if game_action == 'call':
            bet_amount = current_bet - player.placed_bet
            player.bet(bet_amount)
            pot += bet_amount
            print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), "Call")
            last_bet_position = i
        elif game_action[:5] == 'raise':
            bet_amount = current_bet - player.placed_bet + round(float(game_action.split(' ')[1]), 2)
            player.bet(bet_amount)
            pot += bet_amount
            print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), f"Raise to {bet_amount}")
            last_bet_position = i
        else:
            print(f"{player.name} [{player.placed_bet}]:".rjust(print_str_len), f"{game_action.capitalize()}")

    # Flop betting round
    table_cards = deck.deal(3)
    print("\nTable cards:")
    print(table_cards)

    game.reorder_players(last_bet_position)

    # Post-flop betting round
    for _ in range(2):
        table_cards.extend(deck.deal(1))
        print("\nCommunity cards:")
        print(table_cards)

        game.reorder_players(last_bet_position)


if __name__ == "__main__":
    game = init_game(n_bots=5)
    game.shuffle_players()
    print("\nPlayer positions:")
    game.print_players()

    play_round(game=game, dealer_position=0)

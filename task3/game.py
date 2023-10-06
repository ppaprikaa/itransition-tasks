from random_number_generator import Generator as RandomGenerator
from hmac_generator import Generator as HMACGenerator
from strategies import InvalidStrategyNumberException, RepeatingStrategyException, Strategies, Strategy
from table import Table
from rules import GameResult, Rules, UndeclaredStrategyException
from typing import List
import messages


class NonTransitiveGame:
    def __init__(self, strats: List[str]) -> None:
        self._random_generator: RandomGenerator = RandomGenerator()
        self._hmac_generator: HMACGenerator = HMACGenerator(self._random_generator)
        self._strategies: Strategies = Strategies(strats)
        self._menu: str = messages.moves.format(moves=self._strategies.to_string())
        self._rules: Rules = Rules(self._strategies)
        self._table: Table = Table(self._rules, self._strategies)
    

    def _run(self) -> None:
        self._start_game_loop()


    def try_run(self) -> None:
        try:
            self._run()
        except UndeclaredStrategyException:
            print(messages.on_undeclared_strategy)


    def _start_game_loop(self) -> None:
        while True:
            strat_ids = [strat.get_id() for strat in self._strategies.to_list()]
            strat_names = [strat.get_name() for strat in self._strategies.to_list()]

            secret = self._hmac_generator.generate_secret()
            computer_strat_id = self._random_generator.generate_int_in_range(1, len(self._strategies.to_list()))
            computer_strat = self._strategies.get_by_id(computer_strat_id)
            computer_hmac = self._hmac_generator.generate_sha256(computer_strat.get_name(), secret)

            print(messages.hmac.format(computer_hmac))
            print(self._menu)
            while True:
                move = input(messages.read_move)
                match move:
                    case move if move.strip() in ["exit", "0"]:
                        exit(0)
                    case move if move.strip() in ["help", "?"]:
                        print(self._table.to_string())
                    case move if move.strip() in strat_names:
                        player_strat = self._strategies.get_by_name(move.strip())
                        self._play(player_strat, computer_strat)
                        break
                    case move if try_str_to_int(move) in strat_ids and is_int(move):
                        player_strat = self._strategies.get_by_id(int(move.strip()))
                        self._play(player_strat, computer_strat)
                        break
                    case _:
                        print(self._menu)
                        print("Please choose one of the commands")

            print(messages.hmac_key.format(secret))
            input("Press 'Enter' to continue...")
            print()


    def _play(self, player_strat: Strategy, computer_strat: Strategy) -> None:
        print(messages.your_move.format(player_strat.get_name()))
        print(messages.computer_move.format(computer_strat.get_name()))
        result = self._rules.get_result(player_strat, computer_strat)
        match result:
            case GameResult.Win: 
                print(messages.on_win)
            case GameResult.Lose:
                print(messages.on_lose)
            case GameResult.Draw:
                print(messages.on_draw)


def try_init_game(args) -> NonTransitiveGame | None:
    try:
        return NonTransitiveGame(args)
    except InvalidStrategyNumberException:
        print(messages.on_invalid_number_of_strategies)
    except RepeatingStrategyException:
        print(messages.on_repeating_strategies)


def is_int(s: str) -> bool:
    try:
        int(s.strip())
    except ValueError:
        return False
    else:
        return True


def try_str_to_int(s: str) -> int:
    try:
        res = int(s.strip())
    except (ValueError, TypeError):
        return -1
    else:
        return res

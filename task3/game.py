from random_number_generator import Generator as RandomGenerator
from hmac_generator import Generator as HMACGenerator
from strategies import InvalidStrategyNumberException, RepeatingStrategyException, Strategies
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
            print(messages.hmac_key.format(secret))
            print(self._menu)
            while True:
                move = input(messages.read_move)
                match move:
                    case move if move.strip() in ["exit", "0"]:
                        exit(0)
                    case move if move.strip() in ["help", "?"]:
                        print(self._table.to_string())
                    case move if move.strip() in strat_names:
                        self._play(secret, move.strip())
                        break
                    case move if try_str_to_int(move) in strat_ids and is_int(move):
                        self._play(secret, self._strategies.get_by_id(int(move.strip())).get_name())
                        break
                    case _:
                        print(self._menu)
                        print("Please choose one of the commands")

            input("Press 'Enter' to continue...")
            print()


    def _play(self, secret: str, your_strat_name: str) -> None:
        your_strat = self._strategies.get_by_name(your_strat_name)

        computerMoveID = self._random_generator.generate_int_in_range(1, len(self._strategies.to_list()))
        computerStrat = self._strategies.get_by_id(computerMoveID)
        result_hmac = self._hmac_generator.generate_sha256(computerStrat.get_name(), secret)
        print(messages.your_move.format(your_strat.get_name()))
        print(messages.computer_move.format(computerStrat.get_name()))
        result = self._rules.get_result(your_strat, computerStrat)
        match result:
            case GameResult.Win: 
                print(messages.on_win)
            case GameResult.Lose:
                print(messages.on_lose)
            case GameResult.Draw:
                print(messages.on_draw)
        print(messages.hmac.format(result_hmac))


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

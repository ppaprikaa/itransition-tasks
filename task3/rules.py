from __future__ import annotations

from strategies import Strategies, Strategy
from enum import Enum
from typing import Dict

class UndeclaredStrategyException(Exception):
    pass

class GameResult(Enum):
    Lose = 0
    Draw = 1
    Win  = 2

    def reverse(self) -> GameResult:
        if self == GameResult.Lose: return GameResult.Win

        if self == GameResult.Win: return GameResult.Lose
        return GameResult.Draw


    def to_string(self) -> str:
        if self == GameResult.Lose: 
            return "LOSE"
        if self == GameResult.Win: 
            return "WIN"
        return "DRAW"
        

class Rules:
    def __init__(self, strategies: Strategies) -> None:
        self._strategies: Strategies = strategies
        self._half_circle_distance: int = int(len(self._strategies) / 2) if (len(self._strategies) % 2 == 0) else int((len(self._strategies) / 2) + 1)
        self._table: Dict[str, Dict[str, GameResult]] = {}


    def get_result(self, strat1: Strategy, strat2: Strategy) -> GameResult:
        if not self._strategies.get_by_name(strat1.get_name()) \
        or not self._strategies.get_by_name(strat1.get_name()):
            raise UndeclaredStrategyException
        diff = abs(strat1.get_id() - strat2.get_id())  
        if diff == 0:
            return GameResult.Draw
        
        move1 = strat1.get_id()
        move2 = strat2.get_id()
        if diff < self._half_circle_distance:
            if move1 < move2:
                return GameResult.Lose
            return GameResult.Win 
         
        # if diff >= _half_circle_distance
        if move1 < move2:
            return GameResult.Win
        return GameResult.Lose

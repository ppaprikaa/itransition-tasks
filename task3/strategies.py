from typing import Dict, List

class RepeatingStrategyException(Exception):
    pass

class InvalidStrategyNumberException(Exception):
    pass

class Strategy:
    def __init__(self, name: str, id: int) -> None:
        self._name: str = name
        self._id: int = id

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name


class Strategies:
    def __init__(self, stratNames: List[str]):
        if len(stratNames) % 2 == 0 or len(stratNames) < 3:
           raise InvalidStrategyNumberException 
        strats_by_name: Dict[str, Strategy] = {}
        strats_by_id: List[Strategy] = []
        gentag = 1
        for stratName in stratNames:
            if stratName in strats_by_name.keys():
                raise RepeatingStrategyException
            strat = Strategy(stratName, gentag)
            strats_by_name[stratName] = strat
            strats_by_id.append(strat)
            gentag += 1
        self._strats_by_name= strats_by_name
        self._strats_by_id = strats_by_id
        self._index = 0
        self._string = ""

    

    def get_by_id(self, id: int) -> Strategy:
        return self._strats_by_id[id - 1]


    def get_by_idx(self, idx: int) -> Strategy:
        return self._strats_by_id[idx]


    def get_by_name(self, name: str) -> Strategy:
        return self._strats_by_name[name]


    def to_string(self):
        if (len(self._string.strip()) == 0 and len(self._strats_by_id) != 0):
            for strat in self._strats_by_id:
                self._string += "{} - {}\n".format(
                        strat.get_id(), 
                        strat.get_name()
                )
            return self._string
        return self._string


    def to_list(self) -> List[Strategy]:
        return self._strats_by_id


    def to_dict(self) -> Dict[str, Strategy]:
        return self._strats_by_name


    def __iter__(self):
        return StrategiesIter(self)


    def __len__(self):
        return len(self._strats_by_id)


class StrategiesIter:
    def __init__(self, strategies: Strategies):
        self._strategies = strategies
        self._i = 0


    def __next__(self):
        if self._i >= len(self._strategies):
            raise StopIteration
        next_item = self._strategies.get_by_idx(self._i)
        self._i += 1
        return next_item

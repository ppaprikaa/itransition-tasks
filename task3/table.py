from rules import Rules
from strategies import Strategies
from tabulate import tabulate
from typing import List

class Table:
    def __init__(self, rules: Rules, strategies: Strategies):
        self._rules: Rules = rules
        self._strategies: Strategies = strategies


    def to_string(self) -> str:
        headers = ['PC|PLAYER', *[strat.get_name() for strat in self._strategies]]
        strat_list = self._strategies.to_list() 
        resultTable: List[List[str]] = [] 
        rowIndex = 0
        for first_strat in strat_list:
            resultTable.insert(rowIndex, [first_strat.get_name()]) 
            for second_strat in strat_list:
                # get result method has to accept swapped first strat and second, because get_result calculates
                # if first player loses to the second, so we have to swap them in order to figure out if first player wins or loses
                resultTable[rowIndex].append(self._rules.get_result(first_strat, second_strat).reverse().to_string())
            rowIndex += 1
        return tabulate(resultTable, headers)

import random
from time import time

class Generator:
    def __init__(self):
        random.seed(time())

    def generate(self) -> int:
        res = random.random() * 10**3
        return int(res)
        
    def generate_int_in_range(self, start: int, end: int):
        return random.randint(start, end)

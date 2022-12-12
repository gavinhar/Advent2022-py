from functools import reduce
from typing import List, Dict


class Monkey:
    def __init__(self, id: int, items: List[int], op: str, test: int, if_t: int, if_f: int):
        self.id: int = id
        self.items: List[int] = items
        self.op: str = op
        self.test: int = test
        self.if_t: int = if_t
        self.if_f: int = if_f


f = open('../input/day11.txt').readlines()

monkeys: Dict[int, Monkey] = {}
for i in range(0, len(f), 7):
    chunk = f[i:i+6]

    id = int(chunk[0][7])
    items = list(map(int, chunk[1][18:].strip().split(', ')))
    op = chunk[2][19:].strip()
    test = int(chunk[3][21:])
    if_t = int(chunk[4][29:])
    if_f = int(chunk[5][30:])
    monkeys[id] = Monkey(id, items, op, test, if_t, if_f)

monkey_business = [0] * len(monkeys)
modulus = reduce(lambda a, m: a * monkeys[m].test, monkeys.keys(), 1)


def calc_worry(item: int, op: str):
    tokens = op.split(' ')
    a = item if tokens[0] == 'old' else int(tokens[0])
    b = item if tokens[2] == 'old' else int(tokens[2])
    if tokens[1] == '+':
        return (a + b) % modulus  # // 3
    return (a * b) % modulus  # // 3


for i in range(10000):
    for j in range(len(monkeys)):
        monkey = monkeys[j]
        monkey_business[j] += len(monkey.items)

        while len(monkey.items) > 0:
            item = monkey.items.pop(0)
            worry = calc_worry(item, monkey.op)
            idx = monkey.if_t if worry % monkey.test == 0 else monkey.if_f
            monkeys[idx].items.append(worry)

monkey_business.sort(reverse=True)
result = monkey_business[0] * monkey_business[1]

print(result)

from typing import IO, Tuple


class Expr:
    """
    a * x + b
    """
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def __sub__(self, other):
        return Expr(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        assert self.a == 0 or other.a == 0
        return Expr(self.a * other.b + self.b * other.a, self.b * other.b)

    def __invert__(self):
        new_a = 1.0 / self.a if self.a != 0 else 0
        new_b = 1.0 / self.b if self.b != 0 else 0
        return Expr(new_a, new_b)

    def __add__(self, other):
        return Expr(self.a + other.a, self.b + other.b)


class Monkey:
    def __init__(self, monkeys=None, value=None, op=None, params=None):
        self.monkeys = monkeys
        self.value = Expr(0, value) if value is not None else None
        self.op = op
        self.params = params

    def eval(self):
        if self.value is not None:
            return self.value

        a = self.monkeys[self.params[0]].eval()
        b = self.monkeys[self.params[1]].eval()
        if self.op == '+':
            return a + b
        elif self.op == '-':
            return a - b
        elif self.op == '*':
            return a * b
        elif self.op == '/':
            return a * (~b)
        else:
            raise Exception


def solution(f: IO) -> Tuple[int, int]:
    monkeys = {}
    for line1 in f:
        line = line1.strip().split(' ')
        name = line[0][:-1]
        if len(line) == 2:
            monkeys[name] = Monkey(value=int(line[1]))
        else:
            monkeys[name] = Monkey(monkeys=monkeys, op=line[2], params=[line[1], line[3]])
    rv1 = int(monkeys['root'].eval().b)

    monkeys['humn'].value = Expr(1, 0)
    a = monkeys[monkeys['root'].params[0]].eval()
    b = monkeys[monkeys['root'].params[1]].eval()
    if a.a == 0:
        a, b = b, a
    return rv1, int((b.b - a.b) / a.a)


def solve_sample():
    with open('../sample/day21.txt') as f:
        part1, part2 = solution(f)
        assert part1 == 152
        assert part2 == 301


def solve():
    with open('../input/day21.txt') as f:
        print(solution(f))


solve_sample()
solve()

import functools
from typing import IO, Optional, List, Union

def parse(l: str) -> List:
    line = l[1:len(l)-1]
    curr = []
    rv = curr
    prev = []
    num = ''

    for c in line:
        if c == '[':
            prev.append(curr)
            curr = []
            prev[-1].append(curr)
        elif c == ']':
            if len(num) > 0:
                curr.append(int(num))
                num = ''
            curr = prev.pop()
        elif c == ',':
            if len(num) > 0:
                curr.append(int(num))
                num = ''
        else:
            num = num + c
    if len(num) > 0:
        curr.append(int(num))
    return rv


def is_list(v):
    return isinstance(v, list)


def is_sorted(a, b):
    if is_list(a) and not is_list(b):
        b = [b]
    elif is_list(b) and not is_list(a):
        a = [a]
    elif not is_list(a) and not is_list(b):
        if a == b:
            return None
        return a < b

    for i in range(min(len(a), len(b))):
        v_sorted = is_sorted(a[i], b[i])
        if v_sorted is not None:
            return v_sorted

    if len(a) == len(b):
        return None
    return len(a) < len(b)


def sort(packets):
    while True:
        ordered = True
        for i in range(1, len(packets)):
            if not is_sorted(packets[i-1], packets[i]):
                ordered = False
                packets[i-1], packets[i] = packets[i], packets[i-1]
        if ordered:
            return


def solution(f: IO) -> int:
    total = 0
    idx = 1
    packets = [[[2]], [[6]]]

    while True:
        a = parse(f.readline().strip())
        b = parse(f.readline().strip())
        packets.extend([a, b])

        if is_sorted(a, b):
            total += idx
        idx += 1

        if f.readline() == '':
            sort(packets)
            return total, (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


with open('../input/day13-sample.txt') as f:
    part1, part2 = solution(f)
    assert part1 == 13
    assert part2 == 140
    print(part1)
    print(part2)
    print()


with open('../input/day13.txt') as f:
    part1, part2 = solution(f)
    print(part1)
    print(part2)

from typing import IO, Tuple


def maxes(lines):
    x, y = 0, 0
    for line in lines:
        for point in line:
            x, y = max(x, point[0]), max(y, point[1])
    return x, y


def print_chart(chart):
    cs = ' #o'
    for line in chart:
        print(''.join([cs[i] for i in line]))


def drop_sand(chart):
    x, y = 500, 0
    while True:
        if len(chart) == y + 1:
            return False
        if chart[y + 1][x] == 0:
            y += 1
        elif chart[y + 1][x - 1] == 0:
            y += 1
            x -= 1
        elif chart[y + 1][x + 1] == 0:
            y += 1
            x += 1
        else:
            chart[y][x] = 2
            return True


def drop_sand2(chart):
    x, y = 500, 0
    while True:
        if len(chart) == y + 1:
            raise Exception
        if chart[y + 1][x] == 0:
            y += 1
        elif chart[y + 1][x - 1] == 0:
            y += 1
            x -= 1
        elif chart[y + 1][x + 1] == 0:
            y += 1
            x += 1
        else:
            chart[y][x] = 2
            if x == 500 and y == 0:
                return False
            return True


def count(chart):
    total = 0
    for line in chart:
        for c in line:
            if c == 2:
                total += 1
    return total


def solution(f: IO) -> Tuple[int, int]:
    lines = [[[int(y) for y in x.split(',')] for x in line] for line in
             [x.strip().split(' -> ') for x in f.readlines()]]
    max_x, max_y = maxes(lines)
    chart = [[0] * (max_x + 1) for i in range(max_y + 1)]

    for line in lines:
        for i in range(1, len(line)):
            a = line[i - 1]
            b = line[i]

            if a[0] == b[0]:
                for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                    chart[y][a[0]] = 1
            else:
                for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                    chart[a[1]][x] = 1

    chart2 = []
    for j in range(len(chart)):
        chart2.append([])
        for i in range(len(chart[j])):
            chart2[j].append(chart[j][i])
        chart2[j].extend([0] * 500)

    chart2.append([0] * len(chart2[0]))
    chart2.append([1] * len(chart2[0]))

    i = 0
    while drop_sand(chart):
        i += 1

    while drop_sand2(chart2):
        pass

    return i, count(chart2)


with open('../sample/day14.txt') as f:
    part1, part2 = solution(f)
    assert part1 == 24
    assert part2 == 93

with open('../input/day14.txt') as f:
    print(solution(f))

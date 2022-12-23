from typing import IO, Tuple, Dict


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def part1_search(beacons, max_d, max_x, min_x, sensors, y):
    empty = 0
    for x in range(min_x - max_d - 10, max_x + max_d + 10):
        if (x, y) in sensors or (x, y) in beacons:
            continue

        for s in sensors.keys():
            if distance(s[0], s[1], x, y) <= sensors[s]:
                empty += 1
                break
    return empty


def is_covered(sensors, c):
    for s in sensors:
        if distance(s[0], s[1], c[0], c[1]) <= sensors[s]:
            return True
    return False


def part2_search(sensors: Dict[Tuple[int, int], int], m):
    for s in sensors:
        d = sensors[s]
        for delta_x in range(-d - 1, d + 2):
            delta_y = (d - abs(delta_x) + 1)
            c1 = (s[0] + delta_x, s[1] - delta_y)
            c2 = (s[0] + delta_x, s[1] + delta_y)
            if 0 <= c1[0] <= m and 0 <= c1[1] <= m and not is_covered(sensors, c1):
                return c1[0] * 4000000 + c1[1]
            if 0 <= c2[0] <= m and 0 <= c2[1] <= m and not is_covered(sensors, c2):
                return c2[0] * 4000000 + c2[1]


def solution(f: IO, y: int, m: int) -> Tuple[int, int]:
    sensors = {}
    beacons = set()
    min_x, max_x, max_d = 0, 0, 0
    for line in f:
        tokens = line.strip().split(' ')
        x1 = int(tokens[2][2:-1])
        y1 = int(tokens[3][2:-1])
        x2 = int(tokens[8][2:-1])
        y2 = int(tokens[9][2:])
        dist = distance(x1, y1, x2, y2)
        min_x = min(min_x, x1)
        max_x = max(max_x, x1)
        max_d = max(max_d, dist)
        sensors[(x1, y1)] = dist
        beacons.add((x2, y2))

        print((x1, y1), dist)

    empty = part1_search(beacons, max_d, max_x, min_x, sensors, y)
    part2 = part2_search(sensors, m)
    return empty, part2


with open('../input/day15-sample.txt') as f:
    part1, part2 = solution(f, 10, 20)
    assert part1 == 26
    assert part2 == 56000011
    print(part1, part2)

with open('../input/day15.txt') as f:
    print(solution(f, 2000000, 4000000))

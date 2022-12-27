from typing import IO, Tuple, List, Set

Point = Tuple[int, int, int]


def adjacent(point: Point) -> List[Point]:
    return [
        (point[0] - 1, point[1], point[2]),
        (point[0] + 1, point[1], point[2]),
        (point[0], point[1] - 1, point[2]),
        (point[0], point[1] + 1, point[2]),
        (point[0], point[1], point[2] - 1),
        (point[0], point[1], point[2] + 1),
    ]



def solution(f: IO) -> Tuple[int, int]:
    cubes: Set[Tuple[int, int, int]] = set([tuple(map(int, line.strip().split(','))) for line in f.readlines()])
    print(cubes)

    # part 1
    total = 0
    for c in cubes:
        for a in adjacent(c):
            if a not in cubes:
                total += 1

    mins = (1000, 1000, 1000)
    maxes = (0, 0, 0)
    for c in cubes:
        mins = (min(mins[0], c[0]), min(mins[1], c[1]), min(mins[2], c[2]))
        maxes = (max(maxes[0], c[0]), max(maxes[1], c[1]), max(maxes[2], c[2]))
    print(mins)
    print(maxes)

    # min/max index for outside air
    # turns out their all the same in sample and my input
    min_idx = mins[0] - 5
    max_idx = maxes[0] + 5

    todo = [(min_idx, min_idx, min_idx)]
    visited = {(min_idx, min_idx, min_idx)}
    while len(todo) > 0:
        curr = todo.pop()
        visited.add(curr)
        for adj in adjacent(curr):
            if adj not in visited \
                    and adj not in cubes \
                    and min_idx <= adj[0] <= max_idx \
                    and min_idx <= adj[1] <= max_idx \
                    and min_idx <= adj[2] <= max_idx:
                todo.append(adj)
                visited.add(adj)

    # visited should contain all outside air
    total2 = 0
    for c in cubes:
        for a in adjacent(c):
            if a in visited:
                total2 += 1

    return total, total2


with open('../sample/day18.txt') as f:
    part1, part2 = solution(f)
    assert part1 == 64
    assert part2 == 58
    print('\n')


with open('../input/day18.txt') as f:
    part1, part2 = solution(f)
    print('part 1:', part1)
    print('part 2:', part2)

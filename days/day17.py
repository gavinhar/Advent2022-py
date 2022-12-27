from itertools import permutations
from typing import List, Tuple, IO, Dict, Iterable, Optional

shapes: List[List[List[int]]] = [
    [
        [1, 1, 1, 1],
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ],
    [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    [
        [1],
        [1],
        [1],
        [1],
    ],
    [
        [1, 1],
        [1, 1],
    ]
]


def print_pit(
        pit: List[List[int]],
        shape: Optional[List[List[int]]] = None,
        pos: Optional[Tuple[int, int]] = None
) -> None:
    for y in range(len(pit) - 1, -1, -1):
        print(''.join(['#' if p == 1 else '.' for p in pit[y]]))
    print()
    print()


def find_floor(
        pit: List[List[int]]
) -> int:
    ps = [1, 2, 3, 4, 5, 6, 7]
    for i in range(len(pit) - 1, -1, -1):
        new_ps = set()
        for p in ps:
            if pit[i][p - 1] == 0 and pit[i - 1][p - 1] == 0:
                new_ps.add(p - 1)
            if pit[i - 1][p] == 0:
                new_ps.add(p)
            if pit[i][p + 1] == 0 and pit[i - 1][p + 1] == 0:
                new_ps.add(p + 1)
        if len(new_ps) == 0:
            assert i > 0
            for j in range(len(pit[i-1])):
                pit[i-1][j] = 1
            return i - 1
        else:
            ps = list(new_ps)
    return 0


def check_move(
        pit: List[List[int]],
        shape: List[List[int]],
        pos: Tuple[int, int],
        direction: Tuple[int, int]
) -> bool:
    new_pos = pos[0] + direction[0], pos[1] + direction[1]
    for i in range(len(shape[0])):
        for j in range(len(shape)):
            x = new_pos[0] + i
            y = new_pos[1] - j
            if pit[y][x] + shape[j][i] > 1:
                return False
    return True


def solution(f: IO, num_iters: int) -> int:
    # pit[0] = floor
    pit: List[List[int]] = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
    ]

    moves = f.readline().strip()

    floor_idx = 0
    height = 0
    move_idx = 0
    iteration = 0
    while iteration <= num_iters:
        iteration += 1
        PRINT_EVERY_N = 10_000
        if iteration % PRINT_EVERY_N == 0:
            print(f'{iteration // PRINT_EVERY_N} / {num_iters // PRINT_EVERY_N} = {iteration * 100.0 / num_iters}')
        shape_idx = iteration % len(shapes)
        shape: List[List[int]] = shapes[shape_idx]
        shape_height = len(shape)

        pos = 3, height + 3 + shape_height
        while pos[1] >= len(pit):
            pit.append([1, 0, 0, 0, 0, 0, 0, 0, 1])

        # size of pit doesn't need to be optimal
        # it's faster to run gc when it's likely floor has moved
        # rather than every iteration
        if iteration % 1_000 == 0:
            new_floor = find_floor(pit)
            if new_floor > 0:
                pit = pit[new_floor:]
                floor_idx += new_floor
                height -= new_floor
                pos = (pos[0], pos[1] - new_floor)

        falling = True
        while falling:
            direction = -1 if moves[move_idx] == '<' else 1
            move_idx = (move_idx + 1) % len(moves)

            if check_move(pit, shape, pos, (direction, 0)):
                pos = (pos[0] + direction, pos[1])
            else:
                pass
            falling = check_move(pit, shape, pos, (0, -1))
            if falling:
                pos = (pos[0], pos[1] - 1)
            else:
                for i in range(len(shape[0])):
                    for j in range(len(shape)):
                        x = pos[0] + i
                        y = pos[1] - j
                        pit[y][x] = pit[y][x] + shape[j][i]
                        height = max(height, pos[1])
    return height + floor_idx


# with open('../sample/day17.txt') as f:
#     part1 = solution(f, 2022)
#     assert 3068 == part1
#
with open('../sample/day17.txt') as f:
    part2 = solution(f, 1000000000000)
    print('sample part2', part2, 1514285714288 - part2)
    print('\n\n')
#    assert 1514285714288 == part2
#
# with open('../input/day17.txt') as f:
#     part1 = solution(f, 2022)
#     print('part1', part1)

with open('../input/day17.txt') as f:
    part2 = solution(f, 1000000000000)
    print('part2', part2)

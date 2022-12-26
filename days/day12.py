from typing import IO, Tuple, List, Optional


def read_input(input: IO, part2: bool) -> Tuple[List[List[int]], List[Tuple[int, int]], Tuple[int, int]]:
    grid = []
    start, end = [], None
    row, col = 0, 0
    for line in input:
        grid.append([])
        col = 0
        for c in line.strip():
            if c == 'S' or (part2 and c == 'a'):
                grid[row].append(0)
                start.append((row + 1, col + 1))
            elif c == 'E':
                grid[row].append(25)
                end = (row + 1, col + 1)
            else:
                grid[row].append(int(c, 36) - int('a', 36))
            col += 1
        row += 1

    # pad the grid to make search logic simpler
    dim = (len(grid), len(grid[0]))
    for i in range(dim[0]):
        grid[i].insert(0, 100)
        grid[i].append(100)
    grid.insert(0, [100] * (2 + dim[1]))
    grid.append([100] * (2 + dim[1]))

    return grid, start, end


def solution(input: IO, part2: bool):
    grid, start, end = read_input(input, part2)

    visited = set()
    todo = list(map(lambda s: (s, 0), start))

    while True:
        curr, steps = todo.pop(0)

        if curr == end:
            return steps

        if curr in visited:
            continue

        visited.add(curr)
        x, y = curr
        curr_alt = grid[x][y]
        if grid[x - 1][y] <= curr_alt + 1:
            todo.append(((x - 1, y), steps + 1))
        if grid[x + 1][y] <= curr_alt + 1:
            todo.append(((x + 1, y), steps + 1))
        if grid[x][y - 1] <= curr_alt + 1:
            todo.append(((x, y - 1), steps + 1))
        if grid[x][y + 1] <= curr_alt + 1:
            todo.append(((x, y + 1), steps + 1))


with open('../sample/day12.txt') as f:
    print(solution(f, False))

with open('../sample/day12.txt') as f:
    print(solution(f, True))

with open('../input/day12.txt') as f:
    print(solution(f, False))

with open('../input/day12.txt') as f:
    print(solution(f, True))

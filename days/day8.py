from functools import reduce


def is_visible(lst, value):
    if len(lst) == 0:
        return True
    return max(lst) < value


def visible_trees(lst, value):
    blockers = list(filter(lambda x: x >= value, lst))
    if (len(blockers)) == 0:
        return len(lst)
    return lst.index(blockers[0]) + 1


with open('../input/day8.txt') as f:
    grid = [[int(x) for x in line.strip()] for line in f.readlines()]

count = 0
scenic_score = 0
for r in range(0, len(grid)):
    for c in range(0, len(grid[0])):
        # the current tree
        v = grid[r][c]

        # the trees in all directions from the current tree, sorted by closest to furthest
        directions = [
            list(reversed(grid[r][0:c])),  # left
            grid[r][c + 1:],  # right
            [row[c] for row in reversed(grid[0:r])],  # up
            [row[c] for row in grid[r + 1:]],  # down
        ]

        # calculate part 1 answer
        count += 1 if reduce(lambda a, b: a or is_visible(b, v), directions, False) else 0

        # calculate part 2 answer
        scenic_score = max(scenic_score, reduce(lambda a, b: a * visible_trees(b, v), directions, 1))

# print part 1 answer
print(count)

# print part 2 answer
print(scenic_score)

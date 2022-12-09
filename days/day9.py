delta = {
    'L': [-1, 0],
    'R': [1, 0],
    'U': [0, 1],
    'D': [0, -1]
}

# [(direction, #), ...]
f = [(item[0], int(item[1])) for item in [line.strip().split(' ') for line in open('../input/day9.txt')]]


def follow(head, tail):
    r_d, c_d = head[0] - tail[0], head[1] - tail[1]
    if max(abs(r_d), abs(c_d)) == 2:
        tail[0] += r_d if abs(r_d) == 1 else (r_d / 2)
        tail[1] += c_d if abs(c_d) == 1 else (c_d / 2)


# row, col
rope = [[0, 0] for i in range(0, 10)]
part1_visited = {(0, 0)}
part2_visited = {(0, 0)}
for line in f:
    d = delta[line[0]]
    for i in range(line[1]):
        rope[0][0:1] = rope[0][0] + d[0], rope[0][1] + d[1]
        for j in range(1, 10):
            follow(rope[j-1], rope[j])
        part1_visited.add(tuple(rope[1]))
        part2_visited.add(tuple(rope[9]))

print(len(part1_visited))
print(len(part2_visited))

# init stacks 1-9
stacks = dict()
for i in range(1, 10):
    stacks[i] = []

with open('../input/day5.txt') as f:
    # read stacks
    for i in range(1, 9):
        line = f.readline()
        for j in range(0, 9):
            c = line[1 + j * 4]
            if c != ' ':
                stacks[j + 1].append(c)

    # skip
    f.readline()
    f.readline()

    # do moves
    moves = map(lambda x: x.strip().split(' '), f.readlines())
    for move in moves:
        n, src, dst = int(move[1]), int(move[3]), int(move[5])

        crates = stacks[src][0:n]
        for i in range(n):
            stacks[src].pop(0)
            stacks[dst].insert(0, crates[n - i - 1])

print(''.join(map(lambda x: stacks[x][0], range(1, 10))))

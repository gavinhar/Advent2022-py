# A = Rock
# B = Paper
# C = Scissors

# X = Lose
# Y = Draw
# Z = Win

f = list(map(lambda x: x.strip().split(' '), open('../input/day2.txt').readlines()))

score = 0
for line in f:
    if line[0] == 'A':
        if line[1] == 'X':  # scissors = 3
            score += 3
        elif line[1] == 'Y':  # rock = 1
            score += 1
        else:
            score += 2
    elif line[0] == 'B':
        if line[1] == 'X':
            score += 1
        elif line[1] == 'Y':
            score += 2
        else:
            score += 3
    else:
        if line[1] == 'X':
            score += 2
        elif line[1] == 'Y':
            score += 3
        else:
            score += 1
    if line[1] == 'X':
        score += 0
    elif line[1] == 'Y':
        score += 3
    elif line[1] == 'Z':
        score += 6

print(score)

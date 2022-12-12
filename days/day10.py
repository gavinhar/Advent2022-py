from functools import reduce

# calculate value of x during each cycle
x = 1
xs = []
for line in open('../input/day10.txt'):
    xs.append(x)
    if line.strip() != 'noop':
        xs.append(x)
        x += int(line.strip().split(' ')[1])

# part 1
indexes = [20, 60, 100, 140, 180, 220]
print(reduce(lambda a, c: a + xs[c - 1] * c, indexes, 0))

# part 2
pixels = list(map(lambda idx: '#' if xs[idx] - 1 <= (idx % 40) <= xs[idx] + 1 else '.', range(240)))
for i in range(0, 240, 40):
    print(''.join(pixels[i:i+40]))

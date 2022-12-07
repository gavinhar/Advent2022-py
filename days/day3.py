f = open('../input/day3.txt').readlines()
f = list(map(lambda x: x.strip(), f))

priorities = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

total = 0
for i in range(int(len(f) / 3)):
    a = set(f[3 * i])
    b = set(f[3 * i + 1])
    c = set(f[3 * i + 2])
    d = list(a.intersection(b, c))
    priority = priorities.find(d[0])
    total += priority

print(total)

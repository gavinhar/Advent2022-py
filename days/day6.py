f = open('../input/day6.txt').read()

c = 14
for i in range(len(f) - c + 1):
    chunk = f[i:i + c]
    if len(set(chunk)) == c:
        print(i + c)
        exit(0)

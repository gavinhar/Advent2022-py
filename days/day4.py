with open('../input/day4.txt') as f:
    total = 0
    for line in f:
        a, b = line.strip().split(',')
        a_left, a_right = map(lambda x: int(x), a.split('-'))
        b_left, b_right = map(lambda x: int(x), b.split('-'))

        a_range = set(range(int(a_left), int(a_right) + 1))
        b_range = set(range(int(b_left), int(b_right) + 1))

        if len(a_range.intersection(b_range)) > 0:
            total += 1

    print(total)

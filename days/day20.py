from typing import List


def solution(nums: List[int], rounds=1, dec_key=1) -> int:
    original = [(i, nums[i] * dec_key) for i in range(len(nums))]
    mixed = original.copy()

    zero = None
    for _ in range(rounds):
        for elm in original:
            if elm[1] == 0:
                zero = elm
                continue

            idx = mixed.index(elm)
            mixed.pop(idx)
            mixed.insert(((idx + elm[1]) % len(mixed)), elm)

    idx = mixed.index(zero)
    return sum([mixed[(idx + offset) % len(mixed)][1] for offset in [1000, 2000, 3000]])


with open('../input/day20.txt') as f:
    puzzle_input: List[int] = [int(line.strip()) for line in f.readlines()]
    print(solution(puzzle_input))
    print(solution(puzzle_input, 10, 811589153))

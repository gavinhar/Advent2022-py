from itertools import permutations
from typing import List, Tuple, IO, Dict, Iterable

INF = 1_000_000


def parse_line(line: str) -> Tuple[str, int, List[str]]:
    tokens = line.strip().split(' ')
    name = tokens[1]
    rate = int(tokens[4].split('=')[1][:-1])
    paths = [p.split(',')[0] for p in tokens[9:]]
    return name, rate, paths


def next_perm(
        data: Dict[str, Tuple[int, List[str]]],
        valves: List[str],
        indexes: Dict[str, int],
        shortest_paths: List[List[int]],
        prev: str = 'AA',
        time: int = 30
) -> List[str]:
    for valve in valves:
        t = shortest_paths[indexes[prev]][indexes[valve]] + 1
        if t < time:
            remaining = valves.copy()
            remaining.remove(valve)
            for tail in next_perm(data, remaining, indexes, shortest_paths, valve, time - t):
                rv = [valve]
                rv.extend(tail)
                yield rv
    yield []


def next_perm2(
        data: Dict[str, Tuple[int, List[str]]],
        valves: List[str],
        indexes: Dict[str, int],
        shortest_paths: List[List[int]],
):
    for perm1 in next_perm(data, valves, indexes, shortest_paths, time=26):
        remaining = list(set(valves) - set(perm1))
        for perm2 in next_perm(data, remaining, indexes, shortest_paths, time=26):
            yield perm1, perm2


def calculate_flow(
        data: Dict[str, Tuple[int, List[str]]],
        valves: Dict[str, int],
        shortest_paths: List[List[int]],
        permutation: Iterable[str],
        time_limit=30
) -> int:
    time = 0
    pos = 'AA'
    flows: List[Tuple[int, int]] = []  # (time activated, flow rate)
    for valve in permutation:
        start = valves[pos]
        dest = valves[valve]
        time = time + 1 + shortest_paths[start][dest]
        flow_rate = data[valve][0]
        flows.append((time, flow_rate))
        pos = valve

    rv = 0
    for flow in flows:
        rv = rv + max(0, time_limit - flow[0]) * flow[1]
    return rv


def solution(f: IO) -> Tuple[int, int]:
    data: Dict[str, Tuple[int, List[str]]] = {}
    working_valves: List[str] = []
    all_valves: List[str] = []
    for line in f:
        name, rate, paths = parse_line(line)
        data[name] = (rate, paths)
        all_valves.append(name)
        if rate > 0:
            working_valves.append(name)

    shortest_paths = [[INF] * len(all_valves) for v in all_valves]
    for i in range(len(all_valves)):
        valve = all_valves[i]
        shortest_paths[i][i] = 0
        for path in data[valve][1]:
            idx = all_valves.index(path)
            shortest_paths[i][idx] = 1
            shortest_paths[idx][i] = 1

    for k in range(len(all_valves)):
        for i in range(len(all_valves)):
            for j in range(len(all_valves)):
                if shortest_paths[i][k] + shortest_paths[k][j] < shortest_paths[i][j]:
                    shortest_paths[i][j] = shortest_paths[i][k] + shortest_paths[k][j]

    indexes = {all_valves[i]: i for i in range(len(all_valves))}

    max_flow = 0
    for permutation in next_perm(data, working_valves, indexes, shortest_paths):
        flow = calculate_flow(data, indexes, shortest_paths, permutation)
        max_flow = max(max_flow, flow)

    max_flow2 = 0
    for perm1, perm2 in next_perm2(data, working_valves, indexes, shortest_paths):
        flow = calculate_flow(data, indexes, shortest_paths, perm1, time_limit=26) + \
               calculate_flow(data, indexes, shortest_paths, perm2, time_limit=26)
        max_flow2 = max(max_flow2, flow)

    return max_flow, max_flow2


with open('../sample/day16.txt') as f:
    part1, part2 = solution(f)
    assert 1651 == part1
    assert 1707 == part2

with open('../input/day16.txt') as f:
    part1, part2 = solution(f)
    print('part1', part1)
    print('part2', part2)

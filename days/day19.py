import heapq
from typing import IO, Tuple


class Costs:
    def __init__(self, line):
        self.ore_bot_cost = int(line[6])
        self.clay_bot_cost = int(line[12])
        self.obsidian_bot_ore = int(line[18])
        self.obsidian_bot_clay = int(line[21])
        self.geode_bot_ore = int(line[27])
        self.geode_bot_obsidian = int(line[30])
    

class Context:
    def __init__(self):
        self.time = 24

        self.ore_bots = 1
        self.clay_bots = 0
        self.obsidian_bots = 0
        self.geode_bots = 0
        
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0
        self.est = None
    
    def copy(self):
        rv = Context()
        rv.time = self.time
        rv.ore_bots = self.ore_bots
        rv.clay_bots = self.clay_bots
        rv.obsidian_bots = self.obsidian_bots
        rv.geode_bots = self.geode_bots
        rv.ore = self.ore
        rv.clay = self.clay
        rv.obsidian = self.obsidian
        rv.geodes = self.geodes
        rv.est = None
        return rv

    def add_ore_bot(self, costs):
        rv = self.copy()
        rv.ore_bots += 1
        rv.ore -= costs.ore_bot_cost
        return rv

    def add_clay_bot(self, costs):
        rv = self.copy()
        rv.clay_bots += 1
        rv.ore -= costs.clay_bot_cost
        return rv

    def add_obsidian_bot(self, costs):
        rv = self.copy()
        rv.obsidian_bots += 1
        rv.ore -= costs.obsidian_bot_ore
        rv.clay -= costs.obsidian_bot_clay
        return rv

    def add_geode_bot(self, costs):
        rv = self.copy()
        rv.geode_bots += 1
        rv.ore -= costs.geode_bot_ore
        rv.obsidian -= costs.geode_bot_obsidian
        return rv

    def mine_material(self):
        rv = self.copy()
        rv.ore += self.ore_bots
        rv.clay += self.clay_bots
        rv.obsidian += self.obsidian_bots
        rv.geodes += self.geode_bots
        return rv

    def __str__(self):
        return f'{self.time}:{self.ore_bots},{self.clay_bots},{self.obsidian_bots},{self.geode_bots}:' + \
                    f'{self.ore},{self.clay},{self.obsidian},{self.geodes}:{self.estimate()}'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def estimate(self):
        # Assume optimistic view that 1 bot can be created per turn, max geodes is time * current geodes + 1, 2, ... m
        # where m is the max number of geode bots we can make before time runs out.
        # This will inevitably favor having more time, but should prune the search space to favor more geode bots when
        # t is small
        if self.est is None:
            rv = self.geodes + self.geode_bots * self.time
            m1 = 1 if self.clay_bots == 0 else 0  # can't make obsidian bots without clay
            m2 = 1 if self.obsidian_bots == 0 else 0  # can't make geode bots without obsidian
            for i in range(1, self.time - m1 - m2 + 1):
                rv += i
            self.est = rv
        return self.est

    def __lt__(self, other):
        return self.estimate() > other.estimate()


def calc(costs: Costs, ctx: Context):
    heap = [ctx]
    rv = 0
    visited = {ctx}

    last_est = 1_000_000
    while True:
        curr = heapq.heappop(heap)
        c_est = curr.estimate()
        if c_est != last_est:
            print(f'est: {c_est} ({len(heap)})')
            last_est = c_est

        if curr.time == 0:
            rv = max(rv, curr.geodes)
            continue

        if curr.estimate() <= rv:
            print(f'done: {rv} ({last_est})')
            return rv

        new_ctx = curr.mine_material()
        new_ctx.time -= 1

        if new_ctx.time == 0:
            rv = max(rv, new_ctx.geodes)
            continue

        if new_ctx not in visited:
            visited.add(new_ctx)
            heapq.heappush(heap, new_ctx)

        if curr.ore >= costs.ore_bot_cost:
            new_with_ore = new_ctx.add_ore_bot(costs)
            if new_with_ore not in visited:
                visited.add(new_with_ore)
                heapq.heappush(heap, new_with_ore)

        if curr.ore >= costs.clay_bot_cost:
            new_with_clay = new_ctx.add_clay_bot(costs)
            if new_with_clay not in visited:
                visited.add(new_with_clay)
                heapq.heappush(heap, new_with_clay)

        if curr.ore >= costs.obsidian_bot_ore and curr.clay >= costs.obsidian_bot_clay:
            new_with_obs = new_ctx.add_obsidian_bot(costs)
            if new_with_obs not in visited:
                visited.add(new_with_obs)
                heapq.heappush(heap, new_with_obs)

        if curr.ore >= costs.geode_bot_ore and curr.obsidian >= costs.geode_bot_obsidian:
            new_with_geode = new_ctx.add_geode_bot(costs)
            if new_with_geode not in visited:
                visited.add(new_with_geode)
                heapq.heappush(heap, new_with_geode)


def solution(f: IO) -> int:
    blueprints = []
    for line1 in f:
        line = line1.strip().split(' ')
        # n = int(line[1][:-1])
        blueprints.append(Costs(line))

    rv = 0
    for i in range(0, len(blueprints)):
        n = i + 1
        print('start', n)
        max_n = calc(blueprints[i], Context())
        rv += n * max_n
        print('max', n, ':', max_n)

    return rv


def solution2(f: IO) -> int:
    blueprints = []
    for line1 in f:
        line = line1.strip().split(' ')
        # n = int(line[1][:-1])
        blueprints.append(Costs(line))

    rv = 1
    for i in range(3):
        ctx = Context()
        ctx.time = 32
        rv *= calc(blueprints[i], ctx)

    return rv


# with open('../sample/day19.txt') as f:
#     part1, part2 = solution(f)
#     assert part1 == 33
#     print('part1', part1)
#     print('part2', part2)
#     print()

# with open('../input/day19.txt') as f:
#     print('part1', solution2(f))


with open('../input/day19.txt') as f:
    print('part2', solution2(f))
    print()

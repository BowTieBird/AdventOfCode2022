import re
import pbd

file = open("input.txt")

debug = False

p = re.compile("Blueprint (.*): Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.")
blueprints_re = [ p.search(line) for line in file.readlines() ]

def maximiseGeodes(costs, robots, resources, t, next_buy=None, collect_resources=False):
    if t == 0:
        return resources['geode']

    # Collection
    if collect_resources:
        for resource in resources.keys():
            resources[resource] += robots[resource]

    # Determine which can be bought
    possible_buy_sets = []
    num_ore = 0
    while (ore_left := resources['ore'] - num_ore*costs['ore']['ore']) >= 0:
        num_clay = 0
        while (ore_left_2 := ore_left - num_clay*costs['clay']['ore']) >= 0:
            num_obsidian = 0
            while (ore_left_3 := ore_left_2 - num_obsidian*costs['obsidian']['ore'] ) >= 0 \
                and num_obsidian*costs['obsidian']['clay'] <= resources['clay']:
                num_geode = 0
                while num_geode*costs['geode']['ore'] <= ore_left_3  \
                    and num_geode*costs['geode']['obsidian'] <= resources['obsidian']:
                    # breakpoint()
                    possible_buy_sets.append({ 'ore': num_ore, 'clay': num_clay, 'obsidian':num_obsidian, 'geode': num_geode})
                    num_geode += 1
                num_obsidian += 1
            num_clay += 1
        num_ore += 1
    print("Buy sets: ", len(possible_buy_sets))

    # Return maximum buy
    possible_cracks = set()
    for buy in possible_buy_sets:
        new_robots = {robot: val + buy[robot] for robot, val in robots.items()}
        new_resources = {}
        for resource, value in resources.items():
            spent = sum([buy[other] * costs[other][resource] for other in resources.keys() if resource in costs[other]])
            new_resources[resource] = value - spent
        if debug: print("t: ", t)
        if debug: print("robots:", new_robots)
        if debug: print("resources:", new_resources)
        if debug: breakpoint()
        possible_cracks.add(maximiseGeodes(costs, new_robots,  new_resources, t-1, collect_resources=True))
    return max(possible_cracks)

for blueprint in blueprints_re:
    robots =  { 'ore':1, 'clay':0, 'obsidian':0, 'geode':0 }
    resources =  { 'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0 }

    ore_robot_ore_cost = int(blueprint.group(2))
    clay_robot_ore_cost = int(blueprint.group(3))
    obsidian_robot_ore_cost = int(blueprint.group(4))
    obsidian_robot_clay_cost = int(blueprint.group(5))
    geode_robot_ore_cost = int(blueprint.group(6))
    geode_robot_obsidian_cost = int(blueprint.group(7))
    costs = {
        'ore': {
            'ore':ore_robot_ore_cost
        },
        'clay': {
            'ore':clay_robot_ore_cost
        },
        'obsidian': {
            'ore':obsidian_robot_ore_cost,
            'clay':obsidian_robot_clay_cost
        }, 'geode': {
            'ore':geode_robot_ore_cost,
            'obsidian':geode_robot_obsidian_cost
        }
    }
    print(costs)
    print(int(blueprint.group(1)) * maximiseGeodes(costs, robots, resources, 24))

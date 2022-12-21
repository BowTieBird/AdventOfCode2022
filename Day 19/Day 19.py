import re

file = open("input.txt")

p = re.compile("Blueprint (.*): Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.")
blueprints_re = [ p.search(line) for line in file.readlines() ]

def maximiseGeodes(blueprint, robots, resources, t, next_buy=None, collect_resources=False):
    if t == 0:
        # print(resources)
        return resources['geode']

    ore_robot_cost = int(blueprint.group(2))
    clay_robot_cost = int(blueprint.group(3))
    obsidian_robot_ore_cost = int(blueprint.group(4))
    obsidian_robot_clay_cost = int(blueprint.group(5))
    geode_robot_ore_cost = int(blueprint.group(6))
    geode_robot_obsidian_cost = int(blueprint.group(7))
    costs = {'ore':{'ore':ore_robot_cost}, 'clay':{'ore':clay_robot_cost}, 'obsidian':{'ore':obsidian_robot_ore_cost, 'clay':obsidian_robot_clay_cost}, 'geode':{'ore':geode_robot_ore_cost, 'obsidian':geode_robot_obsidian_cost}}

    # Collection (We'll say it happens at the beginning of the following minute)
    if collect_resources:
        for resource in resources.keys():
            resources[resource] += robots[resource]

    if next_buy is None:
        # Possible choices for the next buy
        next_possible_buys = {'ore', 'clay'}
        if robots['clay'] >= 1:
            next_possible_buys.add('obsidian')
        if robots['obsidian'] >= 1:
            next_possible_buys.add('geode')
    else:
        next_possible_buys = { next_buy }
        
    # Determine which can be bought immediately
    possible_immediate_buys = set()
    for buy in next_possible_buys:
        cost = costs[buy]
        buyable = True
        for resource in cost.keys():
            if cost[resource] > resources[resource]:
                buyable = False
                break
        # if all([cost[resource] >= resources[resource] for resource in cost.keys()]):
        if buyable:
            possible_immediate_buys.add(buy)      

    # Return maximum buy
    possible_cracks = set()
    for buy in next_possible_buys:
        if buy in possible_immediate_buys:
            new_robots =  { robot: val + 1 if robot == buy else val for robot, val in robots.items() }
            new_resources = { resource: val - costs[buy][resource] if resource in costs[buy].keys() else val for resource, val in resources.items() }
            # print("robots:", new_robots)
            # print("resources:", new_resources)
            possible_cracks.add(maximiseGeodes(blueprint, new_robots,  new_resources, t, collect_resources=False))
        else:
            possible_cracks.add(maximiseGeodes(blueprint, robots, resources, t-1, next_buy=buy, collect_resources=True))
    return max(possible_cracks)

for blueprint in blueprints_re:
    robots = { 'ore':1, 'clay':0, 'obsidian':0, 'geode':0 }
    resources =  { 'ore':0, 'clay':0, 'obsidian':0, 'geode':0 }
    print(int(blueprint.group(1)) * maximiseGeodes(blueprint, robots, resources, 24))




    
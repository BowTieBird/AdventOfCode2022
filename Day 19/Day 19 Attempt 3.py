import re

file = open("input.txt")

T = 32
p = re.compile("Blueprint (.*): Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.")
blueprints_re = [ p.search(line) for line in file.readlines() ]

def maximiseGeodes(costs, robots, resources, t, next_buy=None):
    # Collection 
    new_resources = { resource: val + robots[resource] for resource, val in resources.items()}

    # Return number of geodes
    if t == 1:
        # print("  " * (T-t), "t:", t, " robots:", robots, " resources:", new_resources)
        return new_resources['geode'], []

    # Determine which can be bought (using old resource values)
    if next_buy is None:
        # Possible choices for the next buy
        # Only try to buy if we have the robots to obtain the payment resources,
        # and don't buy if we already have enough robots to buy anything that requires that resource
        next_possible_buys = set()
        if robots['ore'] < max(costs['clay']['ore'], costs['obsidian']['ore'], costs['geode']['ore']):
            next_possible_buys.add('ore')
        if robots['clay'] < costs['obsidian']['clay']:
            next_possible_buys.add('clay')
        if robots['clay'] >= 1 and robots['obsidian'] < costs['geode']['obsidian']:
            next_possible_buys.add('obsidian')
        if robots['obsidian'] >= 1:
            next_possible_buys.add('geode')
    else:
        next_possible_buys = {next_buy}
        
    # print("  " * (T-t), "t:", t, " buys:", next_possible_buys, " robots:", robots, " resources:", new_resources)

    # Return maximum buy
    possible_cracks = []
    for buy in next_possible_buys:
        # Check if old resources can pay for the buy
        if all([resources[pay] >= costs[buy][pay] 
                for pay in costs[buy].keys()]):
            next_robots = {robot: val + 1 if robot == buy else val
                for robot, val in robots.items()}
            next_resources = {resource: val - costs[buy][resource] if resource in costs[buy].keys() else val
                for resource, val in new_resources.items()}
            for val in resources.values():
                assert val >= 0
            possible_cracks.append(maximiseGeodes(costs, next_robots,  next_resources, t-1) + tuple([buy]))
        else:
            next_robots = {robot: val for robot, val in robots.items()}
            next_resources = {resource: val for resource, val in new_resources.items()}
            possible_cracks.append(maximiseGeodes(costs, next_robots,  next_resources, t-1, next_buy=buy) + tuple([buy]))
    max_crack = 0
    buy_path = []
    for crack in possible_cracks:
        if crack[0] >= max_crack:
            max_crack = crack[0]
            buy_path = [crack[2]] + crack[1]
    return max_crack, buy_path

quality = 0
multiply = 1
for blueprint in blueprints_re:
    robots =  { 'ore':1, 'clay':0, 'obsidian':0, 'geode':0 }
    resources =  { 'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0 }

    id = int(blueprint.group(1))
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
    geodes =  maximiseGeodes(costs, robots, resources, T)
    print(id, geodes)
    quality += id * geodes[0]
    multiply *= geodes[0]

    if id == 3:
        break

print("Quality: ", quality)
print("Multiply: ", multiply)

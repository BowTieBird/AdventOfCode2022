import re

file = open("input.txt")

p = re.compile("Blueprint (.*): Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.")
blueprints_re = [ p.search(line) for line in file.readlines() ]

def maximiseGeodes(blue_print, robots, resources, t):
    if t == 0:
        return resources['geode']

    ore_robot_cost = int(blue_print.group(2))
    clay_robot_cost = int(blue_print.group(3))
    obsidian_robot_ore_cost = int(blue_print.group(4))
    obsidian_robot_clay_cost = int(blue_print.group(5))
    geode_robot_ore_cost = int(blue_print.group(6))
    geode_robot_obsidian_cost = int(blue_print.group(7))
    costs = {'ore':{'ore':ore_robot_cost}, 'clay':{'ore':clay_robot_cost}, 'obsidian':{'ore':obsidian_robot_ore_cost, 'clay':obsidian_robot_clay_cost}, 'geode':{'ore':geode_robot_ore_cost, 'obsidian':geode_robot_obsidian_cost}}

    # Only buy when "just reached"
    possible_buys = [{}]

    if resources['ore'] == ore_robot_cost: 
        possible_buys.append({'ore':1})

    if resources['ore'] == clay_robot_cost:
        possible_buys.append({'clay':1})

    if (resources['ore'] == obsidian_robot_ore_cost and resources['clay'] >= obsidian_robot_clay_cost) \
            or (resources['ore'] >= obsidian_robot_ore_cost and resources['clay'] == obsidian_robot_clay_cost):
        possible_buys.append({'obsidian':1})

    if (resources['ore'] == geode_robot_ore_cost and resources['obsidian'] >= geode_robot_obsidian_cost) \
            or (resources['ore'] >= geode_robot_ore_cost and resources['obsidian'] == geode_robot_obsidian_cost):
        possible_buys.append({'geode':1})
    
    # Collection
    for resource in resources.keys():
        resources[resource] += robots[resource]
    print(possible_buys)
    print(resources)

    # Return maximum buy
    possible_cracks = []
    for buy in possible_buys:
        new_robots = { robot: val + buy[robot] if robot in buy.keys() else val for robot, val in robots.items() }
        new_resources = { resource: val - sum([buy[robot] * costs[robot][resource] for robot in robots.items() if robot in buy.keys() and resource in costs[robot].keys()]) for resource, val in resources.items() }
        print([buy[robot] * costs[robot][resource] for robot in robots.items() if robot in buy.keys() and resource in costs[robot].keys() for resource in resources.keys()])
        possible_cracks.append(maximiseGeodes(blue_print, new_robots,  new_resources, t-1))
    return max(possible_cracks)




for blue_print in blueprints_re:
    robots = { 'ore':1, 'clay':0, 'obsidian':0, 'geode':0 }
    resources =  { 'ore':0, 'clay':0, 'obsidian':0, 'geode':0 }
    print(maximiseGeodes(blue_print, robots, resources, 24))




    
import collections
import copy

def read_input(filename):
    with open(filename, 'r') as f:
        line = f.readline().strip()
        start_node = line[line.index('"')+1:-1]
        line = f.readline().strip()
        end_node = line[line.index('"')+1:-1]
        line = f.readline().strip()
        maxTime = int(line[line.index('=')+2:-3])
        line = f.readline().strip().split(' , ')
    letters = {}
    parsed = []
    letters_arr = []
    added = 0

    for chunk in line:
        chunk = chunk.strip()
        index = len(chunk) - 1

        while chunk[index] != ',':
            index -= 1
        cooldown = int(chunk[index + 2:chunk[index+2:].index(' ') + index + 2])
        comma_index = index

        while chunk[index] != '$':
            index -= 1
        cost = int(chunk[index+1:comma_index])
        dollar_index = index

        while chunk[index] != '>':
            index -=  1
        node2 = chunk[index+1:dollar_index-2]
        node1 = chunk[:index-1]

        if node1 not in letters:
            letters[node1] = added
            added += 1
            letters_arr.append(node1)
        if node2 not in letters:
            letters[node2] = added
            added += 1
            letters_arr.append(node2)

        parsed.append([letters[node1], letters[node2], cost, cooldown])

    start_index = letters[start_node]
    end_index = letters[end_node]
    return start_index, end_index, maxTime, parsed, letters_arr


def question3Main(startingNode, endingNode, maxTime, edges, n):
    # Initialize graph
    graph = collections.defaultdict(list)
    for node1, node2, cost, t in edges:
        graph[node1].append([node2, cost, t])

    # Initialize variables
    lowestCost = float('inf')
    lowestPath = []
    lowestTime = 0
    queue = collections.deque()
    start = 1 << startingNode
    pathStart = []
    pathStart.append(startingNode)
    queue.append((startingNode, start, 0, 0, pathStart))
    end = (1 << n) - 1 

    #seen = collections.defaultdict(lambda: {maxTime: float('inf')})
    seen = {}

    # BFS with bitmasking
    while queue:
        currNode, currMask, weight, currTime, currPath = queue.popleft()
        #print(currNode, bin(currMask), weight)
        #print(currPath)
        if currMask == end and currNode == endingNode:
            if lowestCost > weight:
                lowestCost = weight
                lowestPath = currPath
                lowestTime = currTime
            continue
        
        for neighbor, edgeWeight, edgeTime in graph[currNode]:
            neighborBit = 1 << neighbor
            nextMask = currMask | neighborBit
            newWeight = weight + edgeWeight
            newTime = currTime + edgeTime

            # Ignores the possibility if time exceeded
            if newTime > maxTime:
                continue
            
            # Create empty dictionary if it is not in seen yet
            if (neighbor, nextMask) not in seen:
                seen[(neighbor, nextMask)] = {}

            # Loop over values in seen[(neighbor, nextMask)] to see if we have a valid point
            is_better = True
            for key, val in seen[(neighbor, nextMask)].items(): # key => time, val => cost
                if newWeight >= val and newTime >= key: # better path exists already
                    is_better = False
                    break
            
            if is_better: # update seen
                currPath.append(neighbor)
                seen[(neighbor, nextMask)][newTime] = newWeight
                queue.append((neighbor, nextMask, newWeight, newTime, copy.copy(currPath)))
                currPath.pop()

    if lowestCost != float('inf'):
        return lowestCost, lowestPath, lowestTime
    return -1, "", ""

def to_human_readable(best_path, node_names):
    return ', '.join([f'{node_names[best_path[i]]}->{node_names[best_path[i+1]]}' for i in range(len(best_path) - 1)])


if __name__ == '__main__':
    #take input file
    file = "inputs/a3.in"
    startNode, endNode, maxTime, edgesList, letterMap = read_input(file)
    #print(startNode)
    #print(endNode)
    #print(edgesList)
    #print(letterMap)
    #print(len(letterMap))
    #error checking in main function
    #check if only 1 node
    #print("\n\n")


    cost, path, travelTime = question3Main(startNode, endNode, maxTime, edgesList, len(letterMap))
    #print("\n\n")
    s = to_human_readable(path, letterMap)
    print(f'Best path: {s}')
    print(f'Cost: ${cost}')
    print(f'Time: {travelTime}')
    #print("\n\n")


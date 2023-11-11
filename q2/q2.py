import collections
import copy

# Gets first value in quotations
def getValueInQuotes(s):
    res = ''
    opened = False
    openingChars = ['"', "'", '“']
    closingChars = ['"', "'", '”']
    for char in s:
        if not opened and char in openingChars:
            opened = True
            continue
        if opened and char in closingChars:
            opened = False
        if opened:
            res += char
    return res

# Get int value, ignoring anything that comes after an int
def parseForInt(s):
    res = ''
    for char in s:
        if char.isdigit():
            res += char
        else:
            return int(res)
    return int(res)

def readInput(filename):

    with open(filename, 'r',  encoding='utf-8') as f:
        # Parse first line
        line = f.readline().strip()
        startNodeName = getValueInQuotes(line)
        # Parse second line
        line = f.readline().strip()
        endNodeName = getValueInQuotes(line)
        # Read third line
        line = f.readline().strip().split(',')
    
    # Process third line
    letters = {}
    edges = []
    letters_arr = []
    added = 0

    for chunk in line: # a chunk refers to a connection in string form
        node1 = chunk.split('->')[0].strip()
        node2 = chunk.split('->')[1].split('(')[0].strip()
        cost = parseForInt(chunk.split('$')[1])

        if node1 not in letters:
            letters[node1] = added
            added += 1
            letters_arr.append(node1)

        if node2 not in letters:
            letters[node2] = added
            added += 1
            letters_arr.append(node2)

        edges.append([letters[node1], letters[node2], cost])

    # Account for the case where start node or end node is an island
    if startNodeName not in letters:
        letters[startNodeName] = added
        added += 1
        letters_arr.append(startNodeName)

    if endNodeName not in letters:
        letters[endNodeName] = added
        added += 1
        letters_arr.append(endNodeName)

    startNode = letters[startNodeName]
    endNode = letters[endNodeName]

    return startNode, endNode, edges, letters_arr

# starting node, ending node, edges all in 0-indexed form
def question2Main(startingNode, endingNode, edges, n):
    # uses a queue to traverse the graph

    # Initialize ajacency list structure: {node1: [node2, 'cost to go to node2']}
    graph = collections.defaultdict(list)
    for node1, node2, cost in edges:
        graph[node1].append([node2, cost])

    # lowestCost, lowestPath updated when a possible solution is reached
    # possible solution: every single node reached and current node is endingNode
    # if lowestCost stays as float('inf), then there is no possible path from start to end
    lowestCost = float('inf')
    lowestPath = []

    # bit mask for starting node
    start = 1 << startingNode

    pathStart = []
    pathStart.append(startingNode)
    # queue used for breadth first search
    # queue: (currentNode, currentBitMask)
    queue = collections.deque()
    queue.append((startingNode, start, 0, pathStart))
    # ending mask if n = 5, (11111) this means every node has been visited
    end = (1 << n) - 1 

    seen = collections.defaultdict(int)
    
    # BFS with bitmasking
    while queue:
        currNode, currMask, weight, currPath = queue.popleft()

        #if all nodes have been reached and current node is endnode
        if currMask == end and currNode == endingNode:
            if lowestCost > weight:
                lowestCost = weight
                lowestPath = currPath
            continue
        
        #loop through all neighbors of current node (in ajacency list)
        for neighbor, edgeWeight in graph[currNode]:
            neighborBit = 1 << neighbor
            # OR bit manipulation
            nextMask = currMask | neighborBit
            newWeight = weight + edgeWeight
            # if node already visited and newCost is more, then will skip as this will not
            # bring us the optimal solution
            if ((neighbor, nextMask) not in seen) or newWeight < seen[(neighbor, nextMask)]:
                seen[(neighbor, nextMask)] = newWeight 
                # use back tracking to track path of visited nodes
                currPath.append(neighbor)
                queue.append((neighbor, nextMask, newWeight, copy.copy(currPath)))
                currPath.pop()

    # if lowestCost still equals float('inf), then no possible path from start to end exists
    # otherwise, return the cost and path 
    if lowestCost != float('inf'):
        return lowestCost, lowestPath
    return -1, ""

def to_human_readable(best_path, node_names):
    return ', '.join([f'{node_names[best_path[i]]}->{node_names[best_path[i+1]]}' for i in range(len(best_path) - 1)])


import glob
import os

if __name__ == '__main__':
    #take input file
    file = "a.in"
    startNode, endNode, edgesList, letterMap = read_input(file)


    cost, path = question2Main(startNode, endNode, edgesList, len(letterMap))
    #print("\n\n")
    s = to_human_readable(path, letterMap)
    print(f'Best path: {s}')
    print(f'Cost: ${cost}')
    #print("\n\n")

    filenames = glob.glob('input/*')
    
    if not os.path.isdir('output'):
        os.mkdir('output')
    
    for filename in filenames:

        startNode, endNode, edgesList, letterMap = readInput(filename)
        cost, path = question2Main(startNode, endNode, edgesList, len(letterMap))

        basename = os.path.basename(filename)
        with open(os.path.join('output', basename[:basename.index('.')] + '.out'), 'w') as f:
            s = to_human_readable(path, letterMap)
            f.write(f'Best path: {s}\nCost: ${cost}')
            print(f'\n{filename}\nBest path: {s}\nCost: ${cost}\n')
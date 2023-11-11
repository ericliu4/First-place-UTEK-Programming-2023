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

    with open(filename, 'r', encoding='utf-8') as f:
        # Parse first line
        line = f.readline().strip()
        startNodeName = getValueInQuotes(line)
        # Parse second line
        line = f.readline().strip()
        endNodeName = getValueInQuotes(line)
        # Parse third line
        line = f.readline().strip()
        index = 0
        while not line[index].isdigit():
            index += 1
        maxTime = parseForInt(line[index:])
        # Read third line
        line = f.readline().strip().split(',') # two elements combine to form one entry
    
    # Process third line
    letters = {}
    edges = []
    letters_arr = []
    added = 0

    for i in range(len(line) // 2):
        chunk1 = line[2*i]
        chunk2 = line[2*i + 1]
        node1 = chunk1.split('->')[0].strip()
        node2 = chunk1.split('->')[1].split('(')[0].strip()
        cost = parseForInt(chunk1.split('$')[1])
        index = 0
        while not chunk2[index].isdigit():
            index += 1
        t = parseForInt(chunk2[index:])

        if node1 not in letters:
            letters[node1] = added
            added += 1
            letters_arr.append(node1)

        if node2 not in letters:
            letters[node2] = added
            added += 1
            letters_arr.append(node2)

        edges.append([letters[node1], letters[node2], cost, t])

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

    return startNode, endNode, maxTime, edges, letters_arr


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


import glob
import os

if __name__ == '__main__':

    filenames = glob.glob('input/*')
    
    if not os.path.isdir('output'):
        os.mkdir('output')
    
    for filename in filenames:

        startNode, endNode, maxTime, edgesList, letterMap = readInput(filename)
        cost, path, totalTime = question3Main(startNode, endNode, maxTime, edgesList, len(letterMap))

        basename = os.path.basename(filename)
        with open(os.path.join('output', basename[:basename.index('.')] + '.out'), 'w') as f:
            s = to_human_readable(path, letterMap)
            f.write(f'Best path: {s}\nCost: ${cost}\nTime: {totalTime} mins\n')
            print(f'\n{filename}\nBest path: {s}\nCost: ${cost}\nTime: {totalTime} mins\n')
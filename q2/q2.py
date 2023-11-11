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


def question2Main(startingNode, endingNode, edges, n):
    # Initialize graph
    graph = collections.defaultdict(list)
    for node1, node2, cost in edges:
        graph[node1].append([node2, cost])

    # Initialize variables
    lowestCost = float('inf')
    lowestPath = []
    queue = collections.deque()
    start = 1 << startingNode
    pathStart = []
    pathStart.append(startingNode)
    queue.append((startingNode, start, 0, pathStart))
    end = (1 << n) - 1 
    seen = collections.defaultdict(int)
    
    # BFS with bitmasking
    while queue:
        currNode, currMask, weight, currPath = queue.popleft()
        #print(currNode, bin(currMask), weight)
        #print(currPath)
        if currMask == end and currNode == endingNode:
            if lowestCost > weight:
                lowestCost = weight
                lowestPath = currPath
            continue
        
        for neighbor, edgeWeight in graph[currNode]:
            neighborBit = 1 << neighbor
            nextMask = currMask | neighborBit
            newWeight = weight + edgeWeight
            if ((neighbor, nextMask) not in seen) or newWeight < seen[(neighbor, nextMask)]:
                seen[(neighbor, nextMask)] = newWeight 
                currPath.append(neighbor)
                seen[(neighbor, nextMask)] = newWeight
                queue.append((neighbor, nextMask, newWeight, copy.copy(currPath)))
                currPath.pop()
    if lowestCost != float('inf'):
        return lowestCost, lowestPath
    return -1, ""

def to_human_readable(best_path, node_names):
    return ', '.join([f'{node_names[best_path[i]]}->{node_names[best_path[i+1]]}' for i in range(len(best_path) - 1)])


import glob
import os

if __name__ == '__main__':

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
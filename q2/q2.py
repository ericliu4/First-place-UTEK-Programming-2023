import collections
import copy

def read_input(filename):
    with open(filename, 'r') as f:
        line = f.readline().strip()
        start_node = line[line.index('"')+1:-1]
        line = f.readline().strip()
        end_node = line[line.index('"')+1:-1]
        line = f.readline().strip().split(', ')
    letters = {}
    parsed = []
    letters_arr = []
    added = 0

    for chunk in line:
        index = len(chunk) - 1
        while chunk[index] != '$':
            index -= 1
        cost = int(chunk[index+1:-1])
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

        parsed.append([letters[node1], letters[node2], cost])

    start_index = letters[start_node]
    end_index = letters[end_node]
    return start_index, end_index, parsed, letters_arr


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


if __name__ == '__main__':
    #take input file
    file = "a.in"
    startNode, endNode, edgesList, letterMap = read_input(file)
    #print(startNode)
    #print(endNode)
    #print(edgesList)
    #print(letterMap)
    #print(len(letterMap))
    #error checking in main function
    #check if only 1 node
    #print("\n\n")


    cost, path = question2Main(startNode, endNode, edgesList, len(letterMap))
    #print("\n\n")
    s = to_human_readable(path, letterMap)
    print(f'Best path: {s}')
    print(f'Cost: ${cost}')
    #print("\n\n")


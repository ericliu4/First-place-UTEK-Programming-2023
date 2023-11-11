# This function will take in a filename and output an adjacency list and node names
def readInput(filename):

    with open(filename, 'r') as f:
        line = f.read().strip()

    chunks = line.split(',') # Here each chunk represents one connection (string)

    nameToIndex = {}
    names = []
    nodeCount = 0
    adjList = []

    for chunk in chunks:

        nodes = chunk.split('->')
        name1 = nodes[0].strip()
        name2 = nodes[1].strip()

        if name1 not in nameToIndex:
            nameToIndex[name1] = nodeCount
            nodeCount += 1
            adjList.append([])
            names.append(name1)

        if name2 not in nameToIndex:
            nameToIndex[name2] = nodeCount
            nodeCount += 1
            adjList.append([])
            names.append(name2)
        
        adjList[nameToIndex[name1]].append(nameToIndex[name2])
    
    return adjList, names


# This function will take an adjacency list as input and output an adjacency matrix
def adjListToMatrix(adjList):

    n = len(adjList)

    adjMatrix = [[0] * n for i in range(n)]

    for i in range(n):
        for dest in adjList[i]:
            adjMatrix[i][dest] = 1
    
    return adjMatrix


# This function will take an adjacency matrix and node names and output a pretty matrix
def getHumanReadable(adjMatrix, names):
    
    nameLengths = list(map(lambda x: len(x), names))
    maxNameLength = max(nameLengths)
    nameBuffers = list(map(lambda x: maxNameLength - x + 1, nameLengths))

    n = len(names)

    s = ' ' * (maxNameLength + 1) + '|' + '|'.join([' ' + names[i] + ' ' for i in range(n)])
    s += '\n' + '-' * (maxNameLength + 1) + '+' + '-'.join(['-' * (nameLengths[i] + 2) for i in range(n)])
    
    for i in range(n):
        s += '\n' + names[i] + ' ' * nameBuffers[i] + '|' + ' '.join([' ' + str(adjMatrix[i][j]) + ' ' * nameLengths[j] for j in range(n)])

    return s


# This function puts together the whole deal (also returns string)
def printAdjacencyMatrix(filename):
    adjList, names = readInput(filename)
    adjMatrix = adjListToMatrix(adjList)
    s = getHumanReadable(adjMatrix, names)
    print(f'\nAdjacency Matrix for {filename}')
    print(s, end='\n\n')
    return s


# RUN
import glob
import os

if __name__ == '__main__':

    filenames = glob.glob('input/*')
    
    if not os.path.isdir('output'):
        os.mkdir('output')
    
    for filename in filenames:
        s = printAdjacencyMatrix(filename)
        basename = os.path.basename(filename)
        with open(os.path.join('output', basename[:basename.index('.')] + '.out'), 'w') as f:
            f.write(s)
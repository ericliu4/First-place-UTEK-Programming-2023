# This function will take in a filename and output an adjacency list and node names
def read_input(filename):

    with open(filename, 'r') as f:
        line = f.read().strip()

    chunks = line.split(',') # Here each chunk represents one connection (string)

    name_to_index = {}
    names = []
    node_count = 0
    adj_list = []

    for chunk in chunks:

        nodes = chunk.split('->')
        name1 = nodes[0].strip()
        name2 = nodes[1].strip()

        if name1 not in name_to_index:
            name_to_index[name1] = node_count
            node_count += 1
            adj_list.append([])
            names.append(name1)

        if name2 not in name_to_index:
            name_to_index[name2] = node_count
            node_count += 1
            adj_list.append([])
            names.append(name2)
        
        adj_list[name_to_index[name1]].append(name_to_index[name2])
    
    return adj_list, names


# This function will take an adjacency list as input and output an adjacency matrix
def adj_list_to_matrix(adj_list):

    n = len(adj_list)

    adj_matrix = [[0] * n for i in range(n)]

    for i in range(n):
        for dest in adj_list[i]:
            adj_matrix[i][dest] = 1
    
    return adj_matrix


# This function will take an adjacency matrix and node names and output a pretty matrix
def get_human_readable(adj_matrix, names):
    
    name_lengths = list(map(lambda x: len(x), names))
    max_name_length = max(name_lengths)
    name_buffers = list(map(lambda x: max_name_length - x + 1, name_lengths))

    n = len(names)

    s = ' ' * (max_name_length + 1) + '|' + '|'.join([' ' + names[i] + ' ' for i in range(n)])
    s += '\n' + '-' * (max_name_length + 1) + '+' + '-'.join(['-' * (name_lengths[i] + 2) for i in range(n)])
    
    for i in range(n):
        s += '\n' + names[i] + ' ' * name_buffers[i] + '|' + ' '.join([' ' + str(adj_matrix[i][j]) + ' ' * name_lengths[j] for j in range(n)])

    return s


# This function puts together the whole deal
def print_adjacency_matrix(filename):
    adj_list, names = read_input(filename)
    adj_matrix = adj_list_to_matrix(adj_list)
    s = get_human_readable(adj_matrix, names)
    print(f'\nAdjacency Matrix for {filename}')
    print(s, end='\n\n')


# RUN
import glob

if __name__ == '__main__':

    filenames = glob.glob('input/*')
    
    for filename in filenames:
        print_adjacency_matrix(filename)
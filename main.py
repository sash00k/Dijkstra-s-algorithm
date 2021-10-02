#Бочкарев, группа 19213
#Узлы и вершины тут - одно и то же, если что

max_int = 100000 # число, которым изначально обозначим все вершины (кроме стартовой, у нее - 0)

class Node:
    def __init__(self, _index):
        self.index = _index # мы дважды храним index: в элементе класса, и как номер в списке nodes, но так быстрее
        self.is_visited = False # visited = True <=> все пути из узла исследованы
        self.way = [] # массив из индексов узлов, из которых состоит кратчайший путь до узла
        self.way_size = max_int

    def make_visited(self):
        self.is_visited = True

    def set_new_way(self, prev_index):
        new_way = nodes[prev_index].way[:]
        new_way.append(self.index)
        self.way = new_way
        self.way_size = nodes[prev_index].way_size + arr[prev_index][self.index]

    def make_node_starting(self):
        self.way = [self.index]
        self.way_size = 0


def available_nodes(_index): # вернет массив индексов неполностью исследованных доступных вершин
    tmp_avail_nodes = []
    for i in range(size):
        if arr[_index][i] > 0 and not nodes[i].is_visited:
            tmp_avail_nodes.append(i)
    return tmp_avail_nodes

def find_next_starting_node():
    min_index = -1
    min_way_size = max_int
    for node in nodes:
        if node.way_size < max_int and node.way_size < min_way_size and not node.is_visited:
            min_index = node.index
            min_way_size = node.way_size
    return min_index

def nodes_out(): #выведет информацию обо всех узлах (больше для отладки)
    for node in nodes:
        print('Node #'+str(node.index), node.is_visited, node.way_size, node.way, sep = ' ')
    print()

def output(): #выводит ответ
    print('These nodes are reachable from the starting node:')
    for node in nodes:
        if node.is_visited:
            print('#' + str(node.index), end='\t ')
            print('way size =', node.way_size, sep=' ', end='\t')
            print('way =', node.way, sep=' ')

    not_visited = [iterator for iterator in range(size) if nodes[iterator].is_visited == False]
    if len(not_visited) != 0:
        print('These nodes are in another graph component(s):', end=' ')
        print(not_visited)

# читаем матрицу весов или мацтрицу смежности (симметричную, с нулевой диагональю)
size, start_index = input().split()
size, start_index = int(size), int(start_index)
arr = [[int(j) for j in input().split()] for i in range(size)]

# инициализируем списиок узлов графа
nodes = []
for index in range(size):
    nodes.append(Node(index))
# выделяем стартовую вершину
nodes[start_index].make_node_starting()

# собственно, тут сам алгортм Дейкстры
while True:
    curr_start_index = find_next_starting_node()

    if curr_start_index == -1: # если мы не обнаружили ни одной доступной неисследованной вершины
        break # завершаем работу алгоритма

    for curr_node in available_nodes(curr_start_index): # рассмотрим пути во все неисследованные доступные вершины
        # если путь через curr_start_index короче старого, записанного в curr_node
        if nodes[curr_start_index].way_size + arr[curr_start_index][curr_node] < nodes[curr_node].way_size:
            nodes[curr_node].set_new_way(curr_start_index) # запишем предложенный путь в вершину
    # в цикле мы исследовали все пути из curr_start_index, так что отметим ее как исследованную
    nodes[curr_start_index].make_visited()
    # nodes_out() # отладка

output()


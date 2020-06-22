import math
from queue import *


class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    goal = Node('E')  # Represents the goal node for the algorithms.
    start = Node('S')  # Represents the start node of the algorithms.
    visitedlist = []  # for actual_DFS

    def __init__(self, mazeStr, edgeCost=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        cost_count = 0
        self.row_count = 0
        self.column_count = 0
        self.grid = list()
        row = list()
        for symbol in mazeStr:
            if symbol == ',':
                continue
            if symbol == ' ':
                self.row_count += 1
                self.column_count = 0
                self.grid.append(row.copy())
                row.clear()
            else:
                node = Node(symbol)
                node.id = (self.row_count, self.column_count)
                node.gOfN = 0.0
                node.heuristicFn = 1000.0
                node.edgeCost = 1
                if edgeCost:
                    node.edgeCost = edgeCost[cost_count]
                if symbol == 'S':
                    self.start = node
                if symbol == 'G':
                    node.hOfN = 0.0
                    self.goal = node
                row.append(node)
                cost_count += 1
                self.column_count += 1
        self.grid.append(row.copy())
        self.row_count += 1  # for the last row, because there won't be a space
        for n in range(0, self.row_count):
            for m in range(0, self.column_count):
                if n - 1 in range(0, self.row_count):
                    self.grid[n][m].up = self.grid[n - 1][m].id
                if n + 1 in range(0, self.row_count):
                    self.grid[n][m].down = self.grid[n + 1][m].id
                if m - 1 in range(0, self.column_count):
                    self.grid[n][m].left = self.grid[n][m - 1].id
                if m + 1 in range(0, self.column_count):
                    self.grid[n][m].right = self.grid[n][m + 1].id

    # A function to get the children of a certain parent node
    # Takes the parent node and a list of lowercase words of the wanted expansion order
    def get_children(self, parent, order):
        children = list()

        for o in order:
            if o == "up" and parent.up is not None:
                children.append(self.grid[parent.up[0]][parent.up[1]])
            if o == "down" and parent.down is not None:
                children.append(self.grid[parent.down[0]][parent.down[1]])
            if o == "left" and parent.left is not None:
                children.append(self.grid[parent.left[0]][parent.left[1]])
            if o == "right" and parent.right is not None:
                children.append(self.grid[parent.right[0]][parent.right[1]])
        return children

    # A function to get the 1D id from the 2D id.
    def get_1D_idx(self, r, c):
        return r * self.column_count + c

    foundPath = 0

    def actual_dfs(self, current):

        if self.foundPath:
            return self.path, self.fullPath
        currentindex = self.get_1D_idx(current.id[0], current.id[1])
        self.fullPath.append(currentindex)
        if current.value == self.goal.value:
            self.foundPath = 1
            return self.path, self.fullPath

        children = self.get_children(current,
                                     ["up", "left", "left", "left", "up", "up", "right", "up", "up", "up", "right",
                                      "right", "down", "left", "left", "down", "down", "left", "down", "down", "right",
                                      "down", "right", "right"])
        togo = []
        for x in children:
            childindex = self.get_1D_idx(x.id[0], x.id[1])
            if x.value != "#" and childindex not in self.visitedlist:
                self.visitedlist.append(childindex)
                togo.append(x)

        for x in togo:
            self.actual_dfs(x)

    def DFS(self):
        self.fullPath.clear()
        self.visitedlist.append(self.get_1D_idx(self.start.id[0], self.start.id[1]))
        self.actual_dfs(self.start)

        return self.path, self.fullPath

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.path.clear()
        self.fullPath.clear()
        open_q = Queue()
        open_q.put(self.start)
        while not open_q.empty():
            current_node = open_q.get()
            current_index = self.get_1D_idx(current_node.id[0], current_node.id[1])
            if current_index in self.fullPath:
                continue
            self.fullPath.append(current_index)  # self.fullPath = closed list for BFS
            if current_node.value == 'E':
                break
            children = self.get_children(current_node,
                                         ["up", "left", "left", "left", "up", "up", "right", "up", "up", "up", "right",
                                          "right", "down", "left", "left", "down", "down", "left", "down", "down",
                                          "right",
                                          "down", "right", "right"])

            for child_node in children:
                if child_node.value != '#' and child_node.previousNode is None:
                    child_node.previousNode = current_node
                    open_q.put(child_node)

            '''if current_node.up is not None:
                child_node = self.grid[current_node.up[0]][current_node.up[1]]
                if child_node.value != '#' and child_node.previousNode is None:
                    child_node.previousNode = current_node
                    open_q.put(child_node)
            if current_node.down is not None:
                child_node = self.grid[current_node.down[0]][current_node.down[1]]
                if child_node.value != '#' and child_node.previousNode is None:
                    child_node.previousNode = current_node
                    open_q.put(child_node)
            if current_node.left is not None:
                child_node = self.grid[current_node.left[0]][current_node.left[1]]
                if child_node.value != '#' and child_node.previousNode is None:
                    child_node.previousNode = current_node
                    open_q.put(child_node)
            if current_node.right is not None:
                child_node = self.grid[current_node.right[0]][current_node.right[1]]
                if child_node.value != '#' and child_node.previousNode is None:
                    child_node.previousNode = current_node
                    open_q.put(child_node)'''

        goal_index = self.get_1D_idx(self.goal.id[0], self.goal.id[1])
        self.path.append(goal_index)
        current_node = self.goal.previousNode
        while current_node.value != 'S':
            current_index = self.get_1D_idx(current_node.id[0], current_node.id[1])
            self.path.append(current_index)
            current_node = current_node.previousNode
        start_index = self.get_1D_idx(self.start.id[0], self.start.id[1])
        self.path.append(start_index)
        self.path.reverse()
        dummy_path = list()
        return dummy_path, self.fullPath

    def UCS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        # set all nodes to infinity
        self.path.clear()
        self.fullPath.clear()
        self.totalCost = -1

        # set the minimum edge costs to infinity
        for i in range(0, self.row_count):
            for j in range(0, self.column_count):
                self.grid[i][j].gOfN = 1e9

        pq = PriorityQueue()
        visited = list()
        self.grid[0][0].gOfN = 0
        pq.put((0, self.grid[0][0]))
        while not pq.empty():
            tmp = pq.get()
            # current_cost = tmp[0]
            current_node = tmp[1]
            visited.append(current_node)

            if current_node.value == self.goal.value:
                self.totalCost = current_node.gOfN
                '''
                while current_node.previousNode:
                    self.path.append(self.get_1D_idx(current_node.id[0], current_node.id[1]))
                    current_node = current_node.previousNode
                self.path.append(self.get_1D_idx(current_node.id[0], current_node.id[1]))
                self.path.reverse()
                '''
                for n in visited:
                    self.fullPath.append(self.get_1D_idx(n.id[0], n.id[1]))
                break

            # The order of expanding node’s children will be (up, down, left, right).
            children = self.get_children(current_node, ["up", "down", "left", "right"])
            for node in children:
                if node is not None and node.gOfN > node.edgeCost + current_node.gOfN:  # old_minimum > new cost
                    node.gOfN = node.edgeCost + current_node.gOfN  # update the minimum
                    node.previousNode = current_node  # update Parent
                    pq.put((node.gOfN, node))  # push the child in the PQ
                    self.grid[node.id[0]][node.id[1]] = node

        return self.path, self.fullPath, self.totalCost

    def AStarEuclideanHeuristic(self):
        # Cost for a step is calculated based on edge cost of node
        # and use Euclidean Heuristic for evaluating the heuristic value
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes

        self.path.clear()
        self.fullPath.clear()
        self.totalCost = -1

        nodes = list()  # list of unvisited nodes
        visited = list()  # list of visited nodes
        current = self.start  # current node

        nodes.append(current)  # add the current node to the unvisited nodes list
        while nodes:  # while there's still nodes in the Nodes list explore them.
            # get the node with the minimum heuristicFn value in the nodes list.
            current = min(nodes, key=lambda i: i.heuristicFn)
            nodes.remove(current)
            visited.append(current)
            if current == self.goal:
                self.totalCost = current.gOfN
                """
                while Current.previousNode:
                    self.path.append(self.get_1D_idx(Current.id[0], Current.id[1]))
                    Current = Current.previousNode
                self.path.append(self.get_1D_idx(Current.id[0], Current.id[1]))
                self.path.reverse()
                """
                for n in visited:
                    self.fullPath.append(self.get_1D_idx(n.id[0], n.id[1]))

                return self.path, self.fullPath, self.totalCost
            # get the children of the Current node in t he wanted order
            children = self.get_children(current, ["up", "down", "left", "right"])
            for child in children:
                if child in visited or child.value == '#':
                    continue
                if child in nodes:
                    #   if the child node already exists in the nodes list then
                    #   we need to calculate only the new value of g(n) and update it in the list.
                    #   the new value of g(n) comes from the old value +  the penalty of accessing this node.
                    newGOfN = float(current.gOfN) + float(child.edgeCost)
                    if newGOfN < child.gOfN:
                        child.gOfN = newGOfN
                        child.previousNode = current
                else:
                    #   if the child node does not exist in the nodes list then we calculate g(n),
                    #   h(n) by using the Euclidean method h(n) = sqrt((a - c)^2 + (b - d)^2)
                    #   having child.id = (a, b) and goal.id = (c, d).
                    #   and f(n) then add it to the list
                    child.gOfN = current.gOfN + child.edgeCost
                    child.hOfN = math.sqrt(float((child.id[0] - self.goal.id[0]) * (child.id[0] - self.goal.id[0])) +
                                           float((child.id[1] - self.goal.id[1]) * (child.id[1] - self.goal.id[1])))
                    child.heuristicFn = child.gOfN + float(child.hOfN)
                    child.previousNode = current
                    nodes.append(child)

        return self.path, self.fullPath, self.totalCost

    def AStarManhattanHeuristic(self):
        # Cost for a step is 1
        # and use ManhattanHeuristic for evaluating the heuristic value
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes

        self.path.clear()
        self.fullPath.clear()
        self.totalCost = -1

        nodes = list()  # list of unvisited nodes
        visited = list()  # list of visited nodes
        current = self.start  # current node

        nodes.append(current)  # add the current node to the unvisited nodes list
        while nodes:
            # get the node with the minimum heuristicFn value in the nodes list.
            current = min(nodes, key=lambda i: i.heuristicFn)
            nodes.remove(current)
            visited.append(current)
            if current == self.goal:
                self.totalCost = current.gOfN
                """
                while Current.previousNode:
                    self.path.append(self.get_1D_idx(Current.id[0], Current.id[1]))
                    Current = Current.previousNode
                self.path.append(self.get_1D_idx(Current.id[0], Current.id[1]))
                self.path.reverse()
                """
                for n in visited:
                    self.fullPath.append(self.get_1D_idx(n.id[0], n.id[1]))

                return self.path, self.fullPath, self.totalCost

            # get the children of the Current node in t he wanted order
            children = self.get_children(current, ["up", "down", "left", "right"])
            for child in children:
                if child in visited or child.value == '#':
                    continue
                if child in nodes:
                    #   if the child node already exists in the nodes list then
                    #   we need to calculate only the new value of g(n) and update it in the list.
                    #   the new value of g(n) comes from the old value +  the penalty of accessing this node.
                    newGOfN = float(current.gOfN) + float(child.edgeCost)
                    if newGOfN < child.gOfN:
                        child.gOfN = newGOfN
                        child.previousNode = current
                else:
                    #   if the child node does not exist in the nodes list then we calculate g(n),
                    #   h(n) by using the Manhattan method h(n) = abs(a - c) + abs(b - d),
                    #   having child.id = (a, b) and goal.id = (c, d).
                    #   and f(n) then add it to the list
                    child.gOfN = current.gOfN + child.edgeCost
                    child.hOfN = abs(child.id[0] - self.goal.id[0]) + abs(child.id[1] - self.goal.id[1])
                    child.heuristicFn = child.gOfN + float(child.hOfN)
                    child.previousNode = current
                    nodes.append(child)

        return self.path, self.fullPath, self.totalCost


def main():
    searchAlgo = SearchAlgorithms(
        'S,.,.,.,.,.,., ,.,.,.,.,.,.,., ,.,.,.,.,.,.,., ,.,.,.,.,.,.,., ,.,.,G,.,.,.,., ,.,.,.,.,.,.,., ,.,.,.,.,.,.,.')
    path, fullPath = searchAlgo.DFS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

    #######################################################################################

    searchAlgo = SearchAlgorithms(
        'S,.,.,.,.,.,., ,.,.,.,.,.,.,., ,.,.,.,.,.,.,., ,.,.,.,.,.,.,., ,.,.,G,.,.,.,., ,.,.,.,.,.,.,., ,.,.,.,.,.,.,.')
    path, fullPath = searchAlgo.BFS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
    #######################################################################################


'''
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                                  [0, 15, 2, 100, 60, 35, 30, 3
                                      , 100, 2, 15, 60, 100, 30, 2
                                      , 100, 2, 2, 2, 40, 30, 2, 2
                                      , 100, 100, 3, 15, 30, 100, 2
                                      , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.UCS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                                  [0, 15, 2, 100, 60, 35, 30, 3
                                      , 100, 2, 15, 60, 100, 30, 2
                                      , 100, 2, 2, 2, 40, 30, 2, 2
                                      , 100, 100, 3, 15, 30, 100, 2
                                      , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.AStarEuclideanHeuristic()
    print('**ASTAR with Euclidean Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')

    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath, TotalCost = searchAlgo.AStarManhattanHeuristic()
    print('**ASTAR with Manhattan Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')

'''
main()

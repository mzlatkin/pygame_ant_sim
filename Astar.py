import heapq
import time

class Anode():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __hash__(self): 
      return hash((self.position[0], self.position[1]))


class MyHeap(object):
    def __init__(self, initial=None, key=lambda x:x,key2=lambda x:x):
        self.key = key
        self.key2 = key2
        if initial:
            self._data = [(key(item),key2(item),id(item), item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []
    
    def find_node(self, temp_node):
        for i in self._data:
            if i[3] == temp_node:
                return i[3]
    
    def len(self):
        return len(self._data)

    def push(self, item):
        heapq.heappush(self._data, (self.key(item),self.key2(item),id(item), item))

    def pop(self):
        return heapq.heappop(self._data)[3]
    
         

def getf(item):
    return item.f

def getg(item):
    return item.g


def calculate_dist(start, end):
    dist = 0
    position = [start[0],start[1]]
    while position != end:
        update_x = get_dir(position[0], end [0])
        update_y = get_dir(position[1], end [1])

        position[0] += update_x
        position[1] += update_y

        if update_x == 0 or update_y == 0:
            dist += 10
        else:
            dist+=14
    return dist*10

def get_dir(x,y):
    if x < y: return +1
    if x >y: return -1
    if x == y: return 0
            


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    max_itterations = 0
    

    # Create start and end node
    start_node = Anode(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Anode(None, end)
    end_node.g = end_node.h = end_node.f = 100000

    # Initialize both open heap and closed list
    open_heap = MyHeap(None, getf, getg) 
    closed_list = {start_node}
    open_list = {start_node}

    #add start node to open heap
    open_heap.push(start_node)

    ret = []


    while open_heap.len() > 0:

        max_itterations +=1

        # if max_itterations > 1000:
        #     break

        # pop off the node with the lowest f, ties are broken by lowest g, ties are then random

        current_node = open_heap.pop()
        # print(current_node.position)
        
        closed_list.add(current_node) # never need to check this node again
        open_list.add(current_node) # never need to check this node again

        if current_node == end_node: # we are done, return list of path steps
            if current_node.parent is None:
                ret.append(start)
                break
            ret.append(end)
            temp_node = current_node
            while (temp_node.parent != start_node):
                # for i in range(int(maze[temp_node.parent.position[0]][temp_node.parent.position[1]].cost_scale/10)):
                ret.append(temp_node.parent.position)
                
                temp_node = temp_node.parent
            ret.append(start)
            # print(ret)
            break

        children = []

        
        # get all legal children surrounding the current node
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j ==0:
                    continue
                else:
                    if(i == 0 or j ==0):
                        if current_node.position[0] + i >= 0 and current_node.position[0] + i< len(maze) and current_node.position[1] + j >= 0 and current_node.position[1] + j <len(maze[0]):
                            if maze[current_node.position[0] + i][current_node.position[1] + j].diggable:
                                # another check that they are legal children
                                temp_node = Anode(current_node)
                                temp_node.position = [current_node.position[0]+i,current_node.position[1]+j]
                                temp_node.h = calculate_dist(temp_node.position,end_node.position)
                                
                                if i == 0 or j == 0:
                                    temp_node.g = temp_node.parent.g+(100*maze[current_node.position[0] + i][current_node.position[1] + j].cost_scale)
                                else:
                                    temp_node.g = temp_node.parent.g+(140*maze[current_node.position[0] + i][current_node.position[1] + j].cost_scale)

                                temp_node.f = temp_node.g + temp_node.h
                                children.append(temp_node)


                                if temp_node in closed_list:
                                    continue
                                if temp_node in open_list:
                                    open_child = open_heap.find_node(temp_node)
                                    if temp_node.g < open_child.g:
                                        open_child.parent = temp_node.parent
                                        open_child.g = temp_node.g
                                        open_child.f = open_child.g + open_child.h     
                                else:
                                    open_list.add(temp_node)
                                    open_heap.push(temp_node)        
    
    return ret




def main():

    maze = [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = [8, 8]
    end = [0, 0]

    path = astar(maze, start, end)
    # print(path)

    
    # test = [1,2,4,5,6,7,8,2,23,34,45,56,67]
    # heapq.heapify(test)
    # heapq.heappush(test, 2)
    # print(test)

if __name__ == '__main__':
    main()

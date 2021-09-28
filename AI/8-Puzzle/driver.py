"""
Skeleton code for Project 1 of Columbia University's AI EdX course (8-puzzle).
Python 3
"""

import queue as Q
from collections import deque
import time
#import resource
import sys
import math
import psutil
#### SKELETON CODE ####

## The Class that Represents the Puzzle
class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n * n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action        
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):

        for i in range(self.n):
            line = []
            offset = i * self.n

            for j in range(self.n):
                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:
            up_child = self.move_up()

            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, explored, max_depth, time):    
    ### Student Code Goes here
    state.display()
    path = []
    get_path(state,path)
    f = open("output.txt","a")
    f.write("%s: %s\n" % ("path_to_goal",path))
    f.write("%s: %s\n" % ("cost_of_path",len(path)))
    f.write("%s: %s\n" % ("nodes_expanded",explored))
    f.write("%s: %s\n" % ("search_depth",state.cost))
    f.write("%s: %s\n" % ("max_search_depth", max_depth))    
    f.write("%s: %s\n" % ("running_time",time))   
    f.write("%s: %s\n" % ("max_ram_usage",psutil.Process().memory_info().rss / 1024 ** 2))
    f.write("\n")
    f.close()
    print("%s : %s" % ("path_to_goal",path))
    print("%s : %s" % ("cost_of_path",len(path)))
    print("%s : %s" % ("nodes_expanded",explored))
    print("%s : %s" % ("search_depth",state.cost))
    print("%s : %s" % ("max_search_depth", max_depth))    
    print("%s : %s" % ("running_time",time))    
    print("%s : %s" % ("max_ram_usage",psutil.Process().memory_info().rss / 1024 ** 2)) 
                                    # resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    
def get_path(state, path):    
    current_state = state    
    while current_state and current_state.action != "Initial":
        path.append(current_state.action)
        current_state = current_state.parent
    path.reverse()

def bfs_search(initial_state):   
    """BFS search"""

    ### STUDENT CODE GOES HERE ###
    start_time = time.time() 
    frontier = Q.Queue()
    frontier.put(initial_state)
    neighbors = {(initial_state.config)}
    max_depth = explored = 0 
    
    while not frontier.empty():     
        
        state = frontier.get() 
        if state.action != "Initial":
            explored +=1        
        
        if test_goal(state.config):            
            writeOutput(state, explored, max_depth, time.time() - start_time)
            break
                   
        state.expand()
        for c in state.children:
            if c.config not in neighbors:
                frontier.put(c)
                neighbors.add(c.config)                
                if max_depth < c.cost:
                    max_depth = c.cost 
    print("----------BFS Search Ends-------------\n")
    
def dfs_search(initial_state):    
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    frontier = deque()
    frontier.append(initial_state)
    neighbors = {(initial_state.config)}
    max_depth = explored = 0    
    while frontier: 
        state = frontier.pop() 

        if state.action != "Initial":
            explored +=1        

        if test_goal(state.config):              
            writeOutput(state, explored, max_depth, time.time() - start_time)            
            break            
                   
        state.expand()                      
        while state.children:
            c = state.children.pop()                
            if c.config not in neighbors:
                frontier.append(c)
                neighbors.add(c.config)                 
                if max_depth < c.cost:
                    max_depth = c.cost    
                    
    print("----------DFS Search Ends-------------\n")    

def A_star_search(initial_state):    
    """A * search"""

    ### STUDENT CODE GOES HERE ###
    start_time = time.time() 
    frontier = [initial_state]    
    neighbors = {(initial_state.config)}
    max_depth = explored = 0 
    total_cost = []
    while frontier:
        if total_cost:
            explored +=1
            min_position = total_cost.index(min(total_cost))
            state = frontier.pop(min_position)
            del total_cost[min_position]
        else:
            state = frontier.pop()
        
        if test_goal(state.config):
            writeOutput(state, explored, max_depth, time.time() - start_time)
            break
        
        state.expand() 
        for c in state.children:
            if c.config not in neighbors:                
                frontier.append(c)
                neighbors.add(c.config)
                total_cost.append(calculate_total_cost(c) + state.cost)                               
                if max_depth < c.cost:
                    max_depth = c.cost 
        
    print("----------A* Search Ends-------------\n")


def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###
    #h1 = 0
    h2 = i = 0  
    for value in state.config:        
        if value != 0 and i != value:
            #h1 += 1 # misplaced tile
            h2 += calculate_manhattan_dist(i,value,state.n)
        i += 1
    return h2 #if h2 > h1 else h1

def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""
    
    ### STUDENT CODE GOES HERE ###
    return abs(value // n - idx // n) + abs(value % n - idx % n)    
    

def test_goal(puzzle_state):

    """test the state is the goal state or not"""

    ### STUDENT CODE GOES HERE ###
    i = 0
    for s in puzzle_state:
        if s != i:
            return False
        i += 1
    return True
    

# Main Function that reads in Input and Runs corresponding Algorithm
def main():

    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
    
    if sm == "bfs":
        bfs_search(hard_state)

    elif sm == "dfs":
        dfs_search(hard_state)

    elif sm == "ast":
        A_star_search(hard_state)

    else:
        print("Enter valid command arguments !")

if __name__ == '__main__':
    main()


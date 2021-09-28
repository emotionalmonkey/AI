import numpy as np
import sys
import itertools

class CSP():
    def __init__(self,grid): 
        self.grid = grid
        self.size = len(grid)
        self.section = int((self.size) ** 0.5)
        self.d = set(range(1,self.size + 1))        
        self.constraints, self.possible_values, self.binary_constraints = self.initial_configuration()  

    def initial_configuration(self):
        constraints_list = dict()
        possible_list = dict()
        binary_constraints = set()
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 0: 
                    possible_values = set()    
                    
                    rw = row - (row % self.section)
                    cl = col - (col % self.section)

                    # possible values for empty cell
                    row_values = set(self.grid[row])
                    col_values = set(self.grid[:,col])
                    square_values = set(self.grid[rw:rw + self.section,cl:cl + self.section].flatten())
                    possible_values = self.d - row_values - col_values - square_values 

                    if not possible_values: 
                        possible_values = self.d

                    row_constraints = set()
                    col_constraints = set()
                    for i in range(self.size):
                        if grid[row][i] == 0: 
                            # row constraints
                            row_constraints.add(str(row) + str(i))
                        if grid[i][col] == 0: 
                            # column constraints
                            col_constraints.add(str(i) + str(col))    
                    
                    square_constraints = set()
                    for i in range(rw,rw + self.section):
                        for j in range(cl,cl + self.section):
                            if grid[i][j] == 0: 
                                # square constraints
                                square_constraints.add(str(i) + str(j))
                    
                    binary_constraints = binary_constraints | self.generate_binary_constraints(row_constraints) | self.generate_binary_constraints(col_constraints) | self.generate_binary_constraints(square_constraints)
                    constraints_list[str(row) + str(col)] = row_constraints | col_constraints | square_constraints
                    possible_list[str(row) + str(col)] = possible_values

        return constraints_list, possible_list, binary_constraints
        
    def generate_binary_constraints(self, constraint_set):
        binary_constraints = set()
        for x in itertools.permutations(constraint_set,2):
            binary_constraints.add(x) 
        return binary_constraints

class AC3():
    def __init__(self,csp): 
        self.csp = csp      
        self.possible_values = csp.possible_values
    def play(self): 
        queue = self.csp.binary_constraints
        #x = len(queue)
        while queue:            
            (Xi, Xj) = queue.pop()            
            if self.revise(Xi, Xj): 

                # no solution if no possibile value left
                if len(self.possible_values[Xi]) == 0:
                    return False
            
                for Xk in self.csp.constraints[Xi]:
                    if Xk != Xi:
                        queue.add((Xk, Xi))
        
        result_grid = self.csp.grid.copy()
        for cell,v in self.possible_values.items():  
            if len(v) > 1:
                return False
            row, col = np.array(list(cell), dtype=int)
            result_grid[row][col] = v.pop()       
            
        self.csp.grid = result_grid
        #print(result_grid)
        return True

    def revise(self, Xi, Xj):        
        list_to_remove = []
        for value_i in self.possible_values[Xi]:            
            
            if all([value_i == value_j for value_j in self.possible_values[Xj]]):
                list_to_remove.append(value_i)
        
        for x in list_to_remove:
            self.possible_values[Xi].remove(x)            
        
        return any(list_to_remove)

class BTS:
    def __init__(self,csp): 
        self.csp = csp   
        self.empty_cells = [(int(cell[0]),int(cell[1])) for cell in sorted(self.csp.possible_values, key=lambda value: len(self.csp.possible_values[value]))]
        #self.empty_cells = {(int(cell[0]),int(cell[1])) for cell in
        #self.csp.possible_values}
    def play(self,initial=False):        
        available_cells = self.initialize_empty_cell() if initial else self.has_empty_cell()
        if not available_cells: # all cells are filled
            return True    
       
        cell = sorted(available_cells, key=lambda value: len(available_cells[value]))[0]
        values = available_cells[cell]
        if len(values) < self.csp.size : # check constraint
            row, col = np.array(list(cell), dtype=int)
            for num in values:
                self.csp.grid[row][col] = num
            
                if self.play():
                    return True

                self.csp.grid[row][col] = 0

        return False
    
    def initialize_empty_cell(self):
        available_cells = dict()       
        for row, col in self.empty_cells: 
            possible_values = self.csp.possible_values[str(row) + str(col)] 
            if len(possible_values) == 1: # exact location
                self.csp.grid[row][col] = possible_values.pop()
            else:
                if len(possible_values) == 2: #return as two possible values is the least constraint at initial
                    return {str(row) + str(col): possible_values} 
                available_cells[str(row) + str(col)] = possible_values                    
        return available_cells

    def has_empty_cell(self):
        available_cells = dict()       
        for row, col in self.empty_cells:            
            if grid[row][col] == 0: 
                possible_values = self.check_constraints(row,col)
                if possible_values:
                    if len(possible_values) == 1: #return as 1 is the min constraint
                        return {str(row) + str(col): possible_values}  
                    available_cells[str(row) + str(col)] = possible_values

        return available_cells

    def check_constraints(self,row,col):   
        rw = row - (row % self.csp.section)
        cl = col - (col % self.csp.section)    
        row_values = set(self.csp.grid[row])
        col_values = set(self.csp.grid[:,col])
        square_values = set(grid[rw:rw + self.csp.section,cl:cl + self.csp.section].flatten())    

        possible_values = self.csp.d - row_values - col_values - square_values 
        return possible_values if possible_values else self.csp.d    


def format_grid(grid,method):
    f = open("output.txt","a")
    f.write(str(grid).replace(" ","").replace("\n","").replace("[","").replace("]","") + method + "\n")
    f.close()

import time
import os
if __name__ == '__main__':   
    # update - 02/08/2021 - the Last submission
    start = time.process_time()
    txt = list(str("500068000000000060042050000000800900001000040903000620700001009004200003080000000").replace("'","").replace('"',"").replace(" ",""))
    #txt =
    list(str("500068000000000060042050000000800900001000040903000620700001009004200003080000000").replace("'","").replace('"',"").replace(" ",""))
    n=int(len(txt)**0.5)
    grid = np.array(list(txt), dtype=int).reshape(n,n)
    csp = CSP(grid)
    ac3 = AC3(csp)
    if ac3.play():
        format_grid(csp.grid," AC3")
    else:
        bts = BTS(csp)
        format_grid(csp.grid," BTS") if bts.play(True) else print("No solution found!")
    print(grid)

    #f = open(os.path.join(os.path.dirname(__file__),"sudokus_start.txt"),"r")
    #count = 0
    #for line in f:
    #    start_game = time.process_time()
    #    txt = line.split("\n")[0]
    #    print(txt)
    #    grid = np.array(list(txt), dtype=int).reshape(9,9)
    #    csp = CSP(grid)
    #    ac3 = AC3(csp)
    #    if ac3.play():
    #        print(str(csp.grid) + " AC3")
    #    else:
    #        bts = BTS(csp)
    #        print(str(csp.grid) + " BTS") if bts.play(True) else print("No solution found!")
        
        
    #    print("Time : ",end="")
    #    print(time.process_time() - start_game)

    #    count+=1
    #    if count == 20:
    #        break
    #f.close()
    #print(time.process_time() - start)
 #003020600900305001001806400008102900700000008006708200002609500800203009005010300 this gets me zero       
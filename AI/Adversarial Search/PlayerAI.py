from BaseAI import BaseAI
import numpy as np
import time
import math

class PlayerAI(BaseAI):
    def __init__(self):
        self.startTime = time.process_time()

    def getMove(self, grid):   
        self.startTime = time.process_time()
        cellCount = len(grid.getAvailableCells())
        depth =  3 if cellCount > 8 else (4 if cellCount > 4 else 5)
        (child, _) = self.maximize(grid, -1, float('inf'), depth)        
        #print(depth)
        return child
    
    def isInTime(self):
        return time.process_time() - self.startTime < 0.18

    def getScore(self, state):
        total = count = mono = seq = max_val = 0    
        i = j = -1 # max_val index
        map = np.array(state.map)
        for x in range(state.size):

            # monotonic rows - values are either increasing or decreasing along UP/DOWN or LEFT/RIGHT directions
            diff_row = np.diff(map[x])
            mono += np.all(diff_row<=0) or np.all(diff_row>=0)        
            diff_col = np.diff(map[:,x])
            mono += np.all(diff_col<=0) or np.all(diff_col>=0)

            for y in range(state.size): 
                val = map[x][y]
                total += val 
                count += val > 0 

                # same value in adjacent cell
                # note - just count for previous adjacent cell value so as to avoid duplication       
                if (x > 0 and val == map[x - 1][y]):
                    # cell weight (1% of cell value) + constant 0.2 for having same value 
                    seq += (0.01 * val) + 0.2            
                if (y > 0 and val == map[x][y - 1]):
                    seq += (0.01 * val) + 0.2
            
                #max_val = max(max_val,val)
                if val > max_val:
                    max_val = val
                    i = x
                    j = y
                elif val > 0 and val == max_val:
                   if (not i in (0,3) and not j in (0,3)) or (x in (0,3) and y in (0,3)):
                        i = x
                        j = y

        # monotonic rows + Avg + same value in adjacent cell + available empty cells + having max_val in corner(2) or edge(1)
        return mono + math.log2(total / count) + seq + (16-count) + (2 if i in (0,3) and j in (0,3) else 1 if i in (0,3) or j in (0,3) else 0)

    def maximize(self, state, alpha, beta, depth):        
        if depth == 0 or not self.isInTime():
            return None, self.getScore(state)

        (maxChild, maxScore) = (None, -1)

        moves = state.getAvailableMoves()
        if not moves: #state.canMove(moves):
            return None, self.getScore(state)

        # change the order to UP, LEFT, DOWN, RIGHT as UP and DOWN or LEFT and RIGHT directions usually tend to have same heuristic
        moves.sort(key=(lambda a: a%2))

        for child in moves: 
            childState = state.clone() 
            childState.move(child)
        
            (_, score) = self.minimize(childState, alpha, beta, depth-1)

            if score > maxScore:
                (maxChild, maxScore) = (child, score)
            if maxScore >= beta:
                break
            if maxScore > alpha:
                alpha = maxScore

        return (maxChild, maxScore)

    def minimize(self, state, alpha, beta, depth):
        cells = state.getAvailableCells() 

        if depth == 0 or not cells or not self.isInTime():
            return None, self.getScore(state)

        (minChild, minScore) = (None, float('inf'))
        
        for child in cells:
            childState = state.clone()
            childState.setCellValue(child,2)
 
            (_, score) = self.maximize(childState, alpha, beta, depth-1)

            if score < minScore:
                (minChild, minScore) = (child, score)
            if minScore <= alpha:
                break
            if minScore < beta:
                beta = minScore

        return (minChild, minScore)


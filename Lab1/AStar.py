from copy import deepcopy
import time
import argparse
import heapq

MANHATTAN = False
WRONG_POSITION = False
AVARAGE = False

H_coefficient = 1
G_coefficient = 1

def calculateHeuristic(matrix):
    if MANHATTAN:
            return manhattan(matrix)
    elif WRONG_POSITION:
            return wrongPosition(matrix)
    elif AVARAGE:
            return (manhattan(matrix) + wrongPosition(matrix))/2

# wrong position heuristic
def wrongPosition(matrix):
    x = 1
    heuristic = 0
    for i in range(3):
        for j in range(3):
            if matrix[i][j] != x % 9:
                heuristic += 1
            x += 1
    return heuristic

# Manhattan distance
def manhattan(matrix):
    heuristic = 0
    for i in range(3):
        for j in range(3):
            if matrix[i][j] != 0:
                heuristic += abs(i - (matrix[i][j]-1)//3) + \
                    abs(j - (matrix[i][j]-1) % 3)
    return heuristic



class NodeObj:
    matrix = [[0 for i in range(3)] for j in range(3)]
    parentNode = None
    gScore = None
    heuristic = 0

    def __init__(self, values, gScore=None, parentNode=None):
        self.matrix = values
        self.gScore = gScore
        self.parentNode = parentNode
        self.heuristic = calculateHeuristic(values)

    def getGScore(self):
        return self.gScore
    
    def setGScore(self, gScore):
        self.gScore = gScore

    def hasParent(self):
        return self.parentNode != None

    def getMatrix(self):
        return self.matrix
    
    def getHeuristic(self):
        return self.heuristic
    
    def getFScore(self):
        return self.heuristic*H_coefficient + self.gScore*G_coefficient
    
    def printNode(self):
        for i in range(3):
            for j in range(3):
                print(self.matrix[i][j], end=" ")
            print()
    
    def __eq__(self, other):

        if other == None:
            return False
        
        if self.getHeuristic() != other.getHeuristic():
            return False
        
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != other.getMatrix()[i][j]:
                    return False
                    
        return True
    
    def __lt__(self, other):
        if self.getFScore() == other.getFScore():
            return self.getGScore() < other.getGScore()
        return self.getFScore() < other.getFScore()
    



def children(node):
    children = []
    nodeMatrix = node.getMatrix()
    for i in range(3):
        for j in range(3):
            if nodeMatrix[i][j] == 0:
                if i > 0:
                    newMatrix = deepcopy(nodeMatrix)
                    newMatrix[i][j] = newMatrix[i-1][j]
                    newMatrix[i-1][j] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))
                if i < 2:
                    newMatrix = deepcopy(nodeMatrix)
                    newMatrix[i][j] = newMatrix[i+1][j]
                    newMatrix[i+1][j] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))
                if j > 0:
                    newMatrix = deepcopy(nodeMatrix)
                    newMatrix[i][j] = newMatrix[i][j-1]
                    newMatrix[i][j-1] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))
                if j < 2:
                    newMatrix = deepcopy(nodeMatrix)
                    newMatrix[i][j] = newMatrix[i][j+1]
                    newMatrix[i][j+1] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))                

    return children




def AStar(first):

    frontier = []
    explored = []
    
    goal = NodeObj([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    heapq.heappush(frontier, first)

    print("\nA* algorithm is running...")
    start = time.time()

    while frontier:

        try:        
            current = heapq.heappop(frontier)
            explored.append(current)

            print("Node explored:", len(explored), "--- Time elapsed:", round(time.time() - start, 3), end="\r")
            
            if current == goal:
                goal = current
                print("\n\n=========================================")
                print("Goal reached!")
                print("Step needed to reach solution:", goal.getGScore())
                print("=========================================\n")
                break
            else:
                for child in children(current):
                    if child not in explored and child not in frontier:
                        heapq.heappush(frontier, child)

                    # if child in explored:
                    #     continue
                    
                    # try:
                    #     index = frontier.index(child)
                    #     if frontier[index].getGScore() < child.getGScore():
                    #         continue
                    # except:
                    #     pass

                    # heapq.heappush(frontier, child)

        except KeyboardInterrupt:
                print("\n\nUser stopped the program. Printing the first 10 explored nodes: \n")  
                i = 0
                for i in range(0,10, 1):
                    explored.pop().printNode()
                    print()
                break        


    if goal.hasParent() == False:
        print("No solution found")
        return
    
    end = time.time()
    print("Time needed to find solution:", end - start, "seconds")

    r = input("\nTraceback? (Y/n): ")
    if r != "n" and r != "N":
        print()
        while goal.hasParent():
            goal.printNode()
            print("move:", goal.getGScore(), "\n")
            goal = goal.parentNode
        goal.printNode()
        print("starting node")               
    



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="select mode", type=str, default=None)
    parser.add_argument("-t", "--test", help="select case text", type=int, default=0)
    parser.add_argument("-hc", "--h_coefficient", help="set h coefficient", type=float, default=1)

    args = parser.parse_args()

    match args.mode:
        case "m":
            print("\nUSING MANHATTAN DISTANCE AS HEURISTIC VALUE")
            MANHATTAN = True
        case "w":
            print("\nUSING WRONG POSITION HEURISTIC")
            WRONG_POSITION = True
        case "a":
            print("\nUSING AVERAGE OF MANHATTAN DISTANCE AND WRONG POSITION HEURISTIC")
            AVARAGE = True
        case _:
            MANHATTAN = True

    if args.h_coefficient != 1:
        print("\nUSING H COEFFICIENT:", args.h_coefficient)
        H_coefficient = args.h_coefficient

    match args.test:
        case 1:
            print("\nUSING FIRST CASE")
            first = NodeObj([[4, 1, 3], [7, 2, 6], [0, 5, 8]], 0) # 6 moves
        case 2:
            print("\nUSING SECOND CASE")
            first = NodeObj([[7, 2, 4], [5, 0, 6], [8, 3, 1]], 0) # 20 moves
        case 3:
            print("\nUSING THIRD CASE")
            first = NodeObj([[6, 4, 7], [8, 5, 0], [3, 2, 1]], 0) # 31 moves "Tabish"
        case 4:
            print("\nUSING FOURTH CASE")
            first = NodeObj([[8, 6, 7], [2, 5, 4], [3, 0, 1]], 0) # 31 moves "Tabish"
        case _:
            print("\nUSING CUSTOM STARTING NODE")
            matrix = input("Insert a starting node with spaces: ")
            matrix = matrix.split()
            matrix = [int(i) for i in matrix]
            matrix = [matrix[i:i+3] for i in range(0, len(matrix), 3)]
            first = NodeObj(matrix, 0) # 0 moves
        
    #print("Start from node:")
    first.printNode()


    AStar(first)
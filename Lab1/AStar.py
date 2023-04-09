from copy import deepcopy
import time
import argparse

manhattan = False

class NodeObj:

    matrix = [[0 for i in range(3)] for j in range(3)]
    parentNode = None
    gScore = None
    h1 = 0

    def __init__(self, values, gScore=None, parentNode=None):
        self.matrix = values
        self.gScore = gScore
        self.parentNode = parentNode
        if (manhattan):
            self.manhattan()
        else:
            self.wrongPosition()


    def wrongPosition(self):
        x = 1
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != x%9:
                    self.h1 += 1
                x += 1
        self.h1 *= 3

    # Manhattan distance
    def manhattan(self):
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != 0:
                    self.h1 += abs(i - (self.matrix[i][j]-1)//3) + abs(j - (self.matrix[i][j]-1)%3)
        #self.h1 *= 2

    def getGScore(self):
        return self.gScore
    
    def hasParent(self):
        return self.parentNode != None

    def getMatrix(self):
        return self.matrix
    
    def getFScore(self):
        return self.gScore + self.h1
    
    def getH1(self):
        return self.h1
    
    def printNode(self):
        for i in range(3):
            for j in range(3):
                print(self.matrix[i][j], end=" ")
            print()
    
    def __eq__(self, other):
        if other == None:
            return False
        
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != other.getMatrix()[i][j]:
                    return False
        return True
    


def children(node):
    children = []
    for i in range(3):
        for j in range(3):
            if node.getMatrix()[i][j] == 0:
                if i > 0:
                    newMatrix = deepcopy(node.getMatrix())
                    newMatrix[i][j] = newMatrix[i-1][j]
                    newMatrix[i-1][j] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))
                if i < 2:
                    newMatrix = deepcopy(node.getMatrix())
                    newMatrix[i][j] = newMatrix[i+1][j]
                    newMatrix[i+1][j] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))
                if j > 0:
                    newMatrix = deepcopy(node.getMatrix())
                    newMatrix[i][j] = newMatrix[i][j-1]
                    newMatrix[i][j-1] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))
                if j < 2:
                    newMatrix = deepcopy(node.getMatrix())
                    newMatrix[i][j] = newMatrix[i][j+1]
                    newMatrix[i][j+1] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1, node))                

    return children


def AStar(first):

    forntier = []
    explored = []
    
    goal = NodeObj([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    print("Start from node:")
    first.printNode()

    forntier.append(first)

    print("\nA* algorithm is running...")
    start = time.time()

    while len(forntier) > 0:
            current = forntier.pop(0)
            explored.append(current)
            
            if current == goal:
                goal = current
                print("\n=========================================")
                print("Goal reached!")
                print("Step needed to reach solution:", goal.getGScore())
                print("=========================================\n")
                break
            else:
                for child in children(current):
                    if child not in explored:
                        forntier.append(child)
                    # if child in forntier:
                    #     for node in forntier:
                    #         if node == child:
                    #             if node.getGScore() > child.getGScore():
                    #                 node = child
                    #                 break
                
                forntier.sort(key=lambda x: x.getFScore())

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
    parser.add_argument("-m", "--manhattan", help="use manhattan distance", action="store_true")
    parser.add_argument("-2", "--second", help="second case with 20 move", action="store_true")
    parser.add_argument("-3", "--third", help="third case with 31 move", action="store_true")
    parser.add_argument("-4", "--fourth", help="fourth case with 31 move", action="store_true")
    parser.add_argument("-5", "--fifth", help="fifth case with ? move", action="store_true")
    parser.add_argument("-6", "--sixth", help="sixth case with ? move", action="store_true")

    args = parser.parse_args()

    if args.manhattan:
        print("\nUSING MANHATTAN DISTANCE AS HEURISTIC VALUE")
        manhattan = True
    else:
        print("\nUSING WRONG POSITION HEURISTIC")
        manhattan = False

    if args.second:
        print("\nUSING SECOND CASE")
        first = NodeObj([[7, 2, 4], [5, 0, 6], [8, 3, 1]], 0) # 20 moves
    elif args.third:
        print("\nUSING THIRD CASE")
        first = NodeObj([[2, 8, 1], [0, 4, 3], [7, 6, 5]], 0) # 31 moves
    elif args.fourth:
        print("\nUSING FOURTH CASE")
        first = NodeObj([[5, 6, 7], [4, 0, 8], [3, 2, 1]], 0) # 31 moves
    elif args.fifth:
        print("\nUSING FIFTH CASE")
        first = NodeObj([[6, 4, 7], [8, 5, 0], [3, 2, 1]], 0) # ? moves
    elif args.sixth:
        print("\nUSING SIXTH CASE")
        first = NodeObj([[8, 6, 7], [2, 5, 4], [3, 0, 1]], 0) # ? moves 
    else:
        print("\nUSING FIRST CASE")
        first = NodeObj([[4, 1, 3], [7, 2, 6], [0, 5, 8]], 0)  # 6 moves
        


    AStar(first)
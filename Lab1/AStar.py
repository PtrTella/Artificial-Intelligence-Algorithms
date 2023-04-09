from copy import deepcopy

class NodeObj:

    matrix = [[0 for i in range(3)] for j in range(3)]
    gScore = None
    h1 = 0
    

    def __init__(self, values, gScore=None):
        self.matrix = values
        self.gScore = gScore
        self.setH1()


    def setH1(self):
        x = 1
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != x%9:
                    self.h1 += 1
                x += 1
        self.h1 *= 3

    def getGScore(self):
        return self.gScore

    def getMatrix(self):
        return self.matrix
    
    def getFScore(self):
        return self.gScore + self.h1
    
    def getH1(self):
        return self.h1
    
    def printNode(self):
        print()
        for i in range(3):
            for j in range(3):
                print(self.matrix[i][j], end=" ")
            print()
        print()
    

    
    def __eq__(self, other):
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
                    children.append(NodeObj(newMatrix, node.getGScore()+1))
                if i < 2:
                    newMatrix = deepcopy(node.getMatrix())
                    newMatrix[i][j] = newMatrix[i+1][j]
                    newMatrix[i+1][j] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1))
                if j > 0:
                    newMatrix = deepcopy(node.getMatrix())
                    newMatrix[i][j] = newMatrix[i][j-1]
                    newMatrix[i][j-1] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1))
                if j < 2:
                    newMatrix = deepcopy(node.getMatrix())
                    newMatrix[i][j] = newMatrix[i][j+1]
                    newMatrix[i][j+1] = 0
                    children.append(NodeObj(newMatrix, node.getGScore()+1))                

    return children
    

def AStar():

    forntier = []
    explored = []

    goal = NodeObj([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    #first = NodeObj([[4, 1, 3], [7, 2, 6], [0, 5, 8]], 0)  # 6 moves
    first = NodeObj([[7, 2, 4], [5, 0, 6], [8, 3, 1]], 0) # 20 moves

    print("start from node:")
    first.printNode()

    forntier.append(first)

    print("A* algorithm is running...")
    while len(forntier) > 0:
            current = forntier.pop(0)
            explored.append(current)
            if current == goal:
                goal = current
                print("\nGoal reached!\n")
                print("Step needed to reach solution:", goal.getGScore())
                goal.printNode()
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



    r = input("\nTraceback? y/N")
    if r == "y":
        explored.sort(key=lambda x: x.getFScore())
        path = explored[0 : goal.getGScore()]
        path.sort(key=lambda x: x.getGScore(), reverse=True)

        print("\ntraceback:")
        for node in path :
            node.printNode()
            print("gScore:", node.getGScore())
            if node == first:
                break

    
               
    

if __name__ == "__main__":
    AStar()
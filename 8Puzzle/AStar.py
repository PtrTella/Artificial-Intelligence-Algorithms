from queue import PriorityQueue
import time

# Dictionary with the possible moves and the opposite of the move
possibleMoves = {
        'up': (-3, 'down'),
        'down': (3, 'up'),
        'left': (-1, 'right'),
        'right': (1, 'left')
}

# Calculate the Manhattan distance based on [1, 2, 3, 4, 5, 6, 7, 8, 0]
def manhattan_distance(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            x, y = divmod(i, 3)
            x_goal, y_goal = divmod(tile-1, 3)
            distance += abs(x - x_goal) + abs(y - y_goal)
    return distance

# Calculate the number of tiles in the wrong position based on [1, 2, 3, 4, 5, 6, 7, 8, 0]
def wrong_position(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0 and tile != i+1:
            distance += 1
    return distance


class Node:
    def __init__(self, state, parent, move, depth, cost):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost
    


class Puzzle:

    def __init__(self, initial_state, mode="m"):
        self.mode = mode
        self.start_node = Node(initial_state, None, None, 0, 0)
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    # Generate the children nodes of the given node
    def get_children(self, node):

        children = []
        # Find the position of the blank tile (0)
        blank_pos = node.state.index(0)

        # Generate the possible moves given by the dictionary possibleMoves
        for move, (offset, opposite) in possibleMoves.items():

            new_pos = blank_pos + offset     # Calculate the position of the tile to be moved

            # Check if it is not the opposite of the last move (to avoid the same moves in a loop)
            # If it is the first Node, the last move is None so it is not necessary to check (opposite != None)
            if (opposite != node.move):

                # Check if the move is valid (inside vector 0-8) and if it is not the opposite of the last move
                if (move == "up") and (new_pos < 0):
                    continue
                if (move == "down") and (new_pos > 8):
                    continue
                if (move == "left") and (new_pos%3 == 2):
                    continue
                if (move == "right") and (new_pos%3 == 0):
                    continue

                # Create a new state by swapping the blank tile with the tile to be moved
                new_state = node.state[:]  # Copy the current state
                new_state[blank_pos], new_state[new_pos] = new_state[new_pos], new_state[blank_pos] # Swap the tiles

                # Calculate the heuristic value with the selected mode
                h = self.heuristic(new_state)

                # Create a new node and add it to the children list
                child_node = Node(new_state, node, move,
                                    node.depth+1, node.depth+1+h)
                children.append(child_node)    
        return children

    # select Heuristic function
    def heuristic(self, state):
        if self.mode == "w":                                     
            return wrong_position(state)
        else:                                           
            return manhattan_distance(state)
        

    # Solve the puzzle
    def solve(self):
        
        # Using a priority queue to store the nodes is faster to get the node with the lowest cost
        pq = PriorityQueue()
        pq.put(self.start_node)

        # Using a set to store the visited states is faster than using a list when need to check if a state is visited
        visited = set()
        
        while not pq.empty():
            node = pq.get()
            if node.state == self.goal_state:
                moves = []
                while node.parent is not None:
                    moves.append(node.move)
                    node = node.parent
                return moves[::-1]
            visited.add(tuple(node.state))
            for child in self.get_children(node):
                if tuple(child.state) not in visited:
                    pq.put(child)
        return [("No solution found")]


if __name__ == '__main__':

    # Read the initial state from the user
    initial_state = input("Enter the initial state with spaces: ")
    initial_state = initial_state.strip().split()
    
    # Check if the input is valid
    try:
        if len(initial_state) != 9:
            raise ValueError
        else :
            check = [int(i) for i in range(9)]
            for i in initial_state:
                if int(i) not in check:
                    raise ValueError
                else :
                    check.remove(int(i))
        initial_state = [int(i) for i in initial_state]
    except:
        print("Invalid input")
        exit()
    

    # Read the mode from the user
    mode = input("Enter the mode (m for Manhattan distance, w for wrong position) [default m]: ")
    mode = mode.lower().strip()

    puzzle = Puzzle(initial_state, mode)        
    
    print("\nSolving puzzle...")
    start = time.time()
    moves = puzzle.solve()
    print("\nTime: ", time.time() - start)    
    print("\nPath length: ", len(moves), "\n\nMoves: ", moves)
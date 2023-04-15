from queue import PriorityQueue
import time


mode = {
    "m": "MANHATTAN",
    "w": "WRONG_POSITION",
}


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

    possibleMoves = {
        'up': (-3, 'down'),
        'down': (3, 'up'),
        'left': (-1, 'right'),
        'right': (1, 'left')
    }

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def get_children(self, node):

        children = []
        # Find the position of the blank tile (0)
        blank_pos = node.state.index(0)

        # Generate the possible moves
        for move, (offset, opposite) in self.possibleMoves.items():

            new_pos = blank_pos + offset     # Calculate the position of the tile to be moved
            #check = blank_pos%3 + offset
            #print(check)

            # Check if it is not the opposite of the last move and if it is not the first move
            if (opposite != node.move or node.depth == 0):

                # Check if the move is valid (inside vector 0-8) and if it is not the opposite of the last move
                if (move == "up") and (new_pos < 0):
                    continue
                if (move == "down") and (new_pos > 8):
                    continue
                if (move == "left") and (new_pos%3 == 2):
                    continue
                if (move == "right") and (new_pos%3 == 0):
                    continue

                #print("move: ", move)
                        # Create a new state by swapping the blank tile with the tile to be moved
                new_state = node.state[:]
                new_state[blank_pos], new_state[new_pos] = new_state[new_pos], new_state[blank_pos]

                    # Calculate the heuristic
                h = self.heuristic(new_state)

                    # Create a new node and add it to the children list
                child_node = Node(new_state, node, move,
                                    node.depth+1, node.depth+1+h)
                children.append(child_node)

                
        return children

    # select Heuristic function
    def heuristic(self, state):
        if mode == "m":                             # mode == "MANHATTAN"               
            return self.manhattan_distance(state)
        else:                                       # mode == "WRONG_POSITION"
            return self.wrong_position(state)
        

    # Calculate the Manhattan distance
    def manhattan_distance(self, state):
        distance = 0
        for i, tile in enumerate(state):
            if tile != 0:
                x, y = divmod(i, 3)
                x_goal, y_goal = divmod(tile-1, 3)
                distance += abs(x - x_goal) + abs(y - y_goal)
        return distance

    # Calculate the number of tiles in the wrong position
    def wrong_position(self, state):
        distance = 0
        for i, tile in enumerate(state):
            if tile != 0 and tile != i+1:
                distance += 1
        return distance

    def solve(self):
        start_node = Node(self.initial_state, None, None, 0, 0)
        pq = PriorityQueue()
        pq.put(start_node)
        visited = set()
        moves = []
        while not pq.empty():
            node = pq.get()
            if node.state == self.goal_state:
                while node.parent is not None:
                    moves.append(node.move)
                    node = node.parent
                return moves[::-1]
            visited.add(tuple(node.state))
            for child in self.get_children(node):
                if tuple(child.state) not in visited:
                    pq.put(child)
        return None


if __name__ == '__main__':

    # Read the initial state from the user
    initial_state = input("Enter the initial state: ")
    initial_state = initial_state.split()
    initial_state = [int(i) for i in initial_state]
    puzzle = Puzzle(initial_state)

    # Read the mode from the user
    mode = input("Enter the mode (m for Manhattan distance, w for wrong position) [default w]: ")
    mode = mode.lower()
    mode = mode.strip()

    print("\nSolving puzzle...")
    start = time.time()
    moves = puzzle.solve()
    print("\nTime: ", time.time() - start)    
    print("\nPath length: ", len(moves), "\n\nMoves: ", moves) 

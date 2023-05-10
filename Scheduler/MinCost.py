import random

# Define the classes and rooms
# List of classes to schedule
classes = ['MT101', 'MT102', 'MT103', 'MT104', 'MT105', 'MT106', 'MT107', 'MT201', 'MT202', 'MT203', 'MT204', 'MT205', 'MT206', 'MT301', 'MT302', 'MT303', 'MT304', 'MT401', 'MT402', 'MT403', 'MT501', 'MT502']

# List of valid classrooms
rooms = ['TP51', 'SP34', 'K3']

# Define the time slots (8am to 4pm)
times = list(range(9, 17))

# Create an initial random solution
solution = {}

# Define the cost function
def cost(solution, c, r, t):
    # Check if another class is already scheduled in the chosen room and time
    if any([solution[k] == (r, t) for k in solution if k != c]):
        return 1

    # Check if another class with the same four digits is scheduled in the same time slot
    class_prefix = c[:4]
    if any([k[:4] == class_prefix and solution[k][1] == t for k in solution if k != c]):
        return 1

    # All requirements are satisfied, return 0 cost
    return 0


def find_new_time_and_room(solution, c):
    best_r, best_t = solution[c]
    best_cost = cost(solution, c, best_r, best_t)
    # Iterate over all rooms and times to find the best one
    for r in rooms:
        for t in times:
            if r != solution[c][0] or t != solution[c][1]:
                cost_ = cost(solution, c, r, t)
                if cost_ < best_cost:
                    best_r, best_t = r, t
                    best_cost = cost_

    return best_r, best_t

def find_new_time_and_room_random(solution, c):
    conflict_rooms_and_times = []
    for r in rooms:
        for t in times:
            if cost(solution, c, r, t) < cost(solution, c, *solution[c]):
                conflict_rooms_and_times.append((r, t))
    return random.choice(conflict_rooms_and_times)

def print_solution(solution):
    # Create a list of lists representing the schedule table
    schedule_table = [[""] + list(rooms)]
    for t in times:
        row = [t]
        for r in rooms:
            scheduled_class = [k for k, v in solution.items() if v == (r, t)]
            if scheduled_class:
                row.append(scheduled_class[0])
            else:
                row.append("")
        schedule_table.append(row)

    # Print the schedule table
    for row in schedule_table:
        print("".join(str(cell).ljust(10) for cell in row))


# Define the main loop
def min_conflicts(max_iterations=50):
    # Create a random initial solution
    solution = {c: (random.choice(rooms), random.choice(times)) for c in classes}

    # Loop until we find a solution or reach the maximum number of iterations
    for i in range(max_iterations):
        # Compute the cost of the current solution
        #current_cost = sum([cost(solution, c, r, t) for c, (r, t) in solution.items()])
        conflict_classes = [c for c in classes if cost(solution, c, *solution[c]) > 0]
        
        # If the cost is 0, we have found a valid solution
        if conflict_classes == []:            
            return solution, i

        # Otherwise, choose a random class that has conflicts and a random time or room to move it to
        c = random.choice(conflict_classes)
        r, t = find_new_time_and_room(solution, c)
        # Move the class to the new time or room
        solution[c] = (r, t)
    else:
        return "failure", i



if __name__ == '__main__':
    solution, i = min_conflicts()
    if(solution == "failure"):
        print("Could not find a solution")
    else:
        print(f'\nFound solution after {i} iterations\n')
        print_solution(solution)

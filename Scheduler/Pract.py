import random

# List of classes to schedule
classes = ['MT101', 'MT102', 'MT103', 'MT104', 'MT105', 'MT106', 'MT107', 'MT201', 'MT202', 'MT203', 'MT204', 'MT205', 'MT206', 'MT301', 'MT302', 'MT303', 'MT304', 'MT401', 'MT402', 'MT403', 'MT501', 'MT502']

# List of valid times
times = ['9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm']

# List of valid classrooms
classrooms = ['TP51', 'SP34', 'K3']

# Dictionary to store the current schedule
schedule = {}

# Function to calculate the conflict score for a class
def conflict_score(c):
    time, room = schedule[c]
    same_time_room = [x for x in schedule if schedule[x] == (time, room) and x != c]
    same_time_first_digit = [x for x in schedule if x != c and x[:4] == c[:4] and (x != 'MT501' and c != 'MT502') and schedule[x][0] == time]
    return len(same_time_room) + len(same_time_first_digit)

# Function to get the set of conflicted variables
def get_conflicted_variables():
    conflicted = []
    for c in classes:
        if conflict_score(c) > 0:
            conflicted.append(c)
    return conflicted

def min_conflicts(csp, max_steps, current_state):

    # Initialize the schedule
    for c in classes:
        t = random.choice(times)
        r = random.choice(classrooms)
        schedule[c] = (t, r)

    # Min-Conflicts algorithm
    for i in range(max_steps):
        # Check if the current state is a solution
        if all(conflict_score(c) == 0 for c in classes):
            return schedule

        # Pick a random conflicted variable
        conflicted = get_conflicted_variables()
        var = random.choice(conflicted)

        # Find the value that minimizes conflicts for the variable
        min_score = conflict_score(var)
        min_values = []
        for value in csp[var]:
            current_state[var] = value
            new_score = conflict_score(var)
            if new_score < min_score:
                min_score = new_score
                min_values = [value]
            elif new_score == min_score:
                min_values.append(value)

        # Assign the variable to a random value that minimizes conflicts
        new_value = random.choice(min_values)
        current_state[var] = new_value
        schedule[var] = (new_value[0], new_value[1])

    # If a solution is not found after max_steps iterations, return failure
    return "failure"

# Print formatted schedule
def print_schedule(schedule):
    for r in classrooms:
        print(f'Room {r}:')
        for t in times:
            print(f'{t}:', end=' ')
            for c in classes:
                if schedule[c] == (t, r):
                    print(c, end=' ')
            print()
        print()

# Run the algorithm
if __name__ == '__main__':
    # Define the CSP
    csp = {}
    for c in classes:
        csp[c] = []
        for t in times:
            for r in classrooms:
                csp[c].append((t, r))

    # Set the initial state
min_conflicts(csp,100,)
print_schedule()
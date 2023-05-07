import copy
import random

# List of classes to schedule
classes = ['MT101', 'MT102', 'MT103', 'MT104', 'MT105', 'MT106', 'MT107', 'MT201', 'MT202', 'MT203', 'MT204', 'MT205', 'MT206', 'MT301', 'MT302', 'MT303', 'MT304', 'MT401', 'MT402', 'MT403', 'MT501', 'MT502']

# List of valid times
times = ['9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm']

# List of valid classrooms
classrooms = ['TP51', 'SP34', 'K3']

# Dictionary to store the current schedule
schedule = {}
csp = {}

# Function to calculate the conflict score for a class in the current schedule
def get_conflict(c, values):
    # c is an element of csp a dictionary of the form {class: [(time, room), (time, room), ...]}
    time, room = values
    #print("GET CONFLICT: ", c, time, room)
    score = 0
    for x in schedule:
        if schedule[x] == (time, room) and x != c:
            score += 1
        if x[:4] == c[:4] and (x != 'MT501' and c != 'MT502') and schedule[x][0] == time:
            score += 1
    #print("BROOOO: ", schedule[c][0])
    return score

# Function to get the set of conflicted variables
def get_conflicted_variables(sched):
    #print("GET CONFLICTED VARIABLES", sched)
    #get conflicted variables for each assignment in the schedule
    #print ("SCHEDULE: ", sched)
    conflicted = []
    for c in sched:
        if get_conflict(c, sched[c]) > 0:
            conflicted.append(c)
    return conflicted


def min_conflicts(csp, max_steps):

    # Initialize the schedule
    for c in csp:
        schedule[c] = random.choice(csp[c])
        print("\nFrom: ",csp[c][0], "\nChoose: ", schedule[c], len(schedule[c]))
    
    
    # Min-Conflicts algorithm
    for i in range(max_steps):

        conflicts = get_conflicted_variables(schedule)

        print("CONFLICTS: ", conflicts)
        # Check if the current state is a solution
        if conflicts == []:
            return schedule, i
            
        # Pick a random conflicted variable
        var = random.choice(conflicts)

        # Find the value that minimizes conflicts for the variable
        
        for value in csp[var]:
            conflict = get_conflict(var, value)
            #print("VAR >", var ,"VALUE: ", value, "CONFLICT: ", conflict)
            if conflict == 0:
                schedule[var] = value
                break

        # Update the schedule
        

        #current_state[var] = new_value
        #schedule[var] = (new_value)

    # If a solution is not found after max_steps iterations, return failure
    else:
        return "failure", max_steps

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


# Function to create the CSP
def csp_problem():
    csp = {}
    for c in classes:
        csp[c] = []
        for t in times:
            for r in classrooms:
                csp[c].append((t, r))
    return csp

# Run the algorithm
if __name__ == '__main__':
    # Define the CSP

    # Set the initial state
    #min_conflicts(csp,100)
    csp = csp_problem()
    #print("CSP: ", csp)
    sched, iter = min_conflicts(csp, 3000)
    print("SCHEDULE: ", sched)
    print_schedule(sched)
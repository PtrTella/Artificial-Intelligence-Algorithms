import random

# List of classes to schedule
classes = ['MT101', 'MT102', 'MT103', 'MT104', 'MT105', 'MT106', 'MT107', 'MT201', 'MT202', 'MT203', 'MT204', 'MT205', 'MT206', 'MT301', 'MT302', 'MT303', 'MT304', 'MT401', 'MT402', 'MT403', 'MT501', 'MT502']

# List of valid times
times = ['9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm']

# List of valid classrooms
classrooms = ['TP51', 'SP34', 'K3']

# Dictionary to store the current schedule
schedule = {}

#this is a comment

# Function to calculate the conflict score for a class

def conflict_score(c):
    time, room = schedule[c]
    same_time_room = [x for x in schedule if schedule[x] == (time, room) and x != c]
    same_time_first_digit = [x for x in schedule if x != c and x[:4] == c[:4] and (x != 'MT501' and c != 'MT502') and schedule[x][0] == time]
    return len(same_time_room) + len(same_time_first_digit)


def min_conflicts():

    # Initialize the schedule randomly
    for c in classes:
        t = random.choice(times)
        r = random.choice(classrooms)
        schedule[c] = (t, r)
    
    # Min-Conflicts algorithm
    max_iter = 1000
    for i in range(max_iter):
        # Pick a random class
        c = random.choice(classes)
        # Find its current conflict score
        score = conflict_score(c)
        # Find the assignments that result in the minimum conflict score
        min_score = score
        min_assignments = []
        for t in times:
            for r in classrooms:
                schedule[c] = (t, r)
                new_score = conflict_score(c)
                if new_score < min_score:
                    min_score = new_score
                    min_assignments = [(t, r)]
                elif new_score == min_score:
                    min_assignments.append((t, r))
        # Assign the class to a random assignment that results in the minimum conflict score
        if min_assignments:
            new_time, new_room = random.choice(min_assignments)
            schedule[c] = (new_time, new_room)
        # Check if the schedule has converged
        if all(conflict_score(c) == 0 for c in classes):            
            return schedule, i+1
    else:
        print(f'No feasible schedule found after {max_iter} iterations.')

# print formatted schedule
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
    schedule, iteration = min_conflicts()
    print_schedule(schedule)
    print(f'\nSchedule found after {iteration} iterations.')
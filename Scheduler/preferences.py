from copy import deepcopy
import MinCost as mc

# Give point to preferences, anyone wotrh the same
def preference_score(schedule):
    score = 0
    hours = 9
    for c in schedule:
        room, time = schedule[c]
        # MT501 should be scheduled at 1 pm or 2 pm
        if c == 'MT501' and time in  [13, 14]:
            score += 1
        
        # MT502 should be scheduled at 1 pm or 2 pm
        if c == 'MT502' and time in [13, 14]:
            score += 1
        
        # No class should be scheduled at 12 pm or 4 pm or 9 am
        if time in [9, 12, 16]:
                hours -= 1

    return (score + hours)

# Run the MinCost algorithm many times and keep the best schedule
def run_min_cost(iter):
    best_schedule = None
    best_score = 0

    for i in range(iter):
        schedule, n = deepcopy(mc.min_conflicts())
        if(schedule == "failure"):
            pass
        else:
            score = preference_score(schedule)
            if score > best_score:
                best_score = score
                best_schedule = schedule
        
    return best_schedule, best_score

if __name__ == '__main__':
    iter = int(input("How many times you want run min cost? "))
    sched, score = run_min_cost(iter)
    print(f"\nBEST SCHEDULE FOUND (score {score})\n")
    mc.print_solution(sched)

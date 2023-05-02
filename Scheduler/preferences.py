from copy import deepcopy
import MinCost as mc

# Give point to preferences, anyone wotrh the same
def preference_score(schedule):
    score = 0
    hours = 9
    for c in schedule:
        time, room = schedule[c]
        # MT501 should be scheduled at 1 pm or 2 pm
        if c == 'MT501' and time in ['1 pm', '2 pm']:
            score += 1
        
        # MT502 should be scheduled at 1 pm or 2 pm
        if c == 'MT502' and time in ['1 pm', '2 pm']:
            score += 1
        
        # No class should be scheduled at 12 pm or 4 pm or 9 am
        if time in ['12 pm', '4 pm', '9 am']:
                hours -= 1

    return (score + hours)

# Run the MinCost algorithm many times and keep the best schedule
def run_min_cost(iter):
    best_schedule = None
    best_score = 0

    for i in range(iter):
        schedule, n = deepcopy(mc.min_conflicts())
        score = preference_score(schedule)
        if score > best_score:
            best_score = score
            best_schedule = schedule
        
    return best_schedule, best_score

if __name__ == '__main__':
    iter = int(input("How many times you want run min cost? "))
    sched, score = run_min_cost(iter)
    print("\nFINAL SCORE", score)
    mc.print_schedule(sched)

same_time_room = [x for x in schedule if schedule[x] == (time, room) and x != c]
same_time_first_digit = [x for x in schedule if x != c and x[:4] == c[:4] and (x != 'MT501' and c != 'MT502') and schedule[x][0] == time]
return len(same_time_room) + len(same_time_first_digit)
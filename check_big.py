def verify_solution(schedule, num_weeks, num_groups):
    # Dictionary to track pairs of golfers seen together per group
    seen_pairs = {}

    for week in range(num_weeks):
        for group in range(num_groups):
            group_members = schedule[week][group]
            # Sort golfers to ensure unique representation of pairs
            group_members.sort()
            
            # Check all pairs within the group
            for i in range(len(group_members)):
                for j in range(i + 1, len(group_members)):
                    pair = (group_members[i], group_members[j])
                    if pair in seen_pairs:
                        return False  # Pair already seen together in a previous week
                    seen_pairs[pair] = True  # Mark pair as seen this week
    return True


# New schedule to check
new_schedule = [
    [[2, 20, 25, 28], [4, 14, 27, 31], [6, 8, 12, 24], [13, 18, 30, 32], [3, 11, 19, 23], [5, 15, 16, 29], [7, 10, 21, 26], [1, 9, 17, 22]],
    [[9, 18, 23, 27], [4, 7, 19, 25], [8, 10, 22, 29], [1, 16, 24, 32], [5, 11, 14, 26], [2, 20, 28, 31], [3, 17, 21, 30], [6, 12, 13, 15]],
    [[24, 30, 31, 32], [5, 20, 27, 29], [2, 11, 23, 25], [7, 12, 13, 21], [6, 8, 9, 14], [4, 10, 16, 19], [1, 3, 22, 26], [15, 17, 18, 28]],
    [[14, 15, 16, 32], [2, 12, 13, 31], [9, 20, 23, 30], [22, 24, 27, 29], [19, 25, 26, 28], [3, 10, 18, 21], [1, 5, 6, 17], [4, 7, 8, 11]],
    [[7, 17, 19, 28], [16, 20, 26, 31], [14, 15, 24, 30], [21, 23, 29, 32], [5, 13, 25, 27], [2, 6, 8, 9], [1, 4, 12, 18], [3, 10, 11, 22]],
    [[16, 27, 28, 31], [8, 20, 22, 30], [17, 24, 25, 29], [15, 19, 23, 26], [2, 4, 12, 14], [1, 5, 11, 13], [3, 6, 9, 10], [7, 18, 21, 32]],
    [[19, 20, 21, 32], [23, 24, 27, 30], [22, 25, 26, 31], [16, 18, 28, 29], [1, 12, 15, 17], [3, 6, 11, 14], [4, 7, 9, 13], [2, 5, 8, 10]],
    [[22, 23, 25, 32], [19, 24, 28, 31], [26, 27, 29, 30], [13, 15, 16, 20], [14, 17, 18, 21], [4, 5, 7, 12], [1, 2, 10, 11], [3, 6, 8, 9]],
    [[20, 26, 27, 30], [25, 29, 31, 32], [19, 21, 24, 28], [17, 18, 22, 23], [10, 11, 12, 16], [9, 13, 14, 15], [2, 3, 4, 8], [1, 5, 6, 7]],
    [[4, 6, 13, 32], [25, 26, 27, 28], [18, 21, 22, 30], [17, 19, 24, 31], [14, 15, 16, 20], [9, 10, 11, 12], [5, 7, 8, 29], [1, 2, 3, 23]],
]

# Use the existing parameters for the new schedule
num_weeks = 10
num_groups = 8

# Check and print result for the new schedule
print(verify_solution(new_schedule, num_weeks, num_groups))

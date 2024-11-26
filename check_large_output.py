import re

def parse_schedule(input_text):
    """
    Parses the input text into a structured schedule format compatible with verify_solution.

    Args:
        input_text (str): The input schedule text in the given format.

    Returns:
        list: A nested list of weeks and groups.
    """
    schedule = []
    current_week = []

    for line in input_text.splitlines():
        week_match = re.match(r"Week \d+:", line)
        group_match = re.match(r"  Group \d+: \[(.*?)\]", line)

        if week_match:
            if current_week:
                schedule.append(current_week)
                current_week = []
        elif group_match:
            group_data = list(map(int, group_match.group(1).split(", ")))
            current_week.append(group_data)

    # Append the last week
    if current_week:
        schedule.append(current_week)

    return schedule

def verify_solution(schedule, num_weeks, num_groups):
    """
    Verifies that no golfer pair appears more than once across all groups.

    Args:
        schedule (list): The nested list schedule to verify.
        num_weeks (int): The number of weeks in the schedule.
        num_groups (int): The number of groups per week.

    Returns:
        bool: True if the solution is valid, False otherwise.
    """
    seen_pairs = {}

    for week in range(num_weeks):
        for group in range(num_groups):
            group_members = schedule[week][group]
            group_members.sort()
            
            for i in range(len(group_members)):
                for j in range(i + 1, len(group_members)):
                    pair = (group_members[i], group_members[j])
                    if pair in seen_pairs:
                        return False  
                    seen_pairs[pair] = True  
    return True

input_text = """
Week 1:
  Group 1: [1, 21, 23, 31]
  Group 2: [4, 5, 9, 13]
  Group 3: [20, 25, 29, 32]
  Group 4: [12, 14, 16, 19]
  Group 5: [6, 10, 11, 24]
  Group 6: [3, 22, 26, 30]
  Group 7: [2, 8, 17, 27]
  Group 8: [7, 15, 18, 28]
Week 2:
  Group 1: [4, 10, 23, 25]
  Group 2: [7, 26, 27, 31]
  Group 3: [3, 8, 16, 24]
  Group 4: [1, 6, 14, 22]
  Group 5: [13, 18, 30, 32]
  Group 6: [15, 17, 20, 21]
  Group 7: [5, 11, 12, 28]
  Group 8: [2, 9, 19, 29]
Week 3:
  Group 1: [9, 17, 23, 24]
  Group 2: [2, 10, 16, 32]
  Group 3: [1, 28, 29, 30]
  Group 4: [3, 5, 7, 21]
  Group 5: [18, 19, 25, 31]
  Group 6: [8, 11, 14, 15]
  Group 7: [4, 6, 12, 26]
  Group 8: [13, 20, 22, 27]
Week 4:
  Group 1: [1, 10, 19, 26]
  Group 2: [6, 9, 16, 30]
  Group 3: [2, 5, 22, 24]
  Group 4: [8, 18, 20, 23]
  Group 5: [7, 12, 17, 29]
  Group 6: [11, 13, 21, 25]
  Group 7: [3, 15, 31, 32]
  Group 8: [4, 14, 27, 28]
Week 5:
  Group 1: [2, 7, 11, 20]
  Group 2: [5, 14, 30, 31]
  Group 3: [19, 22, 23, 28]
  Group 4: [3, 6, 17, 25]
  Group 5: [4, 18, 21, 24]
  Group 6: [1, 8, 12, 32]
  Group 7: [9, 10, 15, 27]
  Group 8: [13, 16, 26, 29]
Week 6:
  Group 1: [10, 14, 17, 18]
  Group 2: [2, 12, 13, 31]
  Group 3: [1, 3, 9, 20]
  Group 4: [24, 25, 26, 28]
  Group 5: [11, 23, 27, 32]
  Group 6: [4, 7, 16, 22]
  Group 7: [8, 19, 21, 30]
  Group 8: [5, 6, 15, 29]
Week 7:
  Group 1: [4, 11, 17, 19]
  Group 2: [12, 15, 24, 30]
  Group 3: [9, 21, 22, 32]
  Group 4: [10, 20, 28, 31]
  Group 5: [1, 5, 16, 25]
  Group 6: [6, 7, 8, 13]
  Group 7: [2, 14, 23, 26]
  Group 8: [3, 18, 27, 29]
"""

parsed_schedule = parse_schedule(input_text)
num_weeks = len(parsed_schedule)
num_groups = len(parsed_schedule[0]) if parsed_schedule else 0
print(verify_solution(parsed_schedule, num_weeks, num_groups))

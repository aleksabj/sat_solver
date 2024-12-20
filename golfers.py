from itertools import combinations
import os
import subprocess

def encode_to_cnf(g, p, w):
    """Encodes the Social Golfer Problem into CNF."""
    a = g * p  # Total number of golfers
    cnf = []
    var_count = 0
    mapping = {}
    pair_mapping = {}  
    
    def get_var(i, j, k):
        """Maps a golfer-week-group tuple to a unique SAT variable."""
        nonlocal var_count
        if (i, j, k) not in mapping:
            var_count += 1
            mapping[(i, j, k)] = var_count
        return mapping[(i, j, k)]
    
    def get_pair_var(i1, i2, k):
        """Maps a golfer pair-week to a unique SAT variable."""
        nonlocal var_count
        if (i1, i2, k) not in pair_mapping:
            var_count += 1
            pair_mapping[(i1, i2, k)] = var_count
        return pair_mapping[(i1, i2, k)]
    
    # Ensure each golfer is in exactly one group per week
    for k in range(w):
        for i in range(a):
            vars = [get_var(i, j, k) for j in range(g)]
            cnf.append(vars)
            for v1, v2 in combinations(vars, 2):
                cnf.append([-v1, -v2])  # No golfer can be in more than one group per week
    
    # Ensure each group has exactly p golfers per week
    for k in range(w):
        for j in range(g):
            vars = [get_var(i, j, k) for i in range(a)]
            cnf.append(vars)
            for comb in combinations(vars, p + 1):
                cnf.append([-v for v in comb])  # No group can have more than p golfers
    
    # Ensure no golfer pair meets more than once
    for i1 in range(a):
        for i2 in range(i1 + 1, a):
            t_vars = []
            for k in range(w):
                t_var = get_pair_var(i1, i2, k)
                t_vars.append(t_var)
                for j in range(g):
                    cnf.append([-get_var(i1, j, k), -get_var(i2, j, k), t_var])
                group_vars = [get_var(i1, j, k) for j in range(g)]
                cnf.append([-t_var] + group_vars)
                group_vars = [get_var(i2, j, k) for j in range(g)]
                cnf.append([-t_var] + group_vars)
            for t1, t2 in combinations(t_vars, 2):
                cnf.append([-t1, -t2])  # No pair can meet more than once
    return cnf, var_count, mapping


def write_dimacs(cnf, var_count, filename):
    """Writes the CNF formula to a DIMACS file."""
    print(f"Writing CNF with {var_count} variables and {len(cnf)} clauses.")
    with open(filename, 'w') as f:
        f.write(f"p cnf {var_count} {len(cnf)}\n")
        for clause in cnf:
            f.write(" ".join(map(str, clause)) + " 0\n")


def run_glucose(dimacs_file):
    """Executes Glucose SAT solver on the given DIMACS file."""
    result = subprocess.run(["./glucose/simp/glucose", "-model", dimacs_file], capture_output=True, text=True)
    if "UNSAT" in result.stdout:
        return "UNSAT"
    return result.stdout

def decode_solution(output, mapping):
    """Decodes Glucose solution."""
    if output == "UNSAT":
        return None
    assignment_set = set()
    for line in output.strip().splitlines():
        if line.startswith('v') or line.startswith('V'):
            tokens = line[1:].strip().split()
            for token in tokens:
                if token == '0':
                    continue
                assignment_set.add(int(token))
    solution = {}
    reverse_mapping = {v: k for k, v in mapping.items()}
    for var in assignment_set:
        var_num = abs(var)
        assigned_value = var > 0
        if var_num in reverse_mapping:
            key = reverse_mapping[var_num]
            solution[key] = assigned_value
        else:
            pass
    return solution

def generate_schedule(solution, g, p, w):
    """Generates a human-readable schedule from the solution."""
    if not solution:
        return "No solution found."
    a = g * p
    schedule = []
    for k in range(w):
        week = []
        for j in range(g):
            group = [i + 1 for i in range(a) if solution.get((i, j, k), False)]
            week.append(group)
        schedule.append(week)
    return schedule

def print_schedule(schedule, output_file):
    """Writes the schedule to an output file."""
    with open(output_file, 'w') as f:
        if schedule == "No solution found.":
            f.write(schedule)
        else:
            for w, week in enumerate(schedule):
                f.write(f"Week {w + 1}:\n")
                for g, group in enumerate(week):
                    f.write(f"  Group {g + 1}: {group}\n")

def process_instance(instance_file):
    """Processes an instance from an input file."""
    with open(instance_file, 'r') as f:
        g, p, w = map(int, f.readline().split())
    cnf, var_count, mapping = encode_to_cnf(g, p, w)
    dimacs_file = instance_file.replace('.in', '.cnf')
    write_dimacs(cnf, var_count, dimacs_file)
    output = run_glucose(dimacs_file)
    if output == "UNSAT":
        print_schedule("No solution found.", instance_file.replace('.in', '.out'))
        return
    solution = decode_solution(output, mapping)
    if not solution:
        print_schedule("No solution found.", instance_file.replace('.in', '.out'))
        return
    schedule = generate_schedule(solution, g, p, w)
    print_schedule(schedule, instance_file.replace('.in', '.out'))

def validate_solution(solution, g, p, w):
    """Ensures the SAT solution meets basic SGP constraints."""
    a = g * p
    for k in range(w):
        seen = set()
        for j in range(g):
            for i in range(a):
                if solution.get((i, j, k), False):
                    if i in seen: 
                        return False
                    seen.add(i)
        if len(seen) != a: 
            return False
    return True

if __name__ == "__main__":
    instance_dir = "instances"
    for instance_file in os.listdir(instance_dir):
        if instance_file.endswith(".in"):
            process_instance(os.path.join(instance_dir, instance_file))
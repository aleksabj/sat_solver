# Social Golfer Problem Solver

This project provides a SAT-based solution to the **Social Golfer Problem (SGP)**. It encodes the problem into a CNF formula and utilizes the **Glucose SAT solver** to find a valid schedule or determine that none exists.

## Table of Contents

- [Problem Description](#problem-description)
- [CNF Encoding](#cnf-encoding)
- [Script Usage](#script-usage)
- [Attached Instances](#attached-instances)
- [Experiments and Results](#experiments-and-results)
- [Additional Files](#additional-files)
- [Glucose SAT Solver](#glucose-sat-solver)
- [Project Structure](#project-structure)

## Problem Description

The **Social Golfer Problem** involves scheduling golfers into groups over a certain number of weeks, ensuring that no pair of golfers plays together more than once.

**Parameters:**

- **`m`**: Number of groups per week
- **`n`**: Number of golfers per group
- **`w`**: Number of weeks
- **Total golfers (`m × n`)**: The total number of golfers participating.

**Constraints:**

1. **Each Golfer Plays Exactly Once Per Week:**
   - Every golfer must be assigned to exactly one group each week.
2. **Group Size Is Consistent:**
   - Each group must have exactly `n` golfers.
3. **No Repeated Pairs:**
   - No pair of golfers can play together more than once throughout the `w` weeks.

The goal is to create a schedule that satisfies all these constraints, or determine that no such schedule exists.

## CNF Encoding

The problem is encoded into Conjunctive Normal Form (CNF) to be solved by a SAT solver.

### Propositional Variables

1. **Golfer Assignment Variables (`x_{i,j,k}`):**
   - **Meaning**: Golfer `i` is assigned to group `j` in week `k`.
   - **Indices**:
     - `i` ∈ {0, ..., `a*b` - 1}
     - `j` ∈ {0, ..., `a` - 1}
     - `k` ∈ {0, ..., `c` - 1}

2. **Golfer Pair Variables (`t_{i1,i2,k}`):**
   - **Meaning**: Golfer `i1` and golfer `i2` are together in week `k`.
   - Used to enforce the constraint that any pair meets at most once.

### Constraints Encoding

1. **Each Golfer in Exactly One Group per Week:**

   - **At least one group per week**:
     - For each golfer `i` and week `k`:
       ```
       x_{i,0,k} ∨ x_{i,1,k} ∨ ... ∨ x_{i,a-1,k}
       ```
   - **At most one group per week**:
     - For each golfer `i`, week `k`, and all pairs of groups `(j1, j2)` with `j1 ≠ j2`:
       ```
       ¬x_{i,j1,k} ∨ ¬x_{i,j2,k}
       ```

2. **Each Group Has Exactly `n` Golfers:**

   - **At least `n` golfers per group**:
     - For each group `j`, week `k`:
       ```
       Clauses ensuring at least `n` golfers are in group `j` during week `k`.
       ```
   - **At most `n` golfers per group**:
     - For each group `j`, week `k`, and combinations of `n + 1` golfers:
       ```
       ¬x_{i1,j,k} ∨ ¬x_{i2,j,k} ∨ ... ∨ ¬x_{i_{b+1},j,k}
       ```

3. **No Pair Meets More Than Once:**

   - For each pair of golfers `(i1, i2)`:
     - Introduce auxiliary variables `t_{i1,i2,k}` for each week `k`.
     - Ensure that `t_{i1,i2,k}` is true if `i1` and `i2` are together in week `k`.
     - Add clauses to ensure that no two `t_{i1,i2,k}` are true simultaneously:
       ```
       ¬t_{i1,i2,k1} ∨ ¬t_{i1,i2,k2}   for all k1 < k2
       ```


## Script Usage

### Prerequisites

- Python 3.x
- Glucose SAT Solver (see [Glucose SAT Solver](#glucose-sat-solver))

### Input Format

- **Instance Files (`.in`):**
  - Located in the `instances` folder.
  - Each file contains a single line with three integers:
    ```
    m n w
    ```
    - `m`: Number of groups per week.
    - `n`: Number of golfers per group.
    - `w`: Number of weeks.

### Running the Script

Execute the main script to process all instances in the `instances` folder:

```bash
python golfers.py
```

### Output

- **CNF Files (`.cnf`):**
  - Generated CNF files corresponding to each instance.
  - Located in the `instances` folder.

- **Output Files (`.out`):**
  - Schedule results or "No solution found."
  - Located in the `instances` folder.
  - Format for schedules:
    ```
    Week 1:
      Group 1: [golfer_indices]
      Group 2: [golfer_indices]
      ...
    Week 2:
      Group 1: [golfer_indices]
      ...
    ```

## Attached Instances

Located in the `instances` folder, the project includes three types of instances:

1. **`small_positive.in`:**
   - A small instance that results in a valid schedule.
   - Processes quickly.

2. **`small_negative.in`:**
   - A small instance with no valid schedule.
   - Outputs "No solution found."

3. **`nontrivial.in`:**
   - An instance of moderate complexity.
   - Generates a valid schedule in approximately **2 minutes and 37 seconds**.

### Instance Format

Each `.in` file contains three integers:

```
m n w
```

Example (`nontrivial.in`):

```
8 4 7
```

- **Number of groups (`m`)**: 8
- **Golfers per group (`n`)**: 4
- **Number of weeks (`w`)**: 7
- **Total golfers**: `8 × 4 = 32`

## Experiments and Results

The script's performance varies with the instance size:

- **Small Instances:**
  - Solved in seconds.
  - Validate the correctness of the encoding and solver integration.

- **Medium Instances (e.g., `nontrivial.in`):**
  - **Parameters:** `8 4 7` (32 golfers over 7 weeks)
  - **Runtime:** Approximately **2 minutes and 37 seconds**
  - **Outcome:** Successfully generates a valid schedule.


## Additional Files

- **`check_large_output.py`:**
  - A utility script used during development.
  - Verifies the correctness of large schedules by ensuring no pair of golfers meets more than once.
  - Parses the output schedule and checks for constraint violations.

## Glucose SAT Solver

The project uses the **Glucose SAT Solver**.

### Obtaining Glucose

- **GitHub Repository:**
  - [Glucose GitHub Repository](https://github.com/audemard/glucose.git)

### Compilation Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/audemard/glucose.git 
   ```

2. **Compile the Solver:**

   ```bash
   cd glucose/simp
   make
   ```

   - This will generate the `glucose` executable in the `glucose/simp` directory.

### Integration with the Script

- The script calls the solver using the path `./glucose/simp/glucose`.
- Ensure the executable is in the correct location.

## Project Structure

- **`golfers.py`:**
  - The main script that encodes the SGP into CNF, calls the Glucose solver, and processes the output.
  - **Key Functions:**
    - `encode_to_cnf(g, p, w)`: Encodes the problem into CNF.
    - `write_dimacs(cnf, var_count, filename)`: Writes the CNF to a DIMACS file.
    - `run_glucose(dimacs_file)`: Runs the Glucose solver.
    - `decode_solution(output, mapping)`: Decodes the solver's output.
    - `generate_schedule(solution, g, p, w)`: Generates a readable schedule.
    - `print_schedule(schedule, output_file)`: Writes the schedule to an output file.
    - `process_instance(instance_file)`: Processes a single instance file.

- **`check_large_output.py`:**
  - Helper script for verifying large schedules.

- **`instances/`:**
  - Contains `.in` input files and the generated `.cnf` and `.out` files.

## Conclusion

This project provides a practical solution to the Social Golfer Problem for small to medium instances using SAT encoding and the Glucose solver. While larger instances pose computational challenges, the current implementation serves as a foundation for further optimization and exploration.
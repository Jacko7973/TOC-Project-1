#!/usr/bin/env python3

num_vars = 3
num_clauses = 4
wff = [[1, 2, 3], [3], [-3, -2]]
wff = []

absolute = {}
assignment = []

def unit(wff):
    """
    Apply the unit clause rule to simplify the formula.
    """
    for clause in wff:
        if len(clause) == 1:
            literal = clause[0]
            if literal < 0:
                # If literal is negative, set the corresponding variable to False (0)
                if abs(literal) in absolute:
                    if absolute[abs(literal)] == 1:
                        return False  # Contradiction found
                else:
                    absolute[abs(literal)] = 0
            else:
                # If literal is positive, set the corresponding variable to True (1)
                if abs(literal) in absolute:
                    if absolute[literal] == 0:
                        return False  # Contradiction found
                else:
                    absolute[literal] = 1
    return True

def build_assignment(num_vars):
    """
    Build the initial assignment based on unit clause results.
    Assign 0 (False) for any variable not determined by unit propagation.
    """
    global assignment
    assignment = [0] * (num_vars + 1)  # Assign 0 to all variables initially
    for var in range(1, num_vars + 1):
        if var in absolute:
            assignment[var] = absolute[var]

def check_clause(clause, assignment):
    """
    Check if the clause is satisfied by the current assignment.
    """
    for literal in clause:
        if literal > 0 and assignment[literal] == 1:
            return True  # Positive literal is true
        if literal < 0 and assignment[-literal] == 0:
            return True  # Negative literal is true
    return False  # None of the literals in the clause are satisfied

def check(wff, num_vars, num_clauses, assignment):
    """
    Brute force check: Try all possible assignments to see if the wff is satisfiable.
    """
    while True:
        # Check if the current assignment satisfies all clauses
        all_satisfied = True
        for clause in wff:
            if not check_clause(clause, assignment):
                all_satisfied = False
                break

        if all_satisfied:
            return True  # Found a satisfying assignment

        # Try the next assignment by flipping variables
        for i in range(1, num_vars + 1):
            if i not in absolute:  # Only flip variables that weren't set by unit propagation
                if assignment[i] == 0:
                    assignment[i] = 1
                    break
                else:
                    assignment[i] = 0
        else:
            # If we exhaust all possibilities without finding a solution, return False
            return False

def main():
    global assignment
    # Step 1: Apply unit clause rule
    if not unit(wff):
        print("Unsatisfiable (due to unit clause contradiction)")
        return
    
    # Step 2: Build an initial assignment based on unit propagation
    build_assignment(num_vars)

    # Step 3: Check if the formula is satisfiable with the current assignments
    result = check(wff, num_vars, num_clauses, assignment)
    if result:
        print("Satisfiable")
    else:
        print("Unsatisfiable")

if __name__ == "__main__":
    main()

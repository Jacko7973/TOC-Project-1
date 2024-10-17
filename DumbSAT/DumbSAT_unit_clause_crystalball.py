# /usr/bin/env python3

def check_unit_clause(Wff,Nvars,Nclauses,Assignment):
# Run thru all possibilities for assignments to wff
# Starting at a given Assignment (typically array of Nvars+1 0's)
# At each iteration the assignment is "incremented" to next possible
# At the 2^Nvars+1'st iteration, stop - tried all assignments

    # OPTIMIZATION: Unit Clause:

    print(Wff)
    del_clauses = []
    known_assignments = {}
    for i, clause in enumerate(Wff):
        if len(set(clause)) != 1:
            continue

        literal = clause[0]
        variable = abs(literal)
        negate = (literal < 0)

        if variable in known_assignments:
            assignment = known_assignments[variable]
            if assignment == negate:
                # Conflicting unit clauses: Expression unsatisfiable
                return False

        else:
            # Add to known assignments
            known_assignments[variable] = not negate

        del_clauses.append(i)


    for i in sorted(del_clauses, key=lambda n: -n):
        del Wff[i]
        Nclauses -= 1

    for i in range(1,Nvars+2):
        # Add the known assignments
        if (i in known_assignments):
            Assignment[i] = 1 if known_assignments[i] else 0

    print(known_assignments)


    Satisfiable=False
    while (Assignment[Nvars+1]==0):
        print(Assignment)
        # Iterate thru clauses, quit if not satisfiable
        for i in range(0,Nclauses): #Check i'th clause
            Satisfiable=False
            Clause=Wff[i]

            for j in range(0,len(Clause)): # check each literal
                Literal=Clause[j]
                if Literal>0: Lit=1
                else: Lit=0
                VarValue=Assignment[abs(Literal)] # look up literal's value
                if Lit==VarValue:
                    Satisfiable=True
                    break
            if Satisfiable==False: break
        if Satisfiable==True: break # exit if found a satisfying assignment

        # Last try did not satisfy; generate next assignment)
        for i in range(1,Nvars+2):
            # Skip the known assignments
            # if (i in known_assignments):
            #     continue

            if Assignment[i]==0:
                Assignment[i]=1
                break
            else: Assignment[i]=0
    return Satisfiable


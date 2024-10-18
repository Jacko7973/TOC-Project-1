import sys
import pathlib
from copy import deepcopy
from typing import Optional

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))

from SAT_lib import SATExpression, test_solver


# Reference: UPenn Computer Science
# URL: https://www.cis.upenn.edu/~cis1890/files/Lecture3.pdf
def dpll(ex: SATExpression, assignments: dict[str, bool] = {}) -> Optional[dict[str, bool]]:

    ex = deepcopy(ex)

    # Remove redundant literals / clauses
    for c in ex.clauses[:]:
        # Within a clause, remove any literals that evaluate to False
        for lit in c.literals[:]:
            if lit.var not in assignments: continue
            if not lit(assignments[lit.var]):
                c.literals.remove(lit)

        # Remove any clauses that evaluate to True
        if any(var not in assignments for var in c.get_variables()):
            continue
        if c(assignments):
            ex.clauses.remove(c)

    # Base Case: Empty set of clauses
    if len(ex.clauses) == 0:
        return assignments

    # Base Case: Empty clauses exists
    if any(len(c.literals) == 0 for c in ex.clauses):
        return None

    #Recursive Case: Contains unit clause
    new_assignments = assignments.copy()
    for c in ex.clauses[:]:
        if (len(c.literals) != 1): continue
        new_assignments[c.literals[0].var] = not c.literals[0].negate
        return dpll(ex, new_assignments)


    # Recursive Case: Try assignment
    new_assignments = assignments.copy()
    var = None
    for v in ex.get_variables():
        if v in new_assignments: continue
        var = v
        break
    else:
        return None

    for value in (False, True):
        new_assignments[var] = value
        if ret := dpll(ex, new_assignments):
            return ret
        del new_assignments[var]

    return None


#/usr/bin/env python3

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))

# Import custom SAT library
from SAT_lib import SATExpression, test_solver


# Import DumbSAT checking algorithm
<<<<<<< HEAD
from DumbSAT import check as DumbSAT

from MyDumbSAT_crystalball import MyDumbSAT
# Import DumbSAT with unit clause optimization
from MyDumbSAT_both_crystalball import MyDumbSAT_both
=======
from DumbSAT import check

# Import DumbSAT with unit clause algorithm
from DumbSAT_unit_clause_crystalball import check_unit_clause
>>>>>>> 2d8928069c889b0bbd97be544e3d79b952b730cc



## Constants

SOLVERS = {
<<<<<<< HEAD
    "DumbSAT": DumbSAT,
    "MyDumbSAT": MyDumbSAT,
    "MyDumbSAT_both": MyDumbSAT_both
=======
    "DumbSAT": check,
    "DumbSAT_unit_clause": check_unit_clause,
>>>>>>> 2d8928069c889b0bbd97be544e3d79b952b730cc
}

INPUT_FILE = "../SAT_lib/data/kSAT.cnf.csv"
OUTPUT_FILE = "test_data.csv"


## Functions

def tester_create(check_fn):
    """ Create a function wrapper so DumbSAT implementation
    can be checked using the SAT_lib library.
    """

    def tester(ex: SATExpression) -> bool:
        # Use DumbSAT to solve SATExpression
        wff_list = ex.to_list()
        n_vars = ex.num_vars
        n_clauses = len(ex.clauses)
        assignment = [0 for _ in range(max(max(abs(l) for l in c) for c in wff_list) + 2)]
        return check_fn(wff_list, n_vars, n_clauses, assignment)

    return tester


## Main execution

def main():

    # Test and benchmark the DumbSAT implementation
    # Defaults to unmodified DumbSAT

    solver_name = "DumbSAT"
    if len(sys.argv) >= 2 and sys.argv[1] in SOLVERS:
        solver_name = sys.argv[1]

    infile_name = INPUT_FILE
    if len(sys.argv) >= 3:
        infile_name = sys.argv[2]

    outfile_name = OUTPUT_FILE
    if len(sys.argv) >= 4:
        outfile_name = sys.argv[3]


    check_fn = SOLVERS[solver_name]
    tester = tester_create(check_fn)
    print(f"[INFO] Testing solver {solver_name}")
    test_solver(tester, solver_name, infile_name, outfile_name)



if __name__ == "__main__":
    main()


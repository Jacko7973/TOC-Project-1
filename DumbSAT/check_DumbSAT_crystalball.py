#!/usr/bin/env python3

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))

# Import custom SAT library
from SAT_lib import SATExpression, test_solver


# Import DumbSAT checking algorithm
from DumbSAT_crystalball import check as DumbSAT

# Import DumbSAT improvements
from MyDumbSAT_iter_crystalball import MyDumbSAT_iter
from MyDumbSAT_both_crystalball import MyDumbSAT_both


## Constants

SOLVERS = {
    "DumbSAT": DumbSAT,
    "MyDumbSAT_iter": MyDumbSAT_iter,
    "MyDumbSAT_both": MyDumbSAT_both
}

INPUT_FILE = "../SAT_lib/data/data_kSAT_crystalball.cnf.csv"
OUTPUT_FILE = "output_test_data_crystalball.csv"


## Functions

def tester_create(check_fn):
    # Create a function wrapper so DumbSAT implementation
    # can be checked using the SAT_lib library.

    def tester(ex: SATExpression) -> bool:
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
    if len(sys.argv) >= 2:
        if sys.argv[1] in SOLVERS:
            solver_name = sys.argv[1]
        else:
            print("[ERROR] Please select one of the following solvers to test")
            print(" ".join(SOLVERS.keys()))
            return

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


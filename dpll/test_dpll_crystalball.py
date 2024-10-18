import sys
import pathlib
from copy import deepcopy
from typing import Optional

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))

# Import custom SAT library
from SAT_lib import SATExpression, test_solver

# Import dpll solver
from dpll_crystalball import dpll

# Globals

INPUT_FILE = "../SAT_lib/data/kSAT.cnf.csv"
OUTPUT_FILE = "test_data.csv"

def test_dpll(ex: SATExpression) -> bool:
    return dpll(ex, {})


def main():

    infile_name = INPUT_FILE
    if len(sys.argv) >= 2:
        infile_name = sys.argv[1]

    outfile_name = OUTPUT_FILE
    if len(sys.argv) >= 3:
        infile_name = sys.argv[2]

    test_solver(test_dpll, "dpll", infile_name, outfile_name)


if __name__ == "__main__":
    main()


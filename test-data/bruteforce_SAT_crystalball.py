import sys
import pathlib
import pickle
from typing import Iterator

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))

from SAT_lib import SATExpression, load_DIMACS_csv


def generate_assignments(variables: list[str], assignment:dict[str,bool]={}) -> Iterator[dict[str,bool]]:
  if not variables:
    yield assignment
    return

  var = variables[0]
  for value in (False, True):
    assignment[var] = value
    yield from generate_assignments(variables[1:], assignment)


def bruteforce_expression(ex: SATExpression, verbose: bool = False) -> bool:

    verbose and print(f"Testing expression: " + str(ex) + " ", end="")

    for assignment in generate_assignments(list(ex.get_variables())):
        if not ex(assignment): continue

        verbose and print("SATISFIABLE")
        return True

    verbose and print("UNSATISFIABLE")
    return False



if __name__ == "__main__":
    test_cases = load_DIMACS_csv("2SAT.cnf.csv")
    print(f"[INFO] Successfully loaded {len(test_cases)} test cases.")

    for tc in test_cases:
        tc["satisfiable"] = bruteforce_expression(tc["cnf"], True)
        print()

    with open("2SAT_SOLVED_crystalball.dat", "wb") as f:
        pickle.dump(test_cases, f)



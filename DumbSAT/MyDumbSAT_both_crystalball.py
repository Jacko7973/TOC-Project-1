#!/usr/bin/env python3

import sys
import pathlib
from typing import Iterator
import itertools

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))

# Import custom SAT library
from SAT_lib import SATExpression, test_solver


def MyDumbSAT_both(wff, n_vars, n_clauses, assignment):


  max_var = max(max(abs(i) for i in c) for c in wff)
  input_char_sets = []
  for i in range(max_var):
    input_char_sets.append([0, 1])

  # OPTIMIZATION: Unit Clause
  for clause in wff[:]:
    # Continue if not unit clause
    if (len(set(clause))) != 1: continue

    literal = clause[0]
    variable = abs(literal)
    negate = literal < 0
    index = variable - 1

    try:
      # Add to known assignments
      input_char_sets[index].remove(int(negate))
    except ValueError:
      pass

    if not len(input_char_sets[index]):
      # Unit Clause Contradiction -> Unsatisfiable
      return False



  for assignment in itertools.product(*input_char_sets):
    for clause in wff:
      if any(assignment[abs(l) - 1] == int(l > 0) for l in clause):
        continue
      break
    else:
      return True
  return False


if __name__ == "__main__":
  print(MyDumbSAT_unit([[-1, 2], [-1, -2], [-1]], 2, 3, []))


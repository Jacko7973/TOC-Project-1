#!/usr/bin/env python3

import itertools

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
      # Reduce the input set to only include the satisfying assignment
      input_char_sets[index].remove(int(negate))
    except ValueError:
      pass

    if not len(input_char_sets[index]):
      # Unit Clause Contradiction -> Unsatisfiable
      return False


  # Also use the same incremental approach as before
  for assignment in itertools.product(*input_char_sets):
    for clause in wff:
      if any(assignment[abs(l) - 1] == int(l > 0) for l in clause):
        continue
      break
    else:
      return True
  return False


if __name__ == "__main__":
  # Test a simple wff with a unit clause
  print(MyDumbSAT_both([[-1, 2], [-1, -2], [-1]], 2, 3, []))


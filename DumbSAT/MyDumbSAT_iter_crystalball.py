#!/usr/bin/env python3

import itertools

def MyDumbSAT_iter(wff, n_vars, n_clauses, assignment):

  # OPTIMIZATION: Iterative
  # Define a character set for each variable
  max_var = max(max(abs(i) for i in c) for c in wff)
  input_char_sets = []
  for i in range(max_var):
    input_char_sets.append([0, 1])

  # Use itertools.product to iterativly generate members of the Cross Product
  # of our character sets to use as assignments to the variables in the wff.
  for assignment in itertools.product(*input_char_sets):
    for clause in wff:
      if any(bool(assignment[abs(i) - 1]) == (i > 0) for i in clause):
        continue
      break
    else:
      return True
  return False



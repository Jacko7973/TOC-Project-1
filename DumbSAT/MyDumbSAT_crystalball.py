#!/usr/bin/env python3

import sys
import pathlib
from typing import Iterator
import itertools

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))

# Import custom SAT library
from SAT_lib import SATExpression, test_solver


def MyDumbSAT(wff, n_vars, n_clauses, assignment):

  max_var = max(max(abs(i) for i in c) for c in wff)

  for assignment in itertools.product(*((0, 1),)*max_var):
    for clause in wff:
      if any(bool(assignment[abs(i) - 1]) == (i > 0) for i in clause):
        continue
      break
    else:
      return True
  return False



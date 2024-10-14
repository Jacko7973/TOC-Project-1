#!/usr/bin/env python3
# TOC-Project-1-crystalball
# SAT_lib/__init__.py
# Author: Jack O'Connor
# Date: 10/9/2024


import csv
import itertools
from string import ascii_lowercase
from typing import Iterator


from ._SAT_utils_crystalball import SATExpression, SATClause, SATLiteral, Solution

__all__ = ["SATExpression", "SATClause", "SATLiteral", "load_DIMACS_csv", "load_DIMACS_csv_v2"]

VARIABLES = list(a+b for a, b in itertools.product(ascii_lowercase, ascii_lowercase))


def load_DIMACS_csv_v2(csv_path:str) -> Iterator[SATExpression]:

  with open(csv_path, "r") as f:

    current_ex = None
    current_clauses = None
    satisfiable = None
    for record in csv.reader(f, delimiter=","):
      if not record:
        continue

      if record[0] == "c":
        if current_ex:
          ex = SATExpression.from_list(current_ex)
          ex.solution = satisfiable
          yield ex

        current_ex = []
        current_clause = []
        satisfiable = Solution(record[3].upper())

      elif record[0] == "p":
        continue

      else:
        for item in record:
          if not item: continue
          item = int(item)
          if item == 0:
            current_ex.append(current_clause)
            current_clause = []
            continue

          current_clause.append(item)




def load_DIMACS_csv(csv_path:str) -> Iterator[SATExpression]:
  test_cases = []

  current_expression = None
  current_clause = SATClause([])
  current_case = -1
  with open(csv_path, "r") as f:
    for record in csv.reader(f, delimiter=","):
      if not record:
        continue

      if record[0] == "c":
        current_expression = SATExpression([])
        current_clause = SATClause([])

        current_case += 1
        test_cases.append({})

        test_cases[current_case]["cnf"] = current_expression
        test_cases[current_case]["k-SAT"] = int(record[2])
        test_cases[current_case]["satisfiable"] = (record[3].upper() == "S")

      elif record[0] == "p":
        test_cases[current_case]["variables"] = int(record[2])
        test_cases[current_case]["clauses"] = int(record[3])

      else:
        for item in record:
          if item == "0":
            current_expression.clauses.append(current_clause)
            current_clause = SATClause([])
            break

          var_num = int(item)
          var = VARIABLES[abs(var_num) - 1]
          negate = (var_num < 0)
          lit = SATLiteral(var, negate)

          current_clause.literals.append(lit)

  return test_cases


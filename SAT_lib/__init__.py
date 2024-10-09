#!/usr/bin/env python3
# TOC-Project-1-crystalball
# SAT_lib/__init__.py
# Author: Jack O'Connor
# Date: 10/9/2024


import csv
from string import ascii_lowercase


from ._SAT_utils_crystalball import SATExpression, SATClause, SATLiteral

__all__ = ["SATExpression", "SATClause", "SATLiteral", "load_DIMACS_csv"]

def load_DIMACS_csv(csv_path:str) -> list[str]:
  test_cases = []

  current_expression = None
  current_clause = SATClause([])
  current_case = -1
  with open(csv_path, "r") as f:
    for record in csv.reader(f, delimiter=","):
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

          var = ascii_lowercase[int(item[-1]) - 1]
          negate = (item[0] == "-")
          lit = SATLiteral(var, negate)

          current_clause.literals.append(lit)

  return test_cases


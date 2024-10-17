#!/usr/bin/env python3
# TOC-Project-1-crystalball
# SAT_lib/__init__.py
# Author: Jack O'Connor
# Date: 10/9/2024


import sys
import csv
import itertools
from string import ascii_lowercase
import time
from typing import Iterator
import signal


from ._SAT_utils_crystalball import SATExpression, SATClause, SATLiteral, Solution

__all__ = ["SATExpression", "SATClause", "SATLiteral", "Solution", "load_DIMACS_csv", "test_solver", "generate_assignments", "test_solver"]

VARIABLES = list(a+b for a, b in itertools.product(ascii_lowercase, ascii_lowercase))


class TimeoutException(Exception):
  pass


def load_DIMACS_csv(csv_path:str) -> Iterator[SATExpression]:

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


def test_solver(solver, name: str, test_filename: str, out_filename: str, timeout: int = 300) -> None:
  try:
    test_cases = load_DIMACS_csv(test_filename)
  except:
    print(f"[ERR] Unable to load testcases from {test_filename}")
    return

  i = 0
  data = [("name", "kSAT", "vars", "solution", "runtime")]

  def alarm_handler(signum, frame):
    raise TimeoutException

  signal.signal(signal.SIGALRM, alarm_handler)

  for tc in test_cases:

    print(f"[INFO] Testing case #{i}")

    start = time.time()
    signal.alarm(timeout)

    try:
      sol = Solution.SATISFIABLE if solver(tc) else Solution.UNSATISFIABLE
      runtime = time.time() - start

      if tc.solution == Solution.UNKNOWN:
        tc.solution = sol

      elif tc.solution != sol:
        print(f"[INFO] Test Case Failed: {str(tc)}")
        print(f"\tCorrect output: {tc.solution}")
        print(f"\tProgram output: {sol}")
        print("[INFO] Status... Failure")
        sys.exit()


      data.append((name, tc.ksat, tc.num_vars, tc.solution.value, runtime))
      i += 1

    except KeyboardInterrupt:
      print("[INFO] Interrupt recieved. Exiting...")
      break

    except TimeoutException:
      print("[INFO] Timeout exceeded. Exiting...")
      break

    finally:
      signal.alarm(0)

  print("[INFO] Status... OK")
  print(f"[INFO] Passed {i} tests")

  print(f"[INFO] Saving results to {out_filename}")

  with open(out_filename, "w") as f:
    writer = csv.writer(f, delimiter=",")
    for row in data:
      writer.writerow(row)


def generate_assignments(variables: list[str], assignment:dict[str,bool]={}) -> Iterator[dict[str,bool]]:
  """Iterativley generate boolean assignments for the given variable set.

  @param variables list[int]
  """
  if not variables:
    yield assignment
    return

  var = variables[0]
  for value in (False, True):
    assignment[var] = value
    yield from generate_assignments(variables[1:], assignment)



def bruteforce(ex: SATExpression, verbose: bool = False) -> bool:

    verbose and print(f"Testing expression: " + str(ex) + " ", end="")

    for assignment in generate_assignments(list(ex.get_variables())):
        if not ex(assignment): continue

        verbose and print("SATISFIABLE")
        return True

    verbose and print("UNSATISFIABLE")
    return False


#!/usr/bin/env python3

import sys
import csv
import time
from typing import Iterator
import signal

# Import SAT classes
from ._SAT_utils_crystalball import SATExpression, SATClause, SATLiteral, Solution

__all__ = ["SATExpression", "SATClause", "SATLiteral", "Solution", "load_DIMACS_csv", "test_solver", "test_solver"]


class TimeoutException(Exception):
  pass


def load_DIMACS_csv(csv_path:str) -> Iterator[SATExpression]:
  # Load in test cases from DIMACS csv format
  # Generates SATExpression objects

  with open(csv_path, "r") as f:

    current_ex = None
    current_clauses = None
    satisfiable = None
    for record in csv.reader(f, delimiter=","):
      if not record:
        continue

      if record[0] == "c":
        # Beginning of new test case
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
          # Beginning of new clause
          if not item: continue
          item = int(item)
          if item == 0:
            current_ex.append(current_clause)
            current_clause = []
            continue

          current_clause.append(item)


def test_solver(solver, name: str, test_filename: str, out_filename: str, timeout: int = 300) -> None:
  # Given a solver function, test and benchmark
  # Get input files from test_filename (DIMACS csv format)
  # Write output to out_filename (name, kSAT, nvars, solution, runtime) (csv format)
  # Stop when testcase takes `timeout` seconds or more to run

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
        # Test case failed... End testing
        print(f"[INFO] Test Case Failed: {str(tc)}")
        print(f"\tCorrect output: {tc.solution}")
        print(f"\tProgram output: {sol}")
        print("[INFO] Status... Failure")
        break


      data.append((name, tc.ksat, tc.num_vars, tc.solution.value, runtime))
      i += 1

    except KeyboardInterrupt:
      # Interrupted... end testing
      print("[INFO] Interrupt recieved. Exiting...")
      break

    except TimeoutException:
      # Timeout reached... end testing
      print("[INFO] Timeout exceeded. Exiting...")
      break

    finally:
      signal.alarm(0)

  print("[INFO] Status... OK")
  print(f"[INFO] Passed {i} tests")

  print(f"[INFO] Saving results to {out_filename}")

  # Write results to output file
  with open(out_filename, "w") as f:
    writer = csv.writer(f, delimiter=",")
    for row in data:
      writer.writerow(row)



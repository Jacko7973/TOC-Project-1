#!/usr/bin/env python3

from enum import Enum
import math
import re


## Enums

class Solution(Enum):
    SATISFIABLE = "S"
    UNSATISFIABLE = "U"
    UNKNOWN = "?"


## Classes

class SATLiteral:
    # Class representing a single literal (negated? variable)

    def __init__(self, var: str, negate: bool) -> None:
        self.var = var
        self.negate = negate

    def __call__(self, assignment: bool) -> bool:
        return (assignment != self.negate)

    def __str__(self) -> str:
        return f"{'!' if self.negate else ''}{self.var}"

    def __int__(self) -> int:
        int_value = 0
        if self.var.isdigit():
            int_value = int(self.var)
        else:
            for i, char in enumerate(self.var):
                int_value += int((ord(char) - ord("a")) * math.pow(26, i))
        return int_value * (-1 if self.negate else 1)


    @staticmethod
    def from_str(s: str):
        m = re.match(r"(!)?([0-9a-zA-Z]+)", s)
        if not m or len(m.groups()) != 2:
            print(f"[INFO] Improperly formatted SATLiteral string: {s}")
            return None

        negate = (m.groups()[0] == "!")
        var = m.groups()[1]
        return SATLiteral(var, negate)


    @staticmethod
    def from_int(lit_int: int):
        var = str(abs(lit_int))
        negate = (lit_int < 0)
        return SATLiteral(var, negate)



class SATClause:
    # Class representing the logical OR of a set of literals

    def __init__(self, literals: list[SATLiteral]) -> None:
        self.literals = literals

    def __call__(self, assignments: dict[str, bool]) -> bool:
        # OR all of the literals together
        return any(l(assignments[l.var]) for l in self.literals)

    def __str__(self) -> str:
        return "(" + " | ".join(
                [f"{'!' if l.negate else ''}{l.var}" for l in self.literals]) + ")"


    def to_list(self) -> list[int]:
        # Convert to a clause list of integers
        clause_list = []
        for l in self.literals:
            clause_list.append(int(l))
        return clause_list


    @staticmethod
    def from_str(s: str):
        s_stripped = s.strip("()")
        literals = []
        for lit_str in s_stripped.split(" | "):
            lit = SATLiteral.from_str(lit_str)
            if not lit:
                print(f"[INFO] Improperly formatted SATClause string: {s}")
                return None
            literals.append(lit)

        return SATClause(literals)


    @staticmethod
    def from_list(l: list):
        literals = []
        for lit_int in l:
            lit = SATLiteral.from_int(lit_int)
            if not lit:
                print(f"[INFO] Improperly formatted SATClause list: {l}")
                return None
            literals.append(lit)

        return SATClause(literals)



    def get_variables(self) -> set[str]:
        var_set = set()
        for lit in self.literals:
            var_set.add(lit.var)

        return var_set



class SATExpression:
    # Class representing the logical AND of a set of clauses

    def __init__(self, clauses: list[SATClause], solution:Solution=Solution.UNKNOWN) -> None:
        self.clauses: list[SATClause] = clauses
        self.solution = solution

    def __call__(self, assignments: dict[str, bool]) -> bool:
        return all(c(assignments) for c in self.clauses)

    def __str__(self) -> str:
        return " & ".join(str(c) for c in self.clauses)


    def to_list(self) -> list[int]:
        # Convert to a wff list of integers
        ex_list = []
        for c in self.clauses:
            ex_list.append(c.to_list())
        return ex_list


    @staticmethod
    def from_str(s: str):
        clauses = []
        for c_str in s.split(" & "):
            c = SATClause.from_str(c_str)
            if not c:
                print(f"[INFO] Improperly formatted SATExpression string: {s}")
                return None
            clauses.append(c)

        return SATExpression(clauses)


    @staticmethod
    def from_list(l: list):
        clauses = []
        for c_list in l:
            c = SATClause.from_list(c_list)
            if not c:
                print(f"[INFO] Improperly formatted SATExpression list: {l}")
                return None
            clauses.append(c)

        return SATExpression(clauses)

    @property
    def num_vars(self):
        return len(self.get_variables())

    @property
    def ksat(self):
        return max(len(c.literals) for c in self.clauses)



    def get_variables(self) -> set[str]:
        var_set = set()
        for c in self.clauses:
            for lit in c.literals:
                var_set.add(lit.var)

        return var_set



#!/usr/bin/env python3
# TOC-Project-1-crystalball
# SAT_lib/_SAT_utils_crystalball.py
# Author: Jack O'Connor
# Date: 10/9/2024

import re


## Classes

class SATLiteral:

    def __init__(self, var: str, negate: bool) -> None:
        self.var = var
        self.negate = negate

    def __call__(self, assignment: bool) -> bool:
        return (assignment != self.negate)

    def __str__(self) -> str:
        return f"{'!' if self.negate else ''}{self.var}"

    @staticmethod
    def from_str(s: str):
        m = re.match(r"(!)?([a-z])", s)
        if not m or len(m.groups()) != 2:
            print(f"[INFO] Improperly formatted SATLiteral string: {s}")
            return None

        negate = (m.groups()[0] == "!")
        var = m.groups()[1]
        return SATLiteral(var, negate)



class SATClause:

    def __init__(self, literals: list[SATLiteral]) -> None:
        self.literals = literals

    def __call__(self, assignments: dict[str, bool]) -> bool:
        # OR all of the literals together
        return any(l(assignments[l.var]) for l in self.literals)

    def __str__(self) -> str:
        return "(" + " | ".join(
                [f"{'!' if l.negate else ''}{l.var}" for l in self.literals]) + ")"

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


    def get_variables(self) -> set[str]:
        var_set = set()
        for lit in self.literals:
            var_set.add(lit.var)

        return var_set



class SATExpression:

    def __init__(self, clauses: list[SATClause]) -> None:
        self.clauses: list[SATClause] = clauses

    def __call__(self, assignments: dict[str, bool]) -> bool:
        return all(c(assignments) for c in self.clauses)

    def __str__(self) -> str:
        return " & ".join(str(c) for c in self.clauses)

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



    def get_variables(self) -> set[str]:
        var_set = set()
        for c in self.clauses:
            for lit in c.literals:
                var_set.add(lit.var)

        return var_set


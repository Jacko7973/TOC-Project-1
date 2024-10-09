#!/usr/bin/python3

from SAT_lib import SATExpression, SATClause, SATLiteral

def simplify(expression: TwoSATExpression, var: str, value: bool) -> TwoSATExpression:
    clauses_prime = []
    for clause in expression.clauses:
        literals_prime = []
        clause_satisfied = False
        for literal in clause.literals:
            if literal.var == var:
                if literal(value):
                    clause_satisfied = True
                    break
            else:
                literals_prime.append(literal)
        if not clause_satisfied and literals_prime:
            clauses_prime.append(SATClause(literals_prime))
    return TwoSATExpression(clauses_prime)

def dpll(expression: TwoSATExpression, interpretation: dict[str,bool] = None) -> dict[str,bool] | None:
    if interpretation is None:
        interpretation = {}

    # Base case: if ∆ = ∅, return I beacuses its satisfiable
    if not expression.clauses:
        return interpretation

    # Base case: if square ∈ ∆, return unsatisfiable
    if any(not clause.literals for clause in expression.clauses):
        return None

    # Unit propagation
    for clause in expression.clauses:
        if len(clause.literals) == 1:
            lit = clause.literals[0]
            interpretation_prime = interpretation.copy()
            interpretation_prime[lit.var] = not lit.negate
            return dpll(simplify(expression, lit.var, not lit.negate), interpretation_prime)

    # Splitting rule
    # Select some variable v which occurs in ∆
    var = next(iter(set(lit.var for clause in expression.clauses for lit in clause.literals) - set(interpretation.keys())))

    # Try True (d = T)
    interpretation_prime = interpretation.copy()
    interpretation_prime[var] = True
    result = dpll(simplify(expression, var, True), interpretation_prime)
    if result is not None:
        return result

    # Try False (d = F)
    interpretation_prime = interpretation.copy()
    interpretation_prime[var] = False
    return dpll(simplify(expression, var, False), interpretation_prime)   

def main():
    pass

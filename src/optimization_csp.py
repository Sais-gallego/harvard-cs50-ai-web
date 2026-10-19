"""
Harvard CS50 / CS50AI: Optimization and Constraint Satisfaction Problems (CSP).
Implements the AC-3 (Arc Consistency 3) algorithm and Backtracking Search with MRV heuristic.
"""

from typing import Dict, Set, List, Optional, Tuple


class Variable:
    def __init__(self, i: int, j: int, direction: str, length: int):
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells: List[Tuple[int, int]] = []
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if direction == "down" else 0),
                 self.j + (k if direction == "across" else 0))
            )

    def __hash__(self):
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            isinstance(other, Variable) and
            self.i == other.i and
            self.j == other.j and
            self.direction == other.direction and
            self.length == other.length
        )

    def __repr__(self):
        return f"Var({self.i}, {self.j}, {self.direction}, len={self.length})"


class CSPCrossword:
    """
    Crossword Constraint Satisfaction Problem formulation.
    """

    def __init__(self, words: Set[str], variables: Set[Variable]):
        self.words = set(words)
        self.variables = set(variables)
        self.domains: Dict[Variable, Set[str]] = {v: set(self.words) for v in self.variables}
        self.overlaps: Dict[Tuple[Variable, Variable], Optional[Tuple[int, int]]] = {}

        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                overlap = None
                for idx1, c1 in enumerate(v1.cells):
                    for idx2, c2 in enumerate(v2.cells):
                        if c1 == c2:
                            overlap = (idx1, idx2)
                            break
                    if overlap:
                        break
                self.overlaps[(v1, v2)] = overlap

    def enforce_node_consistency(self) -> None:
        """Removes words that don't match variable length from domains."""
        for var in self.variables:
            self.domains[var] = {w for w in self.domains[var] if len(w) == var.length}

    def revise(self, x: Variable, y: Variable) -> bool:
        """
        Enforces arc consistency for (x, y).
        Removes word from domain of x if no word in domain of y satisfies the overlap.
        """
        revised = False
        overlap = self.overlaps.get((x, y))
        if overlap is None:
            return False

        idx_x, idx_y = overlap
        to_remove = set()

        for word_x in self.domains[x]:
            satisfies = any(word_x[idx_x] == word_y[idx_y] for word_y in self.domains[y] if word_x != word_y)
            if not satisfies:
                to_remove.add(word_x)
                revised = True

        self.domains[x] -= to_remove
        return revised

    def ac3(self, arcs: Optional[List[Tuple[Variable, Variable]]] = None) -> bool:
        """
        Runs the AC-3 algorithm to enforce arc consistency across the network.
        """
        if arcs is None:
            queue = [arc for arc, overlap in self.overlaps.items() if overlap is not None]
        else:
            queue = list(arcs)

        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                # Re-check arcs into x from other neighbors
                for z in self.variables:
                    if z != x and z != y and self.overlaps.get((z, x)) is not None:
                        queue.append((z, x))
        return True

    def is_consistent(self, assignment: Dict[Variable, str]) -> bool:
        """Checks if a partial or full assignment is consistent with all constraints."""
        # Uniqueness
        values = list(assignment.values())
        if len(values) != len(set(values)):
            return False

        # Length and binary overlap constraints
        for var, word in assignment.items():
            if len(word) != var.length:
                return False

        for (v1, v2), overlap in self.overlaps.items():
            if overlap is not None and v1 in assignment and v2 in assignment:
                idx1, idx2 = overlap
                if assignment[v1][idx1] != assignment[v2][idx2]:
                    return False

        return True

    def backtrack(self, assignment: Dict[Variable, str]) -> Optional[Dict[Variable, str]]:
        """Backtracking search with MRV heuristic."""
        if len(assignment) == len(self.variables):
            return assignment

        # Select unassigned variable with Minimum Remaining Values (MRV)
        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.domains[v]))

        for val in sorted(self.domains[var]):
            new_assign = dict(assignment)
            new_assign[var] = val
            if self.is_consistent(new_assign):
                result = self.backtrack(new_assign)
                if result is not None:
                    return result

        return None

    def solve(self) -> Optional[Dict[Variable, str]]:
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack({})

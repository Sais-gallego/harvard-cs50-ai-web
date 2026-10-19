"""
Harvard CS50 / CS50AI: Knowledge and Propositional Logic.
Implements Model Checking (TT-Entails) and Minesweeper Knowledge Inference Engine.
"""

from typing import Set, Dict, List, Optional, Tuple


class Sentence:
    def evaluate(self, model: Dict[str, bool]) -> bool:
        raise NotImplementedError

    def formula(self) -> str:
        return ""

    def symbols(self) -> Set[str]:
        return set()


class Symbol(Sentence):
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return bool(model.get(self.name, False))

    def formula(self) -> str:
        return self.name

    def symbols(self) -> Set[str]:
        return {self.name}


class Not(Sentence):
    def __init__(self, operand: Sentence):
        self.operand = operand

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return not self.operand.evaluate(model)

    def formula(self) -> str:
        return f"¬{self.operand.formula()}"

    def symbols(self) -> Set[str]:
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *conjuncts: Sentence):
        self.conjuncts = list(conjuncts)

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return all(c.evaluate(model) for c in self.conjuncts)

    def symbols(self) -> Set[str]:
        s = set()
        for c in self.conjuncts:
            s |= c.symbols()
        return s


class Or(Sentence):
    def __init__(self, *disjuncts: Sentence):
        self.disjuncts = list(disjuncts)

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return any(d.evaluate(model) for d in self.disjuncts)

    def symbols(self) -> Set[str]:
        s = set()
        for d in self.disjuncts:
            s |= d.symbols()
        return s


class Implication(Sentence):
    def __init__(self, antecedent: Sentence, consequent: Sentence):
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def symbols(self) -> Set[str]:
        return self.antecedent.symbols() | self.consequent.symbols()


class Biconditional(Sentence):
    def __init__(self, left: Sentence, right: Sentence):
        self.left = left
        self.right = right

    def evaluate(self, model: Dict[str, bool]) -> bool:
        return self.left.evaluate(model) == self.right.evaluate(model)

    def symbols(self) -> Set[str]:
        return self.left.symbols() | self.right.symbols()


def check_all(knowledge: Sentence, query: Sentence, symbols: List[str], model: Dict[str, bool]) -> bool:
    if not symbols:
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    p = symbols[0]
    rest = symbols[1:]
    # True branch
    model_true = dict(model)
    model_true[p] = True
    # False branch
    model_false = dict(model)
    model_false[p] = False
    return check_all(knowledge, query, rest, model_true) and check_all(knowledge, query, rest, model_false)


def model_check(knowledge: Sentence, query: Sentence) -> bool:
    """Returns True if knowledge entails query (KB |= alpha)."""
    symbols = list(knowledge.symbols() | query.symbols())
    return check_all(knowledge, query, symbols, {})


# --- Minesweeper Logical Inference ---

Coord = Tuple[int, int]


class MinesweeperSentence:
    """
    Logical statement about a set of cells having a specific count of mines.
    e.g. { (0, 1), (1, 1) } = 1
    """

    def __init__(self, cells: Set[Coord], count: int):
        self.cells = set(cells)
        self.count = count

    def known_mines(self) -> Set[Coord]:
        if len(self.cells) == self.count and self.count > 0:
            return set(self.cells)
        return set()

    def known_safes(self) -> Set[Coord]:
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell: Coord) -> None:
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell: Coord) -> None:
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    AI Agent that plays Minesweeper using propositional logical deduction.
    """

    def __init__(self, height: int = 8, width: int = 8):
        self.height = height
        self.width = width
        self.moves_made: Set[Coord] = set()
        self.mines: Set[Coord] = set()
        self.safes: Set[Coord] = set()
        self.knowledge: List[MinesweeperSentence] = []

    def mark_mine(self, cell: Coord) -> None:
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell: Coord) -> None:
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell: Coord, count: int) -> None:
        """
        Called when a safe cell is revealed with its count of surrounding mines.
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 1. Identify undetermined neighbors
        undetermined_neighbors: Set[Coord] = set()
        r, c = cell
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    if (nr, nc) in self.mines:
                        count -= 1
                    elif (nr, nc) not in self.safes:
                        undetermined_neighbors.add((nr, nc))

        # 2. Add new sentence to knowledge base
        if undetermined_neighbors:
            self.knowledge.append(MinesweeperSentence(undetermined_neighbors, count))

        # 3. Repeatedly deduce safe and mine cells and infer new subset sentences
        changed = True
        while changed:
            changed = False

            # Infer from individual sentences
            new_safes: Set[Coord] = set()
            new_mines: Set[Coord] = set()
            for s in self.knowledge:
                new_safes |= s.known_safes()
                new_mines |= s.known_mines()

            for safe in new_safes:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    changed = True

            for mine in new_mines:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    changed = True

            # Prune empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

            # Subset deduction: if s1.cells subset of s2.cells:
            # (s2 - s1) = count2 - count1
            new_inferred: List[MinesweeperSentence] = []
            for i, s1 in enumerate(self.knowledge):
                for j, s2 in enumerate(self.knowledge):
                    if i != j and s1.cells.issubset(s2.cells):
                        diff_cells = s2.cells - s1.cells
                        diff_count = s2.count - s1.count
                        if diff_cells:
                            candidate = MinesweeperSentence(diff_cells, diff_count)
                            if candidate not in new_inferred and not any(
                                existing.cells == diff_cells and existing.count == diff_count
                                for existing in self.knowledge
                            ):
                                new_inferred.append(candidate)
                                changed = True
            self.knowledge.extend(new_inferred)

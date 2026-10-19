import unittest
from src.knowledge_and_logic import (
    Symbol, Not, And, Or, Implication, Biconditional, model_check, MinesweeperAI
)


class TestKnowledgeAndLogic(unittest.TestCase):
    def test_propositional_logic_model_check(self):
        # Knights and Knaves puzzle:
        # A says "I am both a knight and a knave."
        AKnight = Symbol("AKnight")
        AKnave = Symbol("AKnave")

        # Knowledge: A is either knight or knave, not both
        knowledge = And(
            Or(AKnight, AKnave),
            Not(And(AKnight, AKnave)),
            # If A is knight, sentence is true; if knave, false
            Biconditional(AKnight, And(AKnight, AKnave))
        )

        # A must be a knave
        self.assertTrue(model_check(knowledge, AKnave))
        self.assertFalse(model_check(knowledge, AKnight))

    def test_minesweeper_ai_inference(self):
        ai = MinesweeperAI(height=4, width=4)

        # Mark (0, 0) safe with count 1
        # Neighbors of (0, 0) are (0, 1), (1, 0), (1, 1)
        ai.add_knowledge((0, 0), 1)

        # Now mark (0, 2) safe with count 0
        # Neighbors of (0, 2) include (0, 1), (1, 1), (0, 3), (1, 2), (1, 3)
        # All neighbors of (0, 2) must be safe!
        ai.add_knowledge((0, 2), 0)

        # Since (0, 1) and (1, 1) are known safes, the only remaining neighbor of (0, 0) is (1, 0)
        # Therefore, (1, 0) MUST BE A MINE!
        self.assertIn((1, 0), ai.mines)
        self.assertIn((0, 1), ai.safes)
        self.assertIn((1, 1), ai.safes)


if __name__ == "__main__":
    unittest.main()

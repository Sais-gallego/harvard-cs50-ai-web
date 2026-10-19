import unittest
from src.optimization_csp import Variable, CSPCrossword


class TestOptimizationCSP(unittest.TestCase):
    def test_csp_crossword_solve_with_ac3(self):
        # Two overlapping words forming a cross:
        # v1: across at (0, 0), length 4
        # v2: down at (0, 1), length 4
        # Overlap at cell (0, 1): v1 index 1, v2 index 0
        v1 = Variable(0, 0, "across", 4)
        v2 = Variable(0, 1, "down", 4)

        words = {"NOTE", "OATS", "SEAT", "NINE"}
        csp = CSPCrossword(words, {v1, v2})

        solution = csp.solve()
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 2)

        # Word for v1 and word for v2 must be distinct
        self.assertNotEqual(solution[v1], solution[v2])

        # Overlap check: v1[1] == v2[0]
        # In NOTE (idx 1 = 'O') and OATS (idx 0 = 'O'): matches!
        self.assertEqual(solution[v1][1], solution[v2][0])

    def test_csp_node_consistency(self):
        v1 = Variable(0, 0, "across", 3)
        words = {"CAT", "DOG", "ELEPHANT", "BIRD"}
        csp = CSPCrossword(words, {v1})
        csp.enforce_node_consistency()

        self.assertEqual(csp.domains[v1], {"CAT", "DOG"})


if __name__ == "__main__":
    unittest.main()

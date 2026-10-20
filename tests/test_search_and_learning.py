"""
Unit Tests for CS50 AI Search, Minimax, Q-Learning, and k-NN
Author: Sergio Andrés Ipuz Saavedra (@Sais-gallego)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.search_and_games import TicTacToeAI, Node, StackFrontier, QueueFrontier, AStarFrontier
from src.learning_and_rl import NimAI, KNNClassifier


class TestSearchAndLearning(unittest.TestCase):

    def test_dfs_and_bfs_frontiers(self):
        # DFS (LIFO)
        dfs = StackFrontier()
        dfs.add(Node("A"))
        dfs.add(Node("B"))
        self.assertEqual(dfs.remove().state, "B")
        self.assertEqual(dfs.remove().state, "A")

        # BFS (FIFO)
        bfs = QueueFrontier()
        bfs.add(Node("A"))
        bfs.add(Node("B"))
        self.assertEqual(bfs.remove().state, "A")
        self.assertEqual(bfs.remove().state, "B")

    def test_astar_frontier(self):
        # Heuristic: distance to 0
        frontier = AStarFrontier(heuristic_func=lambda s: abs(s))
        frontier.add(Node(10, path_cost=5))  # total 15
        frontier.add(Node(2, path_cost=1))   # total 3
        frontier.add(Node(7, path_cost=2))   # total 9

        self.assertEqual(frontier.remove().state, 2)
        self.assertEqual(frontier.remove().state, 7)
        self.assertEqual(frontier.remove().state, 10)

    def test_tictactoe_minimax_optimal_blocking(self):
        # X is about to win on top row:
        # X X _
        # O O _
        # _ _ _
        board = [
            ["X", "X", None],
            ["O", "O", None],
            [None, None, None]
        ]
        # It's X's turn (2 Xs, 2 Os -> count_x == count_o -> X moves)
        self.assertEqual(TicTacToeAI.player(board), "X")
        action = TicTacToeAI.minimax(board)
        # Optimal move for X is winning immediately at (0, 2)
        self.assertEqual(action, (0, 2))

    def test_tictactoe_minimax_defense(self):
        # Board state near endgame where O must make critical block to prevent X from winning:
        # X O X
        # X X O
        # O _ _
        # Count X: 4, Count O: 3 -> O's turn!
        # Actions: (2, 1) and (2, 2)
        # If O plays (2, 1), X can win; if O plays (2, 2), O secures a draw (utility 0)!
        board = [
            ["X", "O", "X"],
            ["X", "X", "O"],
            ["O", None, None]
        ]
        self.assertEqual(TicTacToeAI.player(board), "O")
        action = TicTacToeAI.minimax(board)
        # O chooses (2, 2) to prevent X from winning and secure draw
        self.assertEqual(action, (2, 2))

    def test_nim_q_learning_update(self):
        ai = NimAI(alpha=0.5, epsilon=0.0, gamma=1.0)
        state = (1, 2)
        action = (1, 1)

        # Initial Q is 0
        self.assertEqual(ai.get_q_value(state, action), 0.0)

        # Bellman update with reward=1, future=0
        ai.update_q_value(state, action, old_q=0.0, reward=1.0, future_rewards=0.0)
        # 0 + 0.5 * (1 + 0 - 0) = 0.5
        self.assertEqual(ai.get_q_value(state, action), 0.5)

        # ai.choose_action greedy should pick the higher Q action
        other_action = (1, 2)
        chosen = ai.choose_action(state, [action, other_action], epsilon=False)
        self.assertEqual(chosen, action)

    def test_knn_classifier_shopping(self):
        knn = KNNClassifier(k=3)
        train_x = [
            [1.0, 1.0],
            [1.2, 0.9],
            [0.8, 1.1],
            [5.0, 5.0],
            [5.2, 4.8],
            [4.9, 5.1]
        ]
        train_y = [0, 0, 0, 1, 1, 1]
        knn.fit(train_x, train_y)

        # Test sample near cluster 0
        pred0 = knn.predict_one([1.1, 1.0])
        self.assertEqual(pred0, 0)

        # Test sample near cluster 1
        pred1 = knn.predict_one([5.1, 5.0])
        self.assertEqual(pred1, 1)

        # Evaluation metrics
        metrics = KNNClassifier.evaluate([0, 1], [0, 1])
        self.assertEqual(metrics["accuracy"], 1.0)
        self.assertEqual(metrics["sensitivity"], 1.0)
        self.assertEqual(metrics["specificity"], 1.0)


if __name__ == "__main__":
    unittest.main()

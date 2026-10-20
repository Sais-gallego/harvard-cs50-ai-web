"""
Harvard CS50 AI - Search & Adversarial Games (Week 0)
Author: Sergio Andrés Ipuz Saavedra (@Sais-gallego)
Harvard University CS50's Introduction to Artificial Intelligence with Python
"""

import math
from typing import List, Tuple, Optional, Set, Dict


class Node:
    """Represents a state node in the search frontier."""
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


class StackFrontier:
    """Depth-First Search (DFS) Frontier (LIFO)."""
    def __init__(self):
        self.frontier = []

    def add(self, node: Node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self) -> Node:
        if self.empty():
            raise Exception("Frontier is empty")
        return self.frontier.pop()


class QueueFrontier(StackFrontier):
    """Breadth-First Search (BFS) Frontier (FIFO)."""
    def remove(self) -> Node:
        if self.empty():
            raise Exception("Frontier is empty")
        return self.frontier.pop(0)


class AStarFrontier:
    """A* Priority Queue Frontier ordered by f(n) = g(n) + h(n)."""
    def __init__(self, heuristic_func):
        self.frontier: List[Tuple[float, Node]] = []
        self.heuristic = heuristic_func

    def add(self, node: Node):
        priority = node.path_cost + self.heuristic(node.state)
        self.frontier.append((priority, node))
        self.frontier.sort(key=lambda x: x[0])

    def empty(self):
        return len(self.frontier) == 0

    def remove(self) -> Node:
        if self.empty():
            raise Exception("Frontier is empty")
        return self.frontier.pop(0)[1]


class TicTacToeAI:
    """
    Minimax Adversarial Search with Alpha-Beta Pruning.
    X is the maximizing player (+1), O is the minimizing player (-1).
    Empty cells are None.
    """

    X = "X"
    O = "O"
    EMPTY = None

    @classmethod
    def initial_state(cls):
        """Returns starting board 3x3 of empty cells."""
        return [[cls.EMPTY, cls.EMPTY, cls.EMPTY] for _ in range(3)]

    @classmethod
    def player(cls, board) -> str:
        """Determine whose turn it is to move."""
        count_x = sum(row.count(cls.X) for row in board)
        count_o = sum(row.count(cls.O) for row in board)
        return cls.O if count_x > count_o else cls.X

    @classmethod
    def actions(cls, board) -> Set[Tuple[int, int]]:
        """Returns set of all possible coordinates (i, j) for next move."""
        return {(i, j) for i in range(3) for j in range(3) if board[i][j] is cls.EMPTY}

    @classmethod
    def result(cls, board, action: Tuple[int, int]):
        """Returns the resulting board state after taking action (i, j)."""
        i, j = action
        if board[i][j] is not cls.EMPTY:
            raise ValueError(f"Invalid action on occupied cell: {action}")
        new_board = [row[:] for row in board]
        new_board[i][j] = cls.player(board)
        return new_board

    @classmethod
    def winner(cls, board) -> Optional[str]:
        """Returns winner ('X' or 'O'), or None if no winner."""
        # Check rows and columns
        for i in range(3):
            if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]
            if board[0][i] and board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]

        # Check diagonals
        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]

        return None

    @classmethod
    def terminal(cls, board) -> bool:
        """Returns True if game is over (winner found or board is full)."""
        if cls.winner(board) is not None:
            return True
        return all(cell is not cls.EMPTY for row in board for cell in row)

    @classmethod
    def utility(cls, board) -> int:
        """Returns 1 if X won, -1 if O won, 0 if draw."""
        win = cls.winner(board)
        if win == cls.X:
            return 1
        elif win == cls.O:
            return -1
        return 0

    @classmethod
    def minimax(cls, board) -> Optional[Tuple[int, int]]:
        """
        Returns optimal action (i, j) using Alpha-Beta Pruning Minimax.
        """
        if cls.terminal(board):
            return None

        current_player = cls.player(board)

        if current_player == cls.X:
            best_val = -math.inf
            best_action = None
            alpha = -math.inf
            beta = math.inf
            for action in cls.actions(board):
                val = cls._min_value(cls.result(board, action), alpha, beta)
                if val > best_val:
                    best_val = val
                    best_action = action
                alpha = max(alpha, best_val)
            return best_action
        else:
            best_val = math.inf
            best_action = None
            alpha = -math.inf
            beta = math.inf
            for action in cls.actions(board):
                val = cls._max_value(cls.result(board, action), alpha, beta)
                if val < best_val:
                    best_val = val
                    best_action = action
                beta = min(beta, best_val)
            return best_action

    @classmethod
    def _max_value(cls, board, alpha, beta) -> int:
        if cls.terminal(board):
            return cls.utility(board)
        v = -math.inf
        for action in cls.actions(board):
            v = max(v, cls._min_value(cls.result(board, action), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    @classmethod
    def _min_value(cls, board, alpha, beta) -> int:
        if cls.terminal(board):
            return cls.utility(board)
        v = math.inf
        for action in cls.actions(board):
            v = min(v, cls._max_value(cls.result(board, action), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

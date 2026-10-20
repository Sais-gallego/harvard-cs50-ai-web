"""
Harvard CS50 AI - Machine Learning & Reinforcement Learning (Week 4)
Author: Sergio Andrés Ipuz Saavedra (@Sais-gallego)
Harvard University CS50's Introduction to Artificial Intelligence with Python
"""

import math
import random
from typing import Dict, List, Tuple, Optional


class NimAI:
    """
    Q-Learning Reinforcement Learning Agent for the game of Nim.
    Learns state-action values Q(s, a) via Bellman update equation:
    Q(s, a) <- Q(s, a) + alpha * (reward + gamma * max_a' Q(s', a') - Q(s, a))
    """

    def __init__(self, alpha: float = 0.5, epsilon: float = 0.1, gamma: float = 1.0):
        self.q: Dict[Tuple[Tuple[int, ...], Tuple[int, int]], float] = {}
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

    def get_q_value(self, state: Tuple[int, ...], action: Tuple[int, int]) -> float:
        """Returns Q(state, action), default 0.0 if unseen."""
        return self.q.get((tuple(state), action), 0.0)

    def update_q_value(
        self,
        state: Tuple[int, ...],
        action: Tuple[int, int],
        old_q: float,
        reward: float,
        future_rewards: float
    ):
        """Perform Bellman equation update."""
        new_value = old_q + self.alpha * (reward + (self.gamma * future_rewards) - old_q)
        self.q[(tuple(state), action)] = new_value

    def best_future_reward(self, state: Tuple[int, ...], available_actions: List[Tuple[int, int]]) -> float:
        """Calculate max_a' Q(s', a'). If no actions remain, returns 0.0."""
        if not available_actions:
            return 0.0
        return max(self.get_q_value(state, act) for act in available_actions)

    def choose_action(self, state: Tuple[int, ...], available_actions: List[Tuple[int, int]], epsilon: Optional[bool] = None) -> Tuple[int, int]:
        """
        Choose action using epsilon-greedy exploration strategy.
        If epsilon is True, explores randomly with probability self.epsilon.
        If epsilon is False, greedily chooses highest Q-value.
        """
        if not available_actions:
            raise ValueError("No actions available")

        use_epsilon = self.epsilon if epsilon is None or epsilon is True else 0.0

        if random.random() < use_epsilon:
            return random.choice(available_actions)

        # Exploit: pick action with maximum Q-value
        best_reward = -math.inf
        best_actions = []
        for act in available_actions:
            val = self.get_q_value(state, act)
            if val > best_reward:
                best_reward = val
                best_actions = [act]
            elif val == best_reward:
                best_actions.append(act)

        return random.choice(best_actions)


class KNNClassifier:
    """
    k-Nearest Neighbors (k-NN) Supervised Learning Classifier
    for CS50 Shopping revenue prediction and customer classification.
    """

    def __init__(self, k: int = 3):
        self.k = k
        self.train_features: List[List[float]] = []
        self.train_labels: List[int] = []

    def fit(self, features: List[List[float]], labels: List[int]):
        """Store training dataset."""
        self.train_features = features
        self.train_labels = labels

    @staticmethod
    def euclidean_distance(p1: List[float], p2: List[float]) -> float:
        """Calculate Euclidean distance between two feature vectors."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def predict_one(self, sample: List[float]) -> int:
        """Predict label for single feature vector based on majority vote of k nearest neighbors."""
        distances = []
        for idx, train_vec in enumerate(self.train_features):
            dist = self.euclidean_distance(sample, train_vec)
            distances.append((dist, self.train_labels[idx]))

        # Sort by shortest distance
        distances.sort(key=lambda x: x[0])
        k_neighbors = distances[:self.k]

        votes = {}
        for _, label in k_neighbors:
            votes[label] = votes.get(label, 0) + 1

        # Return majority vote label
        return max(votes.items(), key=lambda x: x[1])[0]

    def predict(self, test_features: List[List[float]]) -> List[int]:
        """Predict labels for batch of test samples."""
        return [self.predict_one(sample) for sample in test_features]

    @staticmethod
    def evaluate(actual: List[int], predicted: List[int]) -> Dict[str, float]:
        """
        Calculate Accuracy, Sensitivity (True Positive Rate), and Specificity (True Negative Rate).
        """
        tp = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 1)
        tn = sum(1 for a, p in zip(actual, predicted) if a == 0 and p == 0)
        fp = sum(1 for a, p in zip(actual, predicted) if a == 0 and p == 1)
        fn = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 0)

        total = len(actual)
        accuracy = (tp + tn) / total if total > 0 else 0.0
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

        return {
            "accuracy": round(accuracy, 4),
            "sensitivity": round(sensitivity, 4),
            "specificity": round(specificity, 4)
        }

import unittest
from src.uncertainty_and_markov import transition_model, iterate_pagerank, HeredityBayes


class TestUncertaintyAndMarkov(unittest.TestCase):
    def test_pagerank_markov_iteration(self):
        # 4-page corpus
        corpus = {
            "1.html": {"2.html"},
            "2.html": {"3.html", "1.html"},
            "3.html": {"2.html", "4.html"},
            "4.html": {"2.html"}
        }

        ranks = iterate_pagerank(corpus, damping_factor=0.85)
        # Ranks must sum to 1.0
        self.assertAlmostEqual(sum(ranks.values()), 1.0, places=4)

        # 2.html has the highest number of incoming links and should have highest PageRank
        self.assertTrue(ranks["2.html"] > ranks["1.html"])
        self.assertTrue(ranks["2.html"] > ranks["4.html"])

    def test_transition_model_distribution(self):
        corpus = {
            "A": {"B"},
            "B": {"A", "C"},
            "C": set()  # Sink page
        }
        dist = transition_model(corpus, "A", damping_factor=0.85)
        self.assertAlmostEqual(sum(dist.values()), 1.0, places=4)
        # B should have base (0.15 / 3) + link (0.85 / 1) = 0.05 + 0.85 = 0.90
        self.assertAlmostEqual(dist["B"], 0.90, places=4)

    def test_heredity_bayesian_probability(self):
        people = {
            "Harry": {"name": "Harry", "mother": "Lily", "father": "James"},
            "James": {"name": "James", "mother": None, "father": None},
            "Lily": {"name": "Lily", "mother": None, "father": None}
        }
        # Probability when Harry has 1 gene and trait, Lily has 0 genes, James has 2 genes
        prob = HeredityBayes.joint_probability(
            people,
            one_gene={"Harry"},
            two_genes={"James"},
            have_trait={"Harry"}
        )
        self.assertGreater(prob, 0.0)
        self.assertLess(prob, 1.0)


if __name__ == "__main__":
    unittest.main()

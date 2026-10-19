"""
Harvard CS50 / CS50AI: Uncertainty, Probability and Markov Chains.
Implements PageRank (Random Surfer & Iterative Markov Chain) and Heredity Bayesian Model.
"""

import random
from typing import Dict, Set, List


def transition_model(corpus: Dict[str, Set[str]], page: str, damping_factor: float = 0.85) -> Dict[str, float]:
    """
    Returns probability distribution over pages that a random surfer will visit next.
    """
    n = len(corpus)
    if n == 0:
        return {}

    dist: Dict[str, float] = {}
    links = corpus.get(page, set())

    # If page has no links, treat as having links to all pages in corpus
    if not links:
        for p in corpus:
            dist[p] = 1.0 / n
        return dist

    # Base random jump probability for every page
    base_prob = (1.0 - damping_factor) / n
    for p in corpus:
        dist[p] = base_prob

    # Additional probability for linked pages
    link_prob = damping_factor / len(links)
    for linked_p in links:
        dist[linked_p] += link_prob

    return dist


def sample_pagerank(corpus: Dict[str, Set[str]], damping_factor: float = 0.85, n: int = 10000) -> Dict[str, float]:
    """
    Estimates PageRank by sampling n visits in a random surfer Markov process.
    """
    pages = list(corpus.keys())
    if not pages:
        return {}

    counts: Dict[str, int] = {p: 0 for p in pages}
    curr_page = random.choice(pages)
    counts[curr_page] += 1

    for _ in range(n - 1):
        probs = transition_model(corpus, curr_page, damping_factor)
        choices = list(probs.keys())
        weights = list(probs.values())
        curr_page = random.choices(choices, weights=weights, k=1)[0]
        counts[curr_page] += 1

    return {p: count / n for p, count in counts.items()}


def iterate_pagerank(corpus: Dict[str, Set[str]], damping_factor: float = 0.85, threshold: float = 0.001) -> Dict[str, float]:
    """
    Calculates exact PageRank values by iteratively applying the Markov transition formula
    until values change by less than threshold.
    """
    n = len(corpus)
    if n == 0:
        return {}

    # Initialize uniformly: 1 / N
    ranks: Dict[str, float] = {p: 1.0 / n for p in corpus}

    # Normalize pages with 0 outgoing links to link to all pages
    norm_corpus: Dict[str, Set[str]] = {}
    for p, links in corpus.items():
        norm_corpus[p] = set(corpus.keys()) if not links else set(links)

    while True:
        new_ranks: Dict[str, float] = {}
        max_diff = 0.0

        for p in corpus:
            # Base probability
            rank_sum = 0.0
            for candidate, links in norm_corpus.items():
                if p in links:
                    rank_sum += ranks[candidate] / len(links)

            new_ranks[p] = ((1.0 - damping_factor) / n) + (damping_factor * rank_sum)
            diff = abs(new_ranks[p] - ranks[p])
            if diff > max_diff:
                max_diff = diff

        ranks = new_ranks
        if max_diff < threshold:
            break

    # Normalize so sum is exactly 1.0
    total = sum(ranks.values())
    return {p: r / total for p, r in ranks.items()}


class HeredityBayes:
    """
    Computes joint probability of genetic traits and copies of a mutated gene across family pedigrees.
    """

    PROBS = {
        "gene": {2: 0.01, 1: 0.03, 0: 0.96},
        "trait": {
            2: {True: 0.65, False: 0.35},
            1: {True: 0.56, False: 0.44},
            0: {True: 0.01, False: 0.99},
        },
        "mutation": 0.01,
    }

    @staticmethod
    def joint_probability(
        people: Dict[str, Dict],
        one_gene: Set[str],
        two_genes: Set[str],
        have_trait: Set[str]
    ) -> float:
        """
        Computes joint probability of the entire Bayesian network.
        """
        joint_prob = 1.0

        for person, data in people.items():
            # Determine number of genes
            if person in two_genes:
                genes = 2
            elif person in one_gene:
                genes = 1
            else:
                genes = 0

            trait = person in have_trait

            # 1. Gene probability
            mother = data.get("mother")
            father = data.get("father")

            if not mother and not father:
                # Prior probability
                gene_prob = HeredityBayes.PROBS["gene"][genes]
            else:
                # Calculate inheritance from parents
                assert mother is not None and father is not None
                p_mom = HeredityBayes._pass_gene_prob(mother, one_gene, two_genes)
                p_dad = HeredityBayes._pass_gene_prob(father, one_gene, two_genes)

                if genes == 2:
                    gene_prob = p_mom * p_dad
                elif genes == 1:
                    gene_prob = p_mom * (1 - p_dad) + (1 - p_mom) * p_dad
                else:
                    gene_prob = (1 - p_mom) * (1 - p_dad)

            # 2. Trait probability conditional on genes
            trait_prob = HeredityBayes.PROBS["trait"][genes][trait]

            joint_prob *= gene_prob * trait_prob

        return joint_prob

    @staticmethod
    def _pass_gene_prob(parent: str, one_gene: Set[str], two_genes: Set[str]) -> float:
        mut = HeredityBayes.PROBS["mutation"]
        if parent in two_genes:
            return 1.0 - mut
        elif parent in one_gene:
            return 0.5
        else:
            return mut

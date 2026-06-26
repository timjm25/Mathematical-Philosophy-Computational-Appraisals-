import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from engine.conjecture_ranker import ConjectureRanker, ConjectureScore
from engine.knowledge_graph import MathKnowledgeGraph
from engine.embedding_engine import EmbeddingEngine
from data.mock_corpus import get_concepts, get_relations


def _setup():
    concepts = get_concepts()
    kg = MathKnowledgeGraph()
    for c in concepts:
        kg.add_concept(c)
    for r in get_relations():
        kg.add_relation(r["source_id"], r["target_id"], r["relation_type"])
    emb = EmbeddingEngine(n_components=20)
    emb.fit(concepts)
    return concepts, kg, emb


def _get_conjecture(concepts):
    return next(c for c in concepts if c.get("concept_type") == "conjecture" and not c.get("proven", True))


class TestScoreConjecture:
    def test_returns_conjecture_score(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        score = ranker.score_conjecture(conj, kg, emb)
        assert isinstance(score, ConjectureScore)

    def test_novelty_in_range(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        score = ranker.score_conjecture(conj, kg, emb)
        assert 0.0 <= score.novelty_score <= 1.0

    def test_importance_in_range(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        score = ranker.score_conjecture(conj, kg, emb)
        assert 0.0 <= score.importance_score <= 1.0

    def test_connectivity_in_range(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        score = ranker.score_conjecture(conj, kg, emb)
        assert 0.0 <= score.connectivity_score <= 1.0

    def test_expected_downstream_nonneg(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        score = ranker.score_conjecture(conj, kg, emb)
        assert score.expected_downstream >= 0

    def test_complexity_is_valid(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        score = ranker.score_conjecture(conj, kg, emb)
        assert score.predicted_proof_complexity in ("elementary", "moderate", "deep", "exceptional")

    def test_roadmap_nonempty(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        score = ranker.score_conjecture(conj, kg, emb)
        assert len(score.research_roadmap) > 0


class TestRankConjectures:
    def test_rank_conjectures_returns_list(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        scores = ranker.rank_conjectures(kg, emb)
        assert isinstance(scores, list)

    def test_only_open_conjectures_ranked(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        scores = ranker.rank_conjectures(kg, emb)
        for s in scores:
            c = kg.get_concept(s.concept_id)
            assert c is not None
            assert c.get("concept_type") == "conjecture"
            assert not c.get("proven", False)

    def test_ranks_start_at_one(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        scores = ranker.rank_conjectures(kg, emb)
        if scores:
            assert scores[0].overall_rank == 1

    def test_ranks_are_sequential(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        scores = ranker.rank_conjectures(kg, emb)
        for i, s in enumerate(scores):
            assert s.overall_rank == i + 1

    def test_riemann_is_ranked(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        scores = ranker.rank_conjectures(kg, emb)
        names = [s.name for s in scores]
        assert "Riemann Hypothesis" in names

    def test_generate_roadmap_returns_steps(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        conj = _get_conjecture(concepts)
        roadmap = ranker.generate_roadmap(conj, kg)
        assert isinstance(roadmap, list)
        assert len(roadmap) >= 3

    def test_rank_conjectures_nonempty(self):
        concepts, kg, emb = _setup()
        ranker = ConjectureRanker()
        scores = ranker.rank_conjectures(kg, emb)
        assert len(scores) > 0

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from engine.fruitfulness_predictor import FruitfulnessPredictor, FruitfulnessPrediction
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


class TestPredictSingle:
    def test_returns_prediction_object(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert isinstance(pred, FruitfulnessPrediction)

    def test_concept_id_matches(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert pred.concept_id == concepts[0]["concept_id"]

    def test_overall_fruitfulness_in_range(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert 0.0 <= pred.overall_fruitfulness <= 1.0

    def test_confidence_in_range(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert 0.0 <= pred.confidence <= 1.0

    def test_explanation_nonempty(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert pred.explanation != ""

    def test_cross_disciplinary_in_range(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert 0.0 <= pred.cross_disciplinary_score <= 1.0

    def test_theorem_yield_nonnegative(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert pred.expected_theorem_yield >= 0.0

    def test_proof_difficulty_in_range(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        pred = predictor.predict(concepts[0], kg, emb)
        assert 0.0 <= pred.proof_difficulty_estimate <= 1.0


class TestRankAll:
    def test_rank_all_returns_list(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        ranked = predictor.rank_all(concepts, kg, emb)
        assert isinstance(ranked, list)

    def test_rank_all_length_matches_input(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        ranked = predictor.rank_all(concepts, kg, emb)
        assert len(ranked) == len(concepts)

    def test_rank_all_sorted_descending(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        ranked = predictor.rank_all(concepts, kg, emb)
        scores = [p.overall_fruitfulness for p in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_rank_all_top_has_high_score(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        ranked = predictor.rank_all(concepts, kg, emb)
        assert ranked[0].overall_fruitfulness > 0.5

    def test_rank_all_empty_input(self):
        _, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        result = predictor.rank_all([], kg, emb)
        assert result == []

    def test_centrality_boost_in_range(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        boost = predictor._centrality_boost("C001", kg)
        assert 0.0 <= boost <= 1.0

    def test_neighbor_importance_in_range(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        score = predictor._neighbor_importance_score("C001", kg)
        assert 0.0 <= score <= 1.0

    def test_deterministic_results(self):
        concepts, kg, emb = _setup()
        predictor = FruitfulnessPredictor()
        p1 = predictor.predict(concepts[0], kg, emb)
        p2 = predictor.predict(concepts[0], kg, emb)
        assert p1.overall_fruitfulness == p2.overall_fruitfulness

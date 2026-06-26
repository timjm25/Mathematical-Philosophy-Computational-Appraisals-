import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from engine.historical_simulator import HistoricalSimulator, HistoricalPrediction
from engine.knowledge_graph import MathKnowledgeGraph
from engine.embedding_engine import EmbeddingEngine
from engine.fruitfulness_predictor import FruitfulnessPredictor
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
    predictor = FruitfulnessPredictor()
    return kg, emb, predictor


class TestSimulate:
    def test_simulate_returns_list(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1950, kg, emb, pred)
        assert isinstance(preds, list)

    def test_simulate_predictions_are_dataclass(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1950, kg, emb, pred)
        for p in preds:
            assert isinstance(p, HistoricalPrediction)

    def test_predictions_after_cutoff_year(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1950, kg, emb, pred)
        for p in preds:
            assert p.year_introduced > 1950

    def test_predicted_importance_in_range(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1950, kg, emb, pred)
        for p in preds:
            assert 0.0 <= p.predicted_importance <= 1.0

    def test_actual_importance_in_range(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1950, kg, emb, pred)
        for p in preds:
            assert 0.0 <= p.actual_importance <= 1.0

    def test_prediction_accuracy_in_range(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1950, kg, emb, pred)
        for p in preds:
            assert 0.0 <= p.prediction_accuracy <= 1.0

    def test_sorted_by_predicted_importance(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1980, kg, emb, pred)
        scores = [p.predicted_importance for p in preds]
        assert scores == sorted(scores, reverse=True)

    def test_simulate_no_future_concepts(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(2030, kg, emb, pred)
        assert preds == []


class TestEvaluateAccuracy:
    def test_evaluate_empty_returns_zeros(self):
        sim = HistoricalSimulator()
        result = sim.evaluate_accuracy([])
        assert result["total"] == 0
        assert result["avg_accuracy"] == 0.0

    def test_evaluate_has_required_keys(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1980, kg, emb, pred)
        result = sim.evaluate_accuracy(preds)
        for key in ("total", "avg_accuracy", "correctly_recommended", "precision"):
            assert key in result

    def test_evaluate_precision_in_range(self):
        kg, emb, pred = _setup()
        sim = HistoricalSimulator()
        preds = sim.simulate(1980, kg, emb, pred)
        result = sim.evaluate_accuracy(preds)
        assert 0.0 <= result["precision"] <= 1.0

    def test_famous_predictions_returns_list(self):
        sim = HistoricalSimulator()
        famous = sim.famous_predictions()
        assert isinstance(famous, list)
        assert len(famous) > 0

    def test_famous_predictions_have_required_fields(self):
        sim = HistoricalSimulator()
        famous = sim.famous_predictions()
        for f in famous:
            assert "name" in f
            assert "would_have_predicted" in f
            assert "signals" in f
            assert "explanation" in f

    def test_cutoff_years_defined(self):
        sim = HistoricalSimulator()
        assert 1900 in sim.CUTOFF_YEARS
        assert 1950 in sim.CUTOFF_YEARS
        assert 2010 in sim.CUTOFF_YEARS

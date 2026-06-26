import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from engine.curiosity_engine import CuriosityEngine, CuriosityInsight
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
    return kg, emb


class TestFindInsights:
    def test_find_insights_returns_list(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        assert isinstance(insights, list)

    def test_find_insights_nonempty(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        assert len(insights) > 0

    def test_insights_are_dataclass(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        for ins in insights:
            assert isinstance(ins, CuriosityInsight)

    def test_potential_score_in_range(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        for ins in insights:
            assert 0.0 <= ins.potential_score <= 1.0

    def test_sorted_by_potential_descending(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        scores = [ins.potential_score for ins in insights]
        assert scores == sorted(scores, reverse=True)

    def test_insight_types_valid(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        valid_types = {"hole", "bridge", "isolated", "underexplored", "missing_theory"}
        for ins in insights:
            assert ins.insight_type in valid_types

    def test_descriptions_nonempty(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        for ins in insights:
            assert ins.description != ""

    def test_suggested_questions_nonempty(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        for ins in insights:
            assert ins.suggested_question != ""


class TestInsightTypes:
    def _has_type(self, insight_type):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        return any(ins.insight_type == insight_type for ins in insights)

    def test_has_bridge_insights(self):
        assert self._has_type("bridge")

    def test_has_hole_or_missing_theory(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        insights = ce.find_insights(kg, emb)
        types = {ins.insight_type for ins in insights}
        assert "hole" in types or "missing_theory" in types

    def test_potential_discoveries_returns_list(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        disc = ce.potential_discoveries(kg, emb)
        assert isinstance(disc, list)
        assert len(disc) > 0

    def test_potential_discoveries_have_required_fields(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        disc = ce.potential_discoveries(kg, emb)
        for d in disc:
            assert "type" in d
            assert "description" in d
            assert "potential_score" in d

    def test_empty_graph_returns_empty(self):
        kg = MathKnowledgeGraph()
        emb = EmbeddingEngine()
        ce = CuriosityEngine()
        insights = ce._find_graph_holes(kg)
        assert insights == []

    def test_find_isolated_returns_list(self):
        kg, emb = _setup()
        ce = CuriosityEngine()
        isolated = ce._find_isolated_concepts(kg)
        assert isinstance(isolated, list)

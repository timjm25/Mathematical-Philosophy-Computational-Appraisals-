import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from mdn.model import Model
from data.mock_corpus import get_concepts, get_relations


def _concept(cid="C001", name="Riemann Hypothesis", domain="Number Theory",
             ctype="conjecture", proven=False):
    return {
        "concept_id": cid, "name": name, "domain": domain,
        "concept_type": ctype, "year_introduced": 1859,
        "abstract": "All non-trivial zeros have real part 1/2.",
        "authors": ["Bernhard Riemann"], "citation_count": 15000,
        "importance_score": 1.0, "proven": proven,
        "downstream_theorems": 0, "cross_domain_influence": ["Functional Analysis"],
    }


def _seeded_model():
    m = Model()
    for c in get_concepts():
        m.add_concept(c)
    for r in get_relations():
        m.add_relation(r)
    return m


class TestConcepts:
    def test_add_and_get_concept(self):
        m = Model()
        m.add_concept(_concept())
        c = m.get_concept("C001")
        assert c is not None
        assert c["name"] == "Riemann Hypothesis"

    def test_get_nonexistent_returns_none(self):
        m = Model()
        assert m.get_concept("GHOST") is None

    def test_list_concepts_empty(self):
        m = Model()
        assert m.list_concepts() == []

    def test_list_concepts_after_add(self):
        m = Model()
        m.add_concept(_concept("C001"))
        m.add_concept(_concept("C002", "FLT"))
        assert len(m.list_concepts()) == 2

    def test_filter_by_domain(self):
        m = Model()
        m.add_concept(_concept("C001", domain="Number Theory"))
        m.add_concept(_concept("C002", "Poincaré", domain="Topology"))
        assert len(m.list_concepts(domain="Number Theory")) == 1

    def test_filter_by_type(self):
        m = Model()
        m.add_concept(_concept("C001", ctype="conjecture"))
        m.add_concept(_concept("C002", "FLT", ctype="theorem"))
        assert len(m.list_concepts(concept_type="conjecture")) == 1

    def test_proven_deserialized_as_bool(self):
        m = Model()
        m.add_concept(_concept(proven=True))
        c = m.get_concept("C001")
        assert isinstance(c["proven"], bool)
        assert c["proven"] is True

    def test_cross_domain_deserialized_as_list(self):
        m = Model()
        m.add_concept(_concept())
        c = m.get_concept("C001")
        assert isinstance(c["cross_domain_influence"], list)


class TestRelations:
    def test_add_and_list_relation(self):
        m = Model()
        m.add_relation({"source_id": "C001", "target_id": "C002", "relation_type": "depends_on"})
        rels = m.list_relations()
        assert len(rels) == 1

    def test_filter_relations_by_source(self):
        m = Model()
        m.add_relation({"source_id": "C001", "target_id": "C002", "relation_type": "depends_on"})
        m.add_relation({"source_id": "C003", "target_id": "C002", "relation_type": "uses"})
        assert len(m.list_relations(source_id="C001")) == 1

    def test_relation_fields_stored(self):
        m = Model()
        m.add_relation({"source_id": "C001", "target_id": "C002", "relation_type": "generalizes"})
        r = m.list_relations()[0]
        assert r["source_id"] == "C001"
        assert r["relation_type"] == "generalizes"


class TestRunFullAnalysis:
    def test_run_full_analysis_returns_dict(self):
        m = _seeded_model()
        result = m.run_full_analysis()
        assert isinstance(result, dict)

    def test_fruitfulness_count_positive(self):
        m = _seeded_model()
        result = m.run_full_analysis()
        assert result["fruitfulness"] > 0

    def test_conjectures_count_positive(self):
        m = _seeded_model()
        result = m.run_full_analysis()
        assert result["conjectures"] > 0

    def test_insights_count_positive(self):
        m = _seeded_model()
        result = m.run_full_analysis()
        assert result["insights"] > 0

    def test_empty_model_returns_zeros(self):
        m = Model()
        result = m.run_full_analysis()
        assert result["fruitfulness"] == 0

    def test_fruitfulness_predictions_created(self):
        m = _seeded_model()
        m.run_full_analysis()
        preds = m.list_fruitfulness_predictions()
        assert len(preds) > 0

    def test_conjecture_scores_created(self):
        m = _seeded_model()
        m.run_full_analysis()
        scores = m.list_conjecture_scores()
        assert len(scores) > 0

    def test_curiosity_insights_created(self):
        m = _seeded_model()
        m.run_full_analysis()
        insights = m.list_curiosity_insights()
        assert len(insights) > 0


class TestDashboardStats:
    def _full_model(self):
        m = _seeded_model()
        m.run_full_analysis()
        return m

    def test_has_total_concepts(self):
        assert "total_concepts" in self._full_model().dashboard_stats()

    def test_has_total_relations(self):
        assert "total_relations" in self._full_model().dashboard_stats()

    def test_has_domains_covered(self):
        assert "domains_covered" in self._full_model().dashboard_stats()

    def test_has_conjectures_ranked(self):
        assert "conjectures_ranked" in self._full_model().dashboard_stats()

    def test_total_concepts_positive(self):
        stats = self._full_model().dashboard_stats()
        assert stats["total_concepts"] > 70

    def test_domains_covered_positive(self):
        stats = self._full_model().dashboard_stats()
        assert stats["domains_covered"] > 5


class TestCopilotQuery:
    def _full_model(self):
        m = _seeded_model()
        m.run_full_analysis()
        return m

    def test_copilot_returns_dict(self):
        m = self._full_model()
        result = m.copilot_query("prime numbers and zeta functions")
        assert isinstance(result, dict)

    def test_copilot_has_required_keys(self):
        m = self._full_model()
        result = m.copilot_query("elliptic curves")
        for key in ("related_concepts", "research_gaps", "predictions", "open_problems", "explanation"):
            assert key in result

    def test_copilot_related_concepts_list(self):
        m = self._full_model()
        result = m.copilot_query("topology manifolds")
        assert isinstance(result["related_concepts"], list)

    def test_copilot_explanation_nonempty(self):
        m = self._full_model()
        result = m.copilot_query("algebra groups rings")
        assert result["explanation"] != ""

    def test_copilot_empty_model(self):
        m = Model()
        result = m.copilot_query("anything")
        assert "related_concepts" in result
        assert result["related_concepts"] == []

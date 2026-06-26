import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from engine.knowledge_graph import MathKnowledgeGraph


def _concept(cid="C001", name="Riemann Hypothesis", domain="Number Theory",
             ctype="conjecture", year=1859, importance=1.0, proven=False):
    return {
        "concept_id": cid, "name": name, "domain": domain,
        "concept_type": ctype, "year_introduced": year,
        "importance_score": importance, "proven": proven,
        "citation_count": 10000, "downstream_theorems": 0,
        "cross_domain_influence": ["Functional Analysis"],
        "abstract": f"Abstract for {name}.",
    }


class TestAddAndGet:
    def test_add_and_get_concept(self):
        kg = MathKnowledgeGraph()
        kg.add_concept(_concept())
        c = kg.get_concept("C001")
        assert c is not None
        assert c["name"] == "Riemann Hypothesis"

    def test_get_nonexistent_returns_none(self):
        kg = MathKnowledgeGraph()
        assert kg.get_concept("MISSING") is None

    def test_add_multiple_concepts(self):
        kg = MathKnowledgeGraph()
        for i in range(5):
            kg.add_concept(_concept(f"C{i:03d}", f"Concept {i}"))
        assert len(kg.graph.nodes) == 5

    def test_add_relation_between_existing(self):
        kg = MathKnowledgeGraph()
        kg.add_concept(_concept("C001"))
        kg.add_concept(_concept("C002", "FLT"))
        kg.add_relation("C001", "C002", "motivated_by")
        assert kg.graph.has_edge("C001", "C002")

    def test_add_relation_missing_node_ignored(self):
        kg = MathKnowledgeGraph()
        kg.add_concept(_concept("C001"))
        kg.add_relation("C001", "GHOST", "depends_on")
        assert not kg.graph.has_edge("C001", "GHOST")

    def test_neighbors_returns_list(self):
        kg = MathKnowledgeGraph()
        kg.add_concept(_concept("C001"))
        kg.add_concept(_concept("C002", "FLT"))
        kg.add_relation("C001", "C002", "motivated_by")
        nbrs = kg.neighbors("C001")
        assert isinstance(nbrs, list)
        assert any(n["concept_id"] == "C002" for n in nbrs)

    def test_neighbors_empty_for_isolated(self):
        kg = MathKnowledgeGraph()
        kg.add_concept(_concept("C001"))
        assert kg.neighbors("C001") == []


class TestGraphAnalysis:
    def _make_kg(self):
        kg = MathKnowledgeGraph()
        from data.mock_corpus import get_concepts, get_relations
        for c in get_concepts():
            kg.add_concept(c)
        for r in get_relations():
            kg.add_relation(r["source_id"], r["target_id"], r["relation_type"])
        return kg

    def test_centrality_scores_nonempty(self):
        kg = self._make_kg()
        scores = kg.centrality_scores()
        assert len(scores) > 0

    def test_centrality_values_in_range(self):
        kg = self._make_kg()
        scores = kg.centrality_scores()
        for v in scores.values():
            assert 0.0 <= v <= 1.0

    def test_find_bridges_nonempty(self):
        kg = self._make_kg()
        bridges = kg.find_bridges()
        assert isinstance(bridges, list)
        assert len(bridges) > 0

    def test_bridges_have_centrality_field(self):
        kg = self._make_kg()
        bridges = kg.find_bridges()
        for b in bridges:
            assert "centrality" in b

    def test_domain_clusters_nonempty(self):
        kg = self._make_kg()
        clusters = kg.domain_clusters()
        assert len(clusters) > 5

    def test_domain_clusters_contain_valid_ids(self):
        kg = self._make_kg()
        clusters = kg.domain_clusters()
        for domain, ids in clusters.items():
            for cid in ids:
                assert kg.get_concept(cid) is not None

    def test_missing_connections_returns_list(self):
        kg = self._make_kg()
        missing = kg.missing_connections()
        assert isinstance(missing, list)

    def test_concept_evolution_timeline_sorted(self):
        kg = self._make_kg()
        timeline = kg.concept_evolution_timeline()
        years = [c.get("year_introduced", 9999) for c in timeline]
        assert years == sorted(years)

    def test_stats_has_required_keys(self):
        kg = self._make_kg()
        stats = kg.stats()
        for key in ("node_count", "edge_count", "domain_count", "avg_degree"):
            assert key in stats

    def test_stats_node_count_matches(self):
        kg = self._make_kg()
        stats = kg.stats()
        assert stats["node_count"] == len(kg.graph.nodes)

    def test_shortest_path_exists(self):
        kg = self._make_kg()
        path = kg.shortest_path("C001", "C004")
        assert isinstance(path, list)

    def test_shortest_path_missing_returns_empty(self):
        kg = MathKnowledgeGraph()
        kg.add_concept(_concept("C001"))
        path = kg.shortest_path("C001", "NONE")
        assert path == []

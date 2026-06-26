import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from engine.embedding_engine import EmbeddingEngine
from data.mock_corpus import get_concepts


class TestFitAndEmbed:
    def _fitted_engine(self):
        e = EmbeddingEngine(n_components=20)
        e.fit(get_concepts())
        return e

    def test_fit_sets_fitted_flag(self):
        e = self._fitted_engine()
        assert e._fitted is True

    def test_vocab_nonempty_after_fit(self):
        e = self._fitted_engine()
        assert len(e._vocab) > 0

    def test_embeddings_populated_after_fit(self):
        e = self._fitted_engine()
        assert len(e._embeddings) > 60

    def test_embed_returns_list(self):
        e = self._fitted_engine()
        vec = e.embed("prime numbers and zeta functions")
        assert isinstance(vec, list)
        assert len(vec) > 0

    def test_embed_empty_unfitted_returns_empty(self):
        e = EmbeddingEngine()
        result = e.embed("anything")
        assert result == []

    def test_fit_empty_list(self):
        e = EmbeddingEngine()
        e.fit([])
        assert e._fitted is True

    def test_concept_in_embeddings(self):
        e = self._fitted_engine()
        assert "C001" in e._embeddings


class TestSimilarityAndNeighbors:
    def _fitted_engine(self):
        e = EmbeddingEngine(n_components=20)
        e.fit(get_concepts())
        return e

    def test_similarity_self_is_one(self):
        e = self._fitted_engine()
        sim = e.similarity("C001", "C001")
        assert abs(sim - 1.0) < 0.01

    def test_similarity_in_range(self):
        e = self._fitted_engine()
        sim = e.similarity("C001", "C002")
        assert 0.0 <= sim <= 1.0

    def test_similarity_missing_id_returns_zero(self):
        e = self._fitted_engine()
        assert e.similarity("GHOST", "C001") == 0.0

    def test_nearest_neighbors_returns_list(self):
        e = self._fitted_engine()
        nn = e.nearest_neighbors("C001", k=5)
        assert isinstance(nn, list)
        assert len(nn) == 5

    def test_nearest_neighbors_no_self(self):
        e = self._fitted_engine()
        nn = e.nearest_neighbors("C001", k=5)
        ids = [n["concept_id"] for n in nn]
        assert "C001" not in ids

    def test_nearest_neighbors_have_similarity_field(self):
        e = self._fitted_engine()
        nn = e.nearest_neighbors("C001", k=3)
        for n in nn:
            assert "similarity" in n

    def test_cluster_concepts_returns_dict(self):
        e = self._fitted_engine()
        clusters = e.cluster_concepts(n_clusters=5)
        assert isinstance(clusters, dict)
        assert len(clusters) > 0

    def test_latent_space_coordinates_populated(self):
        e = self._fitted_engine()
        coords = e.latent_space_coordinates()
        assert len(coords) > 0

    def test_latent_coords_are_2d(self):
        e = self._fitted_engine()
        coords = e.latent_space_coordinates()
        for v in list(coords.values())[:5]:
            assert len(v) == 2

    def test_find_latent_gaps_returns_list(self):
        e = self._fitted_engine()
        gaps = e.find_latent_gaps()
        assert isinstance(gaps, list)

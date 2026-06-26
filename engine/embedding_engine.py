"""TF-IDF + SVD embedding engine for mathematical concepts."""
from __future__ import annotations
import math


class EmbeddingEngine:
    def __init__(self, n_components: int = 50) -> None:
        self.n_components = n_components
        self._embeddings: dict[str, list[float]] = {}
        self._concept_index: dict[str, dict] = {}
        self._fitted = False
        self._vocab: dict[str, int] = {}
        self._idf: dict[str, float] = {}
        self._svd_components: list[list[float]] = []
        self._coords_2d: dict[str, list[float]] = {}

    def _tokenize(self, text: str) -> list[str]:
        import re
        tokens = re.findall(r"[a-z]+", text.lower())
        stopwords = {"the", "a", "an", "of", "and", "in", "to", "is", "it", "that",
                     "for", "on", "with", "as", "by", "from", "be", "are", "was",
                     "this", "or", "at", "has", "its", "into", "not", "which"}
        return [t for t in tokens if t not in stopwords and len(t) > 2]

    def _tfidf_vector(self, tokens: list[str]) -> list[float]:
        counts: dict[str, int] = {}
        for t in tokens:
            if t in self._vocab:
                counts[t] = counts.get(t, 0) + 1
        total = max(len(tokens), 1)
        vec = [0.0] * len(self._vocab)
        for t, cnt in counts.items():
            idx = self._vocab[t]
            tf = cnt / total
            idf = self._idf.get(t, 0.0)
            vec[idx] = tf * idf
        return vec

    def _dot(self, a: list[float], b: list[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def _norm(self, a: list[float]) -> float:
        return math.sqrt(sum(x * x for x in a))

    def _mat_vec(self, mat: list[list[float]], vec: list[float]) -> list[float]:
        return [self._dot(row, vec) for row in mat]

    def fit(self, concepts: list[dict]) -> None:
        if not concepts:
            self._fitted = True
            return

        texts: dict[str, list[str]] = {}
        for c in concepts:
            cid = c["concept_id"]
            self._concept_index[cid] = c
            combined = f"{c.get('name', '')} {c.get('abstract', '')} {c.get('domain', '')} {c.get('concept_type', '')}"
            texts[cid] = self._tokenize(combined)

        # Build vocabulary
        doc_freq: dict[str, int] = {}
        all_tokens: set[str] = set()
        for tokens in texts.values():
            unique = set(tokens)
            all_tokens |= unique
            for t in unique:
                doc_freq[t] = doc_freq.get(t, 0) + 1

        self._vocab = {t: i for i, t in enumerate(sorted(all_tokens))}
        n_docs = len(texts)
        self._idf = {
            t: math.log((n_docs + 1) / (df + 1)) + 1.0
            for t, df in doc_freq.items()
        }

        # Build TF-IDF matrix (docs × vocab)
        doc_ids = list(texts.keys())
        tfidf_matrix = [self._tfidf_vector(texts[did]) for did in doc_ids]

        # Power iteration SVD-like: compute top n_components principal components
        n_comp = min(self.n_components, len(self._vocab), len(doc_ids))
        try:
            import numpy as np
            X = np.array(tfidf_matrix, dtype=float)
            # SVD via numpy
            U, s, Vt = np.linalg.svd(X, full_matrices=False)
            k = min(n_comp, len(s))
            reduced = U[:, :k] * s[:k]
            self._svd_components = Vt[:k].tolist()
            for i, did in enumerate(doc_ids):
                self._embeddings[did] = reduced[i].tolist()
        except ImportError:
            # Fallback: use raw TF-IDF (truncated)
            self._svd_components = []
            for i, did in enumerate(doc_ids):
                vec = tfidf_matrix[i][:n_comp] + [0.0] * max(0, n_comp - len(tfidf_matrix[i]))
                self._embeddings[did] = vec

        # Compute 2D projections via PCA
        self._compute_2d_coords(list(self._embeddings.keys()))
        self._fitted = True

    def _compute_2d_coords(self, doc_ids: list[str]) -> None:
        if not doc_ids or not self._embeddings:
            return
        try:
            import numpy as np
            X = np.array([self._embeddings[did] for did in doc_ids], dtype=float)
            # Center
            mean = X.mean(axis=0)
            Xc = X - mean
            # Covariance
            cov = (Xc.T @ Xc) / max(1, len(doc_ids) - 1)
            vals, vecs = np.linalg.eigh(cov)
            # Top 2 eigenvectors
            idx = np.argsort(vals)[::-1][:2]
            proj = Xc @ vecs[:, idx]
            for i, did in enumerate(doc_ids):
                self._coords_2d[did] = [float(proj[i, 0]), float(proj[i, 1])]
        except (ImportError, Exception):
            for i, did in enumerate(doc_ids):
                self._coords_2d[did] = [float(i), 0.0]

    def embed(self, text: str) -> list[float]:
        if not self._fitted:
            return []
        tokens = self._tokenize(text)
        vec = self._tfidf_vector(tokens)
        if self._svd_components:
            try:
                import numpy as np
                v = np.array(vec)
                comp = np.array(self._svd_components)
                return (comp @ v).tolist()
            except ImportError:
                pass
        return vec[:self.n_components] + [0.0] * max(0, self.n_components - len(vec))

    def similarity(self, id_a: str, id_b: str) -> float:
        ea = self._embeddings.get(id_a)
        eb = self._embeddings.get(id_b)
        if not ea or not eb:
            return 0.0
        na, nb = self._norm(ea), self._norm(eb)
        if na == 0 or nb == 0:
            return 0.0
        return max(0.0, min(1.0, self._dot(ea, eb) / (na * nb)))

    def nearest_neighbors(self, concept_id: str, k: int = 5) -> list[dict]:
        if concept_id not in self._embeddings:
            return []
        sims = []
        for other_id in self._embeddings:
            if other_id != concept_id:
                sims.append({"concept_id": other_id, "similarity": self.similarity(concept_id, other_id)})
        sims.sort(key=lambda x: x["similarity"], reverse=True)
        return sims[:k]

    def cluster_concepts(self, n_clusters: int = 8) -> dict[str, int]:
        if not self._embeddings:
            return {}
        ids = list(self._embeddings.keys())
        n = min(n_clusters, len(ids))
        try:
            import numpy as np
            X = np.array([self._embeddings[i] for i in ids], dtype=float)
            # Simple k-means
            rng = np.random.default_rng(42)
            centroids = X[rng.choice(len(X), n, replace=False)]
            for _ in range(20):
                dists = np.linalg.norm(X[:, None] - centroids[None], axis=2)
                labels = np.argmin(dists, axis=1)
                for k in range(n):
                    mask = labels == k
                    if mask.any():
                        centroids[k] = X[mask].mean(axis=0)
            return {ids[i]: int(labels[i]) for i in range(len(ids))}
        except ImportError:
            return {cid: i % n for i, cid in enumerate(ids)}

    def latent_space_coordinates(self) -> dict[str, list[float]]:
        return dict(self._coords_2d)

    def find_latent_gaps(self) -> list[dict]:
        """Find regions of embedding space with low concept density."""
        coords = self._coords_2d
        if len(coords) < 4:
            return []
        ids = list(coords.keys())
        gaps = []
        # Find pairs of concepts that are far apart in embedding space
        # but whose domain suggests they should be related
        try:
            import numpy as np
            pts = np.array([coords[i] for i in ids])
            # Compute pairwise distances
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    dist = float(np.linalg.norm(pts[i] - pts[j]))
                    if dist > 1.5:  # far apart
                        ci = self._concept_index.get(ids[i], {})
                        cj = self._concept_index.get(ids[j], {})
                        gaps.append({
                            "id_a": ids[i],
                            "id_b": ids[j],
                            "name_a": ci.get("name", ids[i]),
                            "name_b": cj.get("name", ids[j]),
                            "distance": round(dist, 3),
                            "description": f"Large latent gap between '{ci.get('name', ids[i])}' and '{cj.get('name', ids[j])}'",
                        })
        except ImportError:
            pass
        gaps.sort(key=lambda x: x["distance"], reverse=True)
        return gaps[:10]

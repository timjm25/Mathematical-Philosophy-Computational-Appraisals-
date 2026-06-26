"""Predict research fruitfulness of mathematical concepts."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class FruitfulnessPrediction:
    concept_id: str
    concept_name: str
    domain: str
    expected_theorem_yield: float
    citation_impact_score: float
    new_subfield_probability: float
    cross_disciplinary_score: float
    proof_difficulty_estimate: float
    overall_fruitfulness: float
    confidence: float
    explanation: str
    comparable_historical: list[str] = field(default_factory=list)


class FruitfulnessPredictor:
    # Maximum observed citation counts for normalization
    _MAX_CITATIONS = 20000.0
    _MAX_DOWNSTREAM = 500.0

    def _normalize(self, value: float, max_val: float) -> float:
        if max_val <= 0:
            return 0.0
        return min(1.0, max(0.0, value / max_val))

    def _centrality_boost(self, concept_id: str, graph) -> float:
        scores = graph.centrality_scores()
        score = scores.get(concept_id, 0.0)
        if not scores:
            return 0.0
        max_score = max(scores.values()) if scores else 1.0
        return self._normalize(score, max_score)

    def _neighbor_importance_score(self, concept_id: str, graph) -> float:
        neighbors = graph.neighbors(concept_id, depth=1)
        if not neighbors:
            return 0.0
        importance_values = [n.get("importance_score", 0.0) for n in neighbors]
        return sum(importance_values) / len(importance_values)

    def predict(self, concept: dict, graph, embeddings) -> FruitfulnessPrediction:
        cid = concept["concept_id"]
        citation_count = concept.get("citation_count", 0)
        importance = concept.get("importance_score", 0.0)
        cross_domains = concept.get("cross_domain_influence", [])
        proven = concept.get("proven", True)
        downstream = concept.get("downstream_theorems", 0)

        # Component scores
        citation_score = self._normalize(citation_count, self._MAX_CITATIONS)
        centrality = self._centrality_boost(cid, graph)
        neighbor_imp = self._neighbor_importance_score(cid, graph)
        cross_score = min(1.0, len(cross_domains) / 4.0)
        downstream_score = self._normalize(downstream, self._MAX_DOWNSTREAM)

        # Unproven conjectures get an uncertainty bonus (high potential)
        conjecture_bonus = 0.15 if not proven else 0.0

        # Composite fruitfulness (weighted)
        overall = (
            0.25 * importance
            + 0.20 * citation_score
            + 0.20 * centrality
            + 0.15 * neighbor_imp
            + 0.10 * cross_score
            + 0.10 * downstream_score
        ) + conjecture_bonus
        overall = min(1.0, max(0.0, overall))

        # Derived predictions
        expected_yield = overall * 10.0  # scale to 0-10
        new_subfield_prob = min(1.0, cross_score * 0.7 + centrality * 0.3)
        proof_difficulty = 1.0 - (downstream_score * 0.5 + citation_score * 0.3 + (0.2 if proven else 0.0))
        proof_difficulty = min(1.0, max(0.0, proof_difficulty))
        confidence = 0.5 + 0.3 * citation_score + 0.2 * importance

        # Explanation
        parts = []
        if centrality > 0.5:
            parts.append(f"high graph centrality ({centrality:.2f}) — concepts depend on it")
        if cross_score > 0.5:
            parts.append(f"cross-domain influence on {len(cross_domains)} fields")
        if not proven:
            parts.append("open conjecture carries exploratory potential")
        if neighbor_imp > 0.7:
            parts.append("strongly connected to high-importance neighbors")
        if citation_score > 0.5:
            parts.append(f"citation volume ({citation_count:,}) signals broad community interest")
        explanation = (
            "Fruitfulness driven by: " + "; ".join(parts)
            if parts else f"Moderate fruitfulness for {concept.get('domain', 'unknown')} domain."
        )

        # Historical comparables (nearest neighbors in embedding space)
        nn = embeddings.nearest_neighbors(cid, k=3) if embeddings._fitted else []
        comparables = []
        for nb in nn:
            c2 = embeddings._concept_index.get(nb["concept_id"], {})
            if c2.get("name"):
                comparables.append(c2["name"])

        return FruitfulnessPrediction(
            concept_id=cid,
            concept_name=concept.get("name", cid),
            domain=concept.get("domain", "Unknown"),
            expected_theorem_yield=round(expected_yield, 2),
            citation_impact_score=round(citation_score, 3),
            new_subfield_probability=round(new_subfield_prob, 3),
            cross_disciplinary_score=round(cross_score, 3),
            proof_difficulty_estimate=round(proof_difficulty, 3),
            overall_fruitfulness=round(overall, 3),
            confidence=round(confidence, 3),
            explanation=explanation,
            comparable_historical=comparables,
        )

    def rank_all(self, concepts: list[dict], graph, embeddings) -> list[FruitfulnessPrediction]:
        predictions = [self.predict(c, graph, embeddings) for c in concepts]
        return sorted(predictions, key=lambda p: p.overall_fruitfulness, reverse=True)

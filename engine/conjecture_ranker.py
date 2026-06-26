"""Score and rank mathematical conjectures."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ConjectureScore:
    concept_id: str
    name: str
    domain: str
    novelty_score: float
    importance_score: float
    connectivity_score: float
    generalization_score: float
    depth_estimate: float
    expected_downstream: int
    predicted_proof_complexity: str
    historical_analogues: list[str] = field(default_factory=list)
    related_conjectures: list[str] = field(default_factory=list)
    research_roadmap: list[str] = field(default_factory=list)
    overall_rank: int = 0


_COMPLEXITY_THRESHOLDS = [
    (0.25, "elementary"),
    (0.50, "moderate"),
    (0.75, "deep"),
    (1.01, "exceptional"),
]


class ConjectureRanker:
    def score_conjecture(self, concept: dict, graph, embeddings) -> ConjectureScore:
        cid = concept["concept_id"]
        importance = concept.get("importance_score", 0.0)
        citations = concept.get("citation_count", 0)
        cross_domains = concept.get("cross_domain_influence", [])
        year = concept.get("year_introduced", 2000)

        # Novelty: older open problems are more novel/deep
        age = 2024 - year
        novelty = min(1.0, age / 200.0)

        # Connectivity via graph centrality
        centrality_scores = graph.centrality_scores()
        raw_centrality = centrality_scores.get(cid, 0.0)
        max_centrality = max(centrality_scores.values()) if centrality_scores else 1.0
        connectivity = raw_centrality / max(max_centrality, 1e-9)

        # Generalization: cross-domain influence
        generalization = min(1.0, len(cross_domains) / 5.0)

        # Depth estimate based on citation density and connectivity
        depth = (importance * 0.4 + connectivity * 0.3 + novelty * 0.3)

        # Expected downstream theorems (heuristic based on importance)
        expected_downstream = int(importance * 200 + connectivity * 100)

        # Proof complexity
        complexity_score = depth
        predicted_complexity = "exceptional"
        for threshold, label in _COMPLEXITY_THRESHOLDS:
            if complexity_score < threshold:
                predicted_complexity = label
                break

        # Historical analogues from nearest neighbors
        analogues = []
        if embeddings._fitted:
            nn = embeddings.nearest_neighbors(cid, k=4)
            for nb in nn:
                c2 = embeddings._concept_index.get(nb["concept_id"], {})
                if c2.get("proven", False) and c2.get("name"):
                    analogues.append(c2["name"])

        # Related conjectures
        related = []
        neighbors = graph.neighbors(cid, depth=2)
        for nb in neighbors:
            if nb.get("concept_type") == "conjecture" and nb.get("concept_id") != cid:
                related.append(nb["name"])

        roadmap = self.generate_roadmap(concept, graph)

        return ConjectureScore(
            concept_id=cid,
            name=concept.get("name", cid),
            domain=concept.get("domain", "Unknown"),
            novelty_score=round(novelty, 3),
            importance_score=round(importance, 3),
            connectivity_score=round(connectivity, 3),
            generalization_score=round(generalization, 3),
            depth_estimate=round(depth, 3),
            expected_downstream=expected_downstream,
            predicted_proof_complexity=predicted_complexity,
            historical_analogues=analogues[:3],
            related_conjectures=related[:4],
            research_roadmap=roadmap,
        )

    def generate_roadmap(self, concept: dict, graph) -> list[str]:
        domain = concept.get("domain", "Mathematics")
        name = concept.get("name", "this conjecture")
        year = concept.get("year_introduced", 1900)
        cross_domains = concept.get("cross_domain_influence", [])

        steps = [
            f"Survey the literature on {name} since {year} to catalog known partial results.",
            f"Identify the boundary cases and special instances that are already resolved.",
            f"Study proof techniques from historically analogous theorems in {domain}.",
        ]
        if cross_domains:
            steps.append(
                f"Explore connections to {', '.join(cross_domains[:2])} for cross-domain insights."
            )
        neighbors = graph.neighbors(concept["concept_id"], depth=1)
        proven_neighbors = [nb["name"] for nb in neighbors if nb.get("proven", False)][:2]
        if proven_neighbors:
            steps.append(
                f"Leverage existing theorems ({', '.join(proven_neighbors)}) as building blocks."
            )
        steps += [
            "Formulate and test specific lemmas that would imply the main result.",
            "Search for computational or algorithmic evidence using finite cases.",
            "Investigate whether a weaker version can be proved to build intuition.",
        ]
        return steps

    def rank_conjectures(self, graph, embeddings) -> list[ConjectureScore]:
        conjectures = [
            dict(graph.graph.nodes[n])
            for n in graph.graph.nodes
            if graph.graph.nodes[n].get("concept_type") == "conjecture"
            and not graph.graph.nodes[n].get("proven", False)
        ]
        scores = [self.score_conjecture(c, graph, embeddings) for c in conjectures]
        # Rank by composite score
        composite = lambda s: (s.importance_score * 0.35 + s.connectivity_score * 0.25
                               + s.generalization_score * 0.20 + s.novelty_score * 0.20)
        scores.sort(key=composite, reverse=True)
        for i, s in enumerate(scores):
            s.overall_rank = i + 1
        return scores

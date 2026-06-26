"""Find unexplored regions and hidden patterns in mathematical space."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class CuriosityInsight:
    insight_type: str  # "hole" | "bridge" | "isolated" | "underexplored" | "missing_theory"
    concept_ids: list[str]
    description: str
    potential_score: float
    suggested_question: str
    recommended_action: str


class CuriosityEngine:
    def find_insights(self, graph, embeddings) -> list[CuriosityInsight]:
        insights: list[CuriosityInsight] = []
        insights.extend(self._find_graph_holes(graph))
        insights.extend(self._find_bridges(graph))
        insights.extend(self._find_isolated_concepts(graph))
        insights.extend(self._find_embedding_gaps(embeddings))
        insights.extend(self._find_missing_theories(graph))
        insights.sort(key=lambda x: x.potential_score, reverse=True)
        return insights

    def _find_graph_holes(self, graph) -> list[CuriosityInsight]:
        """Find domain pairs with few or no cross-domain connections."""
        if not graph.graph.nodes:
            return []
        clusters = graph.domain_clusters()
        domains = list(clusters.keys())
        insights = []
        for i, d1 in enumerate(domains):
            for d2 in domains[i + 1:]:
                nodes1 = clusters[d1]
                nodes2 = clusters[d2]
                cross_edges = sum(
                    1 for a in nodes1 for b in nodes2
                    if graph.graph.has_edge(a, b) or graph.graph.has_edge(b, a)
                )
                total_possible = len(nodes1) * len(nodes2)
                if total_possible > 0:
                    density = cross_edges / total_possible
                    if density < 0.05 and len(nodes1) >= 2 and len(nodes2) >= 2:
                        potential = min(0.95, 0.4 + (1.0 - density) * 0.5)
                        insights.append(CuriosityInsight(
                            insight_type="hole",
                            concept_ids=nodes1[:2] + nodes2[:2],
                            description=f"Sparse connections ({cross_edges}) between {d1} and {d2} despite both being active domains.",
                            potential_score=round(potential, 3),
                            suggested_question=f"What would a unifying theory between {d1} and {d2} look like?",
                            recommended_action=f"Investigate whether techniques from {d1} can solve open problems in {d2}.",
                        ))
        insights.sort(key=lambda x: x.potential_score, reverse=True)
        return insights[:6]

    def _find_bridges(self, graph) -> list[CuriosityInsight]:
        """Highlight concepts that bridge multiple domains."""
        if not graph.graph.nodes:
            return []
        bridges = graph.find_bridges()
        insights = []
        for b in bridges[:4]:
            cross_domains = b.get("cross_domain_influence", [])
            potential = min(0.95, 0.5 + b.get("centrality", 0) * 2)
            insights.append(CuriosityInsight(
                insight_type="bridge",
                concept_ids=[b["concept_id"]],
                description=f"'{b.get('name')}' is a high-centrality bridge concept connecting {b.get('domain')} to {len(cross_domains)} other domains.",
                potential_score=round(potential, 3),
                suggested_question=f"Can '{b.get('name')}' serve as a template for analogous results in adjacent fields?",
                recommended_action=f"Systematically apply methods from '{b.get('name')}' to unexplored neighboring domains.",
            ))
        return insights

    def _find_isolated_concepts(self, graph) -> list[CuriosityInsight]:
        """Find concepts with very few connections despite high importance."""
        insights = []
        for node_id in graph.graph.nodes:
            data = graph.get_concept(node_id)
            if not data:
                continue
            degree = graph.graph.degree(node_id)
            importance = data.get("importance_score", 0.0)
            if degree <= 1 and importance > 0.75:
                potential = min(0.9, importance * 0.8)
                insights.append(CuriosityInsight(
                    insight_type="isolated",
                    concept_ids=[node_id],
                    description=f"'{data.get('name')}' has importance {importance:.2f} but only {degree} connections in the knowledge graph.",
                    potential_score=round(potential, 3),
                    suggested_question=f"Why is '{data.get('name')}' so isolated? Are there hidden connections waiting to be discovered?",
                    recommended_action=f"Conduct a systematic literature search to uncover all known relations of '{data.get('name')}'.",
                ))
        return sorted(insights, key=lambda x: x.potential_score, reverse=True)[:4]

    def _find_embedding_gaps(self, embeddings) -> list[CuriosityInsight]:
        """Find underexplored regions in the latent mathematical space."""
        if not embeddings._fitted:
            return []
        gaps = embeddings.find_latent_gaps()
        insights = []
        for gap in gaps[:3]:
            potential = min(0.88, 0.4 + gap.get("distance", 0) * 0.1)
            insights.append(CuriosityInsight(
                insight_type="underexplored",
                concept_ids=[gap.get("id_a", ""), gap.get("id_b", "")],
                description=f"Large semantic gap (distance {gap.get('distance')}) between '{gap.get('name_a')}' and '{gap.get('name_b')}' in latent space.",
                potential_score=round(potential, 3),
                suggested_question=f"What mathematical structure would interpolate between '{gap.get('name_a')}' and '{gap.get('name_b')}'?",
                recommended_action="Explore the mathematical space between these concepts for novel structures.",
            ))
        return insights

    def _find_missing_theories(self, graph) -> list[CuriosityInsight]:
        """Find pairs of same-domain concepts with no path between them."""
        if not graph.graph.nodes:
            return []
        missing = graph.missing_connections()
        insights = []
        for m in missing[:4]:
            insights.append(CuriosityInsight(
                insight_type="missing_theory",
                concept_ids=[m["source_id"], m["target_id"]],
                description=f"'{m['source_name']}' and '{m['target_name']}' share the {m['domain']} domain but have no known mathematical connection.",
                potential_score=round(0.65, 3),
                suggested_question=f"These structures appear mathematically adjacent but have never been formally connected. Is there a missing theorem linking '{m['source_name']}' to '{m['target_name']}'?",
                recommended_action=f"Develop a formal framework connecting {m['source_name']} and {m['target_name']} within {m['domain']}.",
            ))
        return insights

    def potential_discoveries(self, graph, embeddings) -> list[dict]:
        insights = self.find_insights(graph, embeddings)
        return [
            {
                "type": ins.insight_type,
                "description": ins.description,
                "potential_score": ins.potential_score,
                "action": ins.recommended_action,
                "concept_ids": ins.concept_ids,
            }
            for ins in insights[:10]
        ]

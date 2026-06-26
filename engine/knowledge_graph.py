"""Mathematical knowledge graph backed by NetworkX."""
from __future__ import annotations
import networkx as nx


class MathKnowledgeGraph:
    def __init__(self) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()

    def add_concept(self, concept: dict) -> None:
        self.graph.add_node(concept["concept_id"], **concept)

    def add_relation(self, source_id: str, target_id: str, relation_type: str) -> None:
        if source_id in self.graph and target_id in self.graph:
            self.graph.add_edge(source_id, target_id, relation_type=relation_type)

    def get_concept(self, concept_id: str) -> dict | None:
        if concept_id not in self.graph:
            return None
        return dict(self.graph.nodes[concept_id])

    def neighbors(self, concept_id: str, depth: int = 1) -> list[dict]:
        if concept_id not in self.graph:
            return []
        if depth == 1:
            nbrs = set(self.graph.successors(concept_id)) | set(self.graph.predecessors(concept_id))
        else:
            nbrs = set()
            frontier = {concept_id}
            for _ in range(depth):
                next_frontier: set[str] = set()
                for n in frontier:
                    next_frontier |= set(self.graph.successors(n)) | set(self.graph.predecessors(n))
                nbrs |= next_frontier
                frontier = next_frontier - nbrs - {concept_id}
        result = []
        for n in nbrs:
            if n != concept_id:
                data = self.get_concept(n)
                if data:
                    result.append(data)
        return result

    def shortest_path(self, source: str, target: str) -> list[str]:
        try:
            return nx.shortest_path(self.graph.to_undirected(), source, target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def centrality_scores(self) -> dict[str, float]:
        if len(self.graph) == 0:
            return {}
        try:
            return nx.betweenness_centrality(self.graph)
        except Exception:
            return {n: 0.0 for n in self.graph.nodes}

    def find_bridges(self) -> list[dict]:
        """Return concepts that connect otherwise disconnected components (high betweenness)."""
        if len(self.graph) < 3:
            return []
        scores = self.centrality_scores()
        if not scores:
            return []
        threshold = sorted(scores.values())[-max(1, len(scores) // 5)]
        bridges = []
        for node_id, score in scores.items():
            if score >= threshold:
                data = self.get_concept(node_id)
                if data:
                    bridges.append({**data, "centrality": round(score, 4)})
        return sorted(bridges, key=lambda x: x["centrality"], reverse=True)

    def domain_clusters(self) -> dict[str, list[str]]:
        clusters: dict[str, list[str]] = {}
        for node_id, data in self.graph.nodes(data=True):
            domain = data.get("domain", "Unknown")
            clusters.setdefault(domain, []).append(node_id)
        return clusters

    def missing_connections(self) -> list[dict]:
        """Find pairs of similar-domain concepts with no graph path between them."""
        clusters = self.domain_clusters()
        missing = []
        for domain, node_ids in clusters.items():
            if len(node_ids) < 2:
                continue
            for i, a in enumerate(node_ids):
                for b in node_ids[i + 1:]:
                    path = self.shortest_path(a, b)
                    if not path:
                        ca = self.get_concept(a)
                        cb = self.get_concept(b)
                        if ca and cb:
                            missing.append({
                                "source_id": a,
                                "target_id": b,
                                "source_name": ca.get("name", a),
                                "target_name": cb.get("name", b),
                                "domain": domain,
                                "suggestion": f"No known relationship between '{ca.get('name')}' and '{cb.get('name')}' despite sharing the {domain} domain.",
                            })
        return missing[:20]

    def concept_evolution_timeline(self) -> list[dict]:
        concepts = [dict(self.graph.nodes[n]) for n in self.graph.nodes]
        return sorted(concepts, key=lambda c: c.get("year_introduced", 9999))

    def stats(self) -> dict:
        n = len(self.graph.nodes)
        e = len(self.graph.edges)
        clusters = self.domain_clusters()
        return {
            "node_count": n,
            "edge_count": e,
            "domain_count": len(clusters),
            "avg_degree": round(e / n, 2) if n else 0.0,
            "domains": list(clusters.keys()),
        }

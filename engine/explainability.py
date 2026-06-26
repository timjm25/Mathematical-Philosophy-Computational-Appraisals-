"""Explainability layer — every recommendation must include a human-readable explanation."""
from __future__ import annotations


class ExplainabilityLayer:
    def explain_fruitfulness(self, prediction, graph) -> list[str]:
        explanations = []
        if prediction.overall_fruitfulness > 0.8:
            explanations.append(
                f"Overall fruitfulness score of {prediction.overall_fruitfulness:.2f} places "
                f"'{prediction.concept_name}' in the top tier of research investments."
            )
        if prediction.citation_impact_score > 0.5:
            explanations.append(
                f"High citation impact ({prediction.citation_impact_score:.2f}) reflects broad "
                f"community interest and cross-referencing."
            )
        if prediction.cross_disciplinary_score > 0.5:
            explanations.append(
                f"Cross-disciplinary score {prediction.cross_disciplinary_score:.2f} indicates "
                f"influence beyond {prediction.domain} into multiple fields."
            )
        if prediction.new_subfield_probability > 0.6:
            explanations.append(
                f"There is a {prediction.new_subfield_probability:.0%} probability this concept "
                f"will seed a new mathematical subfield."
            )
        if prediction.comparable_historical:
            explanations.append(
                f"Historically similar to: {', '.join(prediction.comparable_historical)}."
            )
        if not explanations:
            explanations.append(prediction.explanation)
        return explanations

    def explain_conjecture_score(self, score, graph) -> list[str]:
        explanations = []
        explanations.append(
            f"Ranked #{score.overall_rank} among open conjectures."
        )
        if score.novelty_score > 0.5:
            explanations.append(
                f"Novelty score {score.novelty_score:.2f}: this conjecture has remained open for "
                f"many decades, suggesting deep difficulty and correspondingly high reward."
            )
        if score.connectivity_score > 0.5:
            explanations.append(
                f"High connectivity ({score.connectivity_score:.2f}): proving this would "
                f"cascade improvements through connected theorems."
            )
        if score.generalization_score > 0.5:
            explanations.append(
                f"Generalization score {score.generalization_score:.2f}: a proof would "
                f"simultaneously resolve many related questions."
            )
        if score.historical_analogues:
            explanations.append(
                f"Historical analogues suggest successful proof strategies: "
                f"{', '.join(score.historical_analogues[:2])}."
            )
        if score.predicted_proof_complexity == "exceptional":
            explanations.append(
                "Predicted proof complexity is exceptional — likely requires fundamentally "
                "new mathematical tools."
            )
        elif score.predicted_proof_complexity == "deep":
            explanations.append(
                "Proof complexity is deep — expect synthesis of multiple advanced techniques."
            )
        return explanations

    def explain_curiosity_insight(self, insight) -> list[str]:
        type_explanations = {
            "hole": "A gap in cross-domain connections represents an untapped opportunity "
                    "for mathematical synthesis.",
            "bridge": "Bridge concepts with high centrality often generalize into "
                      "new theories when studied abstractly.",
            "isolated": "Highly important but isolated concepts may have hidden "
                        "connections awaiting discovery.",
            "underexplored": "Large semantic gaps in the mathematical landscape signal "
                             "entirely new theoretical territory.",
            "missing_theory": "Two mathematically adjacent concepts with no formal "
                              "connection is a strong indicator of a missing theorem.",
        }
        explanations = [
            type_explanations.get(insight.insight_type, "Potentially significant mathematical gap."),
            f"Potential score: {insight.potential_score:.2f}/1.00",
            f"Suggested investigation: {insight.suggested_question}",
        ]
        return explanations

    def historical_context(self, concept: dict, graph) -> str:
        year = concept.get("year_introduced", "unknown")
        name = concept.get("name", "this concept")
        domain = concept.get("domain", "mathematics")
        predecessors = graph.neighbors(concept["concept_id"], depth=1)
        older = [p for p in predecessors if p.get("year_introduced", 9999) < (year if isinstance(year, int) else 9999)]
        if older:
            pred_names = ", ".join(p["name"] for p in older[:2])
            return (
                f"'{name}' was introduced in {year} in {domain}, building on {pred_names}. "
                f"It has influenced {concept.get('downstream_theorems', 0)} downstream results."
            )
        return (
            f"'{name}' was introduced in {year} in {domain} with {concept.get('citation_count', 0):,} citations."
        )

    def analogy_explanation(self, concept_a: dict, concept_b: dict, similarity: float) -> str:
        return (
            f"'{concept_a.get('name')}' ({concept_a.get('domain')}) and "
            f"'{concept_b.get('name')}' ({concept_b.get('domain')}) share a semantic similarity "
            f"of {similarity:.2f}. "
            f"Historically similar concept pairs have produced {int(similarity * 15)} "
            f"cross-domain theorems on average."
        )

"""Flask application factory for Mathematical Discovery Navigator."""
from __future__ import annotations
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, render_template, request, redirect, url_for

from mdn.model import Model


def create_app(db_path: str = ":memory:") -> Flask:
    app = Flask(__name__, template_folder="templates")
    app.config["DB_PATH"] = db_path
    app._seeded = False

    def get_model() -> Model:
        if not hasattr(app, "_model"):
            app._model = Model(db_path)
        return app._model

    @app.before_request
    def auto_seed():
        if not app._seeded:
            m = get_model()
            if not m.list_concepts():
                from mdn.seed import seed
                seed(m)
            app._seeded = True

    # ------------------------------------------------------------------
    # Browser routes
    # ------------------------------------------------------------------

    @app.route("/")
    def dashboard():
        m = get_model()
        stats = m.dashboard_stats()
        predictions = m.list_fruitfulness_predictions()
        insights = m.list_curiosity_insights()
        scores = m.list_conjecture_scores()
        # Chart data: top 8 fruitfulness
        chart_labels = [p["concept_id"] for p in predictions[:8]]
        chart_data = [round(p["overall_fruitfulness"] * 100, 1) for p in predictions[:8]]
        return render_template(
            "dashboard.html",
            stats=stats,
            predictions=predictions[:8],
            insights=insights[:6],
            scores=scores[:5],
            chart_labels=chart_labels,
            chart_data=chart_data,
        )

    @app.route("/graph")
    def graph():
        m = get_model()
        domain_filter = request.args.get("domain", "")
        concepts = m.list_concepts(domain=domain_filter if domain_filter else None)
        all_domains = list({c["domain"] for c in m.list_concepts()})
        all_domains.sort()
        predictions = m.list_fruitfulness_predictions()
        pred_map = {p["concept_id"]: p for p in predictions}
        # Attach fruitfulness to concepts
        for c in concepts:
            c["fruitfulness"] = pred_map.get(c["concept_id"], {}).get("overall_fruitfulness", 0.0)

        from engine.knowledge_graph import MathKnowledgeGraph
        all_concepts = m.list_concepts()
        kg = MathKnowledgeGraph()
        for c in all_concepts:
            kg.add_concept(c)
        for r in m.list_relations():
            kg.add_relation(r["source_id"], r["target_id"], r["relation_type"])

        centrality = kg.centrality_scores()
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        top_central_data = [
            {"concept_id": cid, "name": kg.get_concept(cid).get("name", cid) if kg.get_concept(cid) else cid, "score": round(sc, 4)}
            for cid, sc in top_central
        ]
        bridges = kg.find_bridges()[:5]
        clusters = kg.domain_clusters()

        return render_template(
            "graph.html",
            concepts=concepts,
            all_domains=all_domains,
            selected_domain=domain_filter,
            top_central=top_central_data,
            bridges=bridges,
            clusters=clusters,
            graph_stats=kg.stats(),
        )

    @app.route("/conjecture")
    def conjecture():
        m = get_model()
        domain_filter = request.args.get("domain", "")
        scores = m.list_conjecture_scores()
        if domain_filter:
            scores = [s for s in scores if s["domain"] == domain_filter]
        all_domains = list({c["domain"] for c in m.list_concepts()})
        all_domains.sort()
        return render_template(
            "conjecture.html",
            scores=scores,
            all_domains=all_domains,
            selected_domain=domain_filter,
        )

    @app.route("/explore")
    def explore():
        m = get_model()
        insights = m.list_curiosity_insights()
        type_filter = request.args.get("type", "")
        if type_filter:
            insights = [i for i in insights if i["insight_type"] == type_filter]

        from engine.knowledge_graph import MathKnowledgeGraph
        from engine.embedding_engine import EmbeddingEngine
        all_concepts = m.list_concepts()
        embeddings = EmbeddingEngine(n_components=min(30, len(all_concepts)))
        embeddings.fit(all_concepts)
        coords = embeddings.latent_space_coordinates()
        kg = MathKnowledgeGraph()
        for c in all_concepts:
            kg.add_concept(c)

        # Nearest neighbors for a sample concept
        sample_id = request.args.get("focus", "C001")
        nn_data = []
        if embeddings._fitted:
            nn = embeddings.nearest_neighbors(sample_id, k=5)
            for nb in nn:
                c = kg.get_concept(nb["concept_id"])
                if c:
                    nn_data.append({**c, "similarity": nb["similarity"]})

        coord_list = [
            {"concept_id": cid, "x": round(xy[0], 3), "y": round(xy[1], 3),
             "name": (kg.get_concept(cid) or {}).get("name", cid)}
            for cid, xy in list(coords.items())[:30]
        ]

        all_types = ["hole", "bridge", "isolated", "underexplored", "missing_theory"]
        return render_template(
            "explore.html",
            insights=insights,
            coords=coord_list,
            nn_data=nn_data,
            focus_id=sample_id,
            all_types=all_types,
            selected_type=type_filter,
        )

    @app.route("/history")
    def history():
        from engine.historical_simulator import HistoricalSimulator
        m = get_model()
        sim = HistoricalSimulator()
        famous = sim.famous_predictions()

        cutoff = int(request.args.get("year", 1995))
        if cutoff not in HistoricalSimulator.CUTOFF_YEARS:
            cutoff = 1995

        from engine.knowledge_graph import MathKnowledgeGraph
        from engine.embedding_engine import EmbeddingEngine
        from engine.fruitfulness_predictor import FruitfulnessPredictor
        all_concepts = m.list_concepts()
        kg = MathKnowledgeGraph()
        for c in all_concepts:
            kg.add_concept(c)
        for r in m.list_relations():
            kg.add_relation(r["source_id"], r["target_id"], r["relation_type"])
        embeddings = EmbeddingEngine(n_components=min(30, len(all_concepts)))
        embeddings.fit(all_concepts)
        predictor = FruitfulnessPredictor()

        predictions = sim.simulate(cutoff, kg, embeddings, predictor)
        accuracy = sim.evaluate_accuracy(predictions)

        return render_template(
            "history.html",
            famous=famous,
            predictions=predictions,
            accuracy=accuracy,
            cutoff=cutoff,
            cutoff_years=HistoricalSimulator.CUTOFF_YEARS,
        )

    @app.route("/copilot")
    def copilot():
        m = get_model()
        query = request.args.get("q", "")
        result = None
        if query:
            result = m.copilot_query(query)
        return render_template("copilot.html", query=query, result=result)

    @app.route("/run_analysis", methods=["POST"])
    def run_analysis():
        m = get_model()
        m.run_full_analysis()
        return redirect(url_for("dashboard"))

    @app.route("/healthz")
    def healthz():
        return jsonify({"status": "ok"})

    # ------------------------------------------------------------------
    # REST API
    # ------------------------------------------------------------------

    @app.route("/api/v1/concepts")
    def api_concepts():
        m = get_model()
        domain = request.args.get("domain")
        ctype = request.args.get("type")
        return jsonify(m.list_concepts(domain=domain, concept_type=ctype))

    @app.route("/api/v1/concept/<concept_id>")
    def api_concept(concept_id: str):
        m = get_model()
        c = m.get_concept(concept_id)
        if not c:
            return jsonify({"error": "not found"}), 404
        return jsonify(c)

    @app.route("/api/v1/relations")
    def api_relations():
        m = get_model()
        source = request.args.get("source_id")
        return jsonify(m.list_relations(source_id=source))

    @app.route("/api/v1/fruitfulness")
    def api_fruitfulness():
        m = get_model()
        domain = request.args.get("domain")
        return jsonify(m.list_fruitfulness_predictions(domain=domain))

    @app.route("/api/v1/conjectures")
    def api_conjectures():
        m = get_model()
        return jsonify(m.list_conjecture_scores())

    @app.route("/api/v1/insights")
    def api_insights():
        m = get_model()
        return jsonify(m.list_curiosity_insights())

    @app.route("/api/v1/stats")
    def api_stats():
        m = get_model()
        return jsonify(m.dashboard_stats())

    @app.route("/api/v1/history/<int:year>")
    def api_history(year: int):
        from engine.historical_simulator import HistoricalSimulator
        from engine.knowledge_graph import MathKnowledgeGraph
        from engine.embedding_engine import EmbeddingEngine
        from engine.fruitfulness_predictor import FruitfulnessPredictor
        m = get_model()
        sim = HistoricalSimulator()
        all_concepts = m.list_concepts()
        kg = MathKnowledgeGraph()
        for c in all_concepts:
            kg.add_concept(c)
        for r in m.list_relations():
            kg.add_relation(r["source_id"], r["target_id"], r["relation_type"])
        embeddings = EmbeddingEngine(n_components=min(30, len(all_concepts)))
        embeddings.fit(all_concepts)
        predictor = FruitfulnessPredictor()
        predictions = sim.simulate(year, kg, embeddings, predictor)
        accuracy = sim.evaluate_accuracy(predictions)
        from dataclasses import asdict
        return jsonify({
            "cutoff_year": year,
            "accuracy": accuracy,
            "predictions": [asdict(p) for p in predictions],
        })

    @app.route("/api/v1/copilot", methods=["POST"])
    def api_copilot():
        m = get_model()
        data = request.get_json(force=True, silent=True) or {}
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "query required"}), 400
        result = m.copilot_query(query)
        return jsonify(result)

    @app.route("/api/v1/run_analysis", methods=["POST"])
    def api_run_analysis():
        m = get_model()
        result = m.run_full_analysis()
        return jsonify(result)

    return app

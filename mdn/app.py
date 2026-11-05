"""Flask application factory for Mathematical Discovery Navigator."""
from __future__ import annotations
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path

from flask import (Flask, Response, abort, jsonify, render_template, request,
                   redirect, send_from_directory, url_for)

from mdn.model import Model

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "data" / "templates"
TEMPLATE_FILES = ("concepts_template.csv", "relations_template.csv")
# Analysis pages need at least one concept; with an empty database they send
# the user to the import page instead.
_NEEDS_DATA = {"dashboard", "graph", "conjecture", "explore", "history", "copilot"}


def _env_flag(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() not in ("0", "false", "no", "off", "")


def create_app(db_path: str = ":memory:", seed_demo: bool | None = None) -> Flask:
    """
    seed_demo: load the built-in demo corpus when the database is empty.
    Defaults to $MDN_SEED_DEMO (on unless set to 0/false). With it off an
    empty database opens on the import page.
    """
    app = Flask(__name__, template_folder="templates")
    app.config["DB_PATH"] = db_path
    app.config["SEED_DEMO"] = _env_flag("MDN_SEED_DEMO", True) if seed_demo is None else seed_demo
    app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024     # upload cap
    app._seeded = False

    def get_model() -> Model:
        if not hasattr(app, "_model"):
            app._model = Model(db_path)
        return app._model

    @app.before_request
    def auto_seed():
        if not app._seeded:
            m = get_model()
            if app.config["SEED_DEMO"] and not m.list_concepts():
                from mdn.seed import seed
                seed(m)
            app._seeded = True
        if request.endpoint in _NEEDS_DATA and not get_model().list_concepts():
            return redirect(url_for("import_page", empty=1))

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
        default_focus = "C001" if kg.get_concept("C001") else (all_concepts[0]["concept_id"] if all_concepts else "")
        sample_id = request.args.get("focus") or default_focus
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
    # Bring your own data
    # ------------------------------------------------------------------

    def _import_uploads(form, files) -> tuple[dict, int]:
        """Shared by the import page and the REST endpoint."""
        from data.importer import (ImportFileError, ImportResult, parse_bundle,
                                   read_tables, tables_to_rows)
        m = get_model()
        replace = form.get("replace") in ("1", "true", "on", "yes")
        skip_invalid = form.get("skip_invalid") in ("1", "true", "on", "yes")
        cfile, rfile = files.get("concepts_file"), files.get("relations_file")
        try:
            ct = read_tables(cfile.filename, cfile.read()) if cfile and cfile.filename else None
            rt = read_tables(rfile.filename, rfile.read()) if rfile and rfile.filename else None
        except ImportFileError as e:
            return {"imported": False, "errors": [str(e)], "warnings": []}, 400
        c_rows, r_rows = tables_to_rows(ct, rt)
        if not c_rows and not r_rows:
            return {"imported": False, "errors": ["choose a concepts and/or relations file with at least one row"],
                    "warnings": []}, 400
        known = [] if replace else [c["concept_id"] for c in m.list_concepts()]
        res: ImportResult = parse_bundle(c_rows, r_rows, known)
        return _apply(res, replace, skip_invalid)

    def _apply(res, replace: bool, skip_invalid: bool) -> tuple[dict, int]:
        body = {"imported": False, **res.summary()}
        if res.errors and not skip_invalid:
            body["message"] = "Nothing imported: fix the listed rows, or allow importing the valid rows only."
            return body, 400
        if not res.concepts and not res.relations:
            body["message"] = "No valid rows to import."
            return body, 400
        out = get_model().import_data(res.concepts, res.relations, replace=replace)
        body.update(imported=True, result=out,
                    message=f"Imported {len(res.concepts)} concept(s) and {len(res.relations)} relation(s).")
        return body, 200

    @app.route("/import", methods=["GET", "POST"])
    def import_page():
        outcome = None
        if request.method == "POST":
            outcome, _ = _import_uploads(request.form, request.files)
        return render_template(
            "import.html",
            outcome=outcome,
            stats=get_model().dashboard_stats(),
            empty=request.args.get("empty") == "1",
            template_files=TEMPLATE_FILES,
        )

    @app.route("/import/demo", methods=["POST"])
    def import_demo():
        from data.mock_corpus import get_concepts, get_relations
        replace = request.form.get("replace") in ("1", "true", "on", "yes")
        get_model().import_data(get_concepts(), get_relations(), replace=replace)
        return redirect(url_for("dashboard"))

    @app.route("/templates/<name>")
    def download_template(name: str):
        if name not in TEMPLATE_FILES:
            abort(404)
        return send_from_directory(TEMPLATES_DIR, name, as_attachment=True)

    @app.route("/export/<kind>.csv")
    def export_csv(kind: str):
        from data.importer import concepts_to_csv, relations_to_csv
        m = get_model()
        if kind == "concepts":
            text = concepts_to_csv(m.list_concepts())
        elif kind == "relations":
            text = relations_to_csv(m.list_relations())
        else:
            abort(404)
        return Response(text, mimetype="text/csv",
                        headers={"Content-Disposition": f"attachment; filename={kind}.csv"})

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

    @app.route("/api/v1/import", methods=["POST"])
    def api_import():
        """
        multipart/form-data: concepts_file, relations_file, replace, skip_invalid
        or JSON: {"concepts": [...], "relations": [...], "replace": false, "skip_invalid": false}
        """
        if request.files:
            body, status = _import_uploads(request.form, request.files)
            return jsonify(body), status
        from data.importer import parse_bundle
        data = request.get_json(force=True, silent=True)
        if not isinstance(data, dict) or not (data.get("concepts") or data.get("relations")):
            return jsonify({"imported": False, "errors": [
                'send multipart files or JSON {"concepts": [...], "relations": [...]}'], "warnings": []}), 400
        replace = bool(data.get("replace"))
        known = [] if replace else [c["concept_id"] for c in get_model().list_concepts()]
        res = parse_bundle(data.get("concepts") or [], data.get("relations") or [], known)
        body, status = _apply(res, replace, bool(data.get("skip_invalid")))
        return jsonify(body), status

    @app.route("/api/v1/demo", methods=["POST"])
    def api_demo():
        from data.mock_corpus import get_concepts, get_relations
        data = request.get_json(force=True, silent=True) or {}
        out = get_model().import_data(get_concepts(), get_relations(), replace=bool(data.get("replace")))
        return jsonify(out)

    return app

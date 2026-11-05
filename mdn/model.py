"""SQLite persistence layer for Mathematical Discovery Navigator."""
from __future__ import annotations
import json
import sqlite3
from datetime import datetime


class Model:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._cached_conn: sqlite3.Connection | None = None
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        if self.db_path == ":memory:":
            if self._cached_conn is None:
                self._cached_conn = sqlite3.connect(":memory:", check_same_thread=False)
                self._cached_conn.row_factory = sqlite3.Row
            return self._cached_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS concepts (
                    concept_id TEXT PRIMARY KEY,
                    name TEXT,
                    domain TEXT,
                    concept_type TEXT,
                    year_introduced INTEGER,
                    abstract TEXT,
                    authors_json TEXT,
                    citation_count INTEGER,
                    importance_score REAL,
                    proven INTEGER,
                    downstream_theorems INTEGER,
                    cross_domain_json TEXT,
                    analyzed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS relations (
                    relation_id TEXT PRIMARY KEY,
                    source_id TEXT,
                    target_id TEXT,
                    relation_type TEXT
                );
                CREATE TABLE IF NOT EXISTS fruitfulness_predictions (
                    concept_id TEXT PRIMARY KEY,
                    domain TEXT,
                    expected_theorem_yield REAL,
                    citation_impact_score REAL,
                    new_subfield_probability REAL,
                    cross_disciplinary_score REAL,
                    proof_difficulty_estimate REAL,
                    overall_fruitfulness REAL,
                    confidence REAL,
                    explanation TEXT,
                    comparable_historical_json TEXT,
                    analyzed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS conjecture_scores (
                    concept_id TEXT PRIMARY KEY,
                    name TEXT,
                    domain TEXT,
                    novelty_score REAL,
                    importance_score REAL,
                    connectivity_score REAL,
                    generalization_score REAL,
                    depth_estimate REAL,
                    expected_downstream INTEGER,
                    predicted_proof_complexity TEXT,
                    historical_analogues_json TEXT,
                    related_conjectures_json TEXT,
                    research_roadmap_json TEXT,
                    overall_rank INTEGER,
                    analyzed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS curiosity_insights (
                    insight_id TEXT PRIMARY KEY,
                    insight_type TEXT,
                    concept_ids_json TEXT,
                    description TEXT,
                    potential_score REAL,
                    suggested_question TEXT,
                    recommended_action TEXT,
                    analyzed_at TEXT
                );
            """)

    # ------------------------------------------------------------------
    # Concepts
    # ------------------------------------------------------------------

    def add_concept(self, data: dict) -> dict:
        now = datetime.utcnow().isoformat()
        authors = data.get("authors", [])
        cross = data.get("cross_domain_influence", [])
        with self._conn() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO concepts
                   (concept_id, name, domain, concept_type, year_introduced, abstract,
                    authors_json, citation_count, importance_score, proven,
                    downstream_theorems, cross_domain_json, analyzed_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    data["concept_id"],
                    data.get("name", ""),
                    data.get("domain", ""),
                    data.get("concept_type", ""),
                    data.get("year_introduced", 0),
                    data.get("abstract", ""),
                    json.dumps(authors) if isinstance(authors, list) else authors,
                    data.get("citation_count", 0),
                    data.get("importance_score", 0.0),
                    1 if data.get("proven", False) else 0,
                    data.get("downstream_theorems", 0),
                    json.dumps(cross) if isinstance(cross, list) else cross,
                    now,
                ),
            )
        return self.get_concept(data["concept_id"])

    def get_concept(self, concept_id: str) -> dict | None:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM concepts WHERE concept_id=?", (concept_id,)).fetchone()
        if not row:
            return None
        return self._deserialize_concept(dict(row))

    def list_concepts(self, domain: str | None = None, concept_type: str | None = None) -> list[dict]:
        with self._conn() as conn:
            if domain and concept_type:
                rows = conn.execute(
                    "SELECT * FROM concepts WHERE domain=? AND concept_type=? ORDER BY importance_score DESC",
                    (domain, concept_type)
                ).fetchall()
            elif domain:
                rows = conn.execute(
                    "SELECT * FROM concepts WHERE domain=? ORDER BY importance_score DESC", (domain,)
                ).fetchall()
            elif concept_type:
                rows = conn.execute(
                    "SELECT * FROM concepts WHERE concept_type=? ORDER BY importance_score DESC", (concept_type,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM concepts ORDER BY importance_score DESC"
                ).fetchall()
        return [self._deserialize_concept(dict(r)) for r in rows]

    def _deserialize_concept(self, row: dict) -> dict:
        row["authors"] = json.loads(row.pop("authors_json", "[]") or "[]")
        row["cross_domain_influence"] = json.loads(row.pop("cross_domain_json", "[]") or "[]")
        row["proven"] = bool(row.get("proven", 0))
        return row

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    def add_relation(self, data: dict) -> dict:
        rel_id = f"{data['source_id']}-{data['target_id']}-{data['relation_type']}"
        with self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO relations (relation_id, source_id, target_id, relation_type) VALUES (?,?,?,?)",
                (rel_id, data["source_id"], data["target_id"], data["relation_type"]),
            )
        return data

    def list_relations(self, source_id: str | None = None) -> list[dict]:
        with self._conn() as conn:
            if source_id:
                rows = conn.execute(
                    "SELECT * FROM relations WHERE source_id=?", (source_id,)
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM relations").fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Fruitfulness predictions
    # ------------------------------------------------------------------

    def upsert_fruitfulness_prediction(self, prediction) -> None:
        now = datetime.utcnow().isoformat()
        with self._conn() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO fruitfulness_predictions
                   (concept_id, domain, expected_theorem_yield, citation_impact_score,
                    new_subfield_probability, cross_disciplinary_score, proof_difficulty_estimate,
                    overall_fruitfulness, confidence, explanation, comparable_historical_json, analyzed_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    prediction.concept_id,
                    prediction.domain,
                    prediction.expected_theorem_yield,
                    prediction.citation_impact_score,
                    prediction.new_subfield_probability,
                    prediction.cross_disciplinary_score,
                    prediction.proof_difficulty_estimate,
                    prediction.overall_fruitfulness,
                    prediction.confidence,
                    prediction.explanation,
                    json.dumps(prediction.comparable_historical),
                    now,
                ),
            )

    def list_fruitfulness_predictions(self, domain: str | None = None) -> list[dict]:
        with self._conn() as conn:
            if domain:
                rows = conn.execute(
                    "SELECT * FROM fruitfulness_predictions WHERE domain=? ORDER BY overall_fruitfulness DESC",
                    (domain,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM fruitfulness_predictions ORDER BY overall_fruitfulness DESC"
                ).fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r["comparable_historical"] = json.loads(r.pop("comparable_historical_json", "[]") or "[]")
            result.append(r)
        return result

    # ------------------------------------------------------------------
    # Conjecture scores
    # ------------------------------------------------------------------

    def upsert_conjecture_score(self, score) -> None:
        now = datetime.utcnow().isoformat()
        with self._conn() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO conjecture_scores
                   (concept_id, name, domain, novelty_score, importance_score, connectivity_score,
                    generalization_score, depth_estimate, expected_downstream, predicted_proof_complexity,
                    historical_analogues_json, related_conjectures_json, research_roadmap_json,
                    overall_rank, analyzed_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    score.concept_id,
                    score.name,
                    score.domain,
                    score.novelty_score,
                    score.importance_score,
                    score.connectivity_score,
                    score.generalization_score,
                    score.depth_estimate,
                    score.expected_downstream,
                    score.predicted_proof_complexity,
                    json.dumps(score.historical_analogues),
                    json.dumps(score.related_conjectures),
                    json.dumps(score.research_roadmap),
                    score.overall_rank,
                    now,
                ),
            )

    def list_conjecture_scores(self) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM conjecture_scores ORDER BY overall_rank ASC"
            ).fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r["historical_analogues"] = json.loads(r.pop("historical_analogues_json", "[]") or "[]")
            r["related_conjectures"] = json.loads(r.pop("related_conjectures_json", "[]") or "[]")
            r["research_roadmap"] = json.loads(r.pop("research_roadmap_json", "[]") or "[]")
            result.append(r)
        return result

    # ------------------------------------------------------------------
    # Curiosity insights
    # ------------------------------------------------------------------

    def upsert_curiosity_insight(self, insight, insight_id: str) -> None:
        now = datetime.utcnow().isoformat()
        with self._conn() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO curiosity_insights
                   (insight_id, insight_type, concept_ids_json, description, potential_score,
                    suggested_question, recommended_action, analyzed_at)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (
                    insight_id,
                    insight.insight_type,
                    json.dumps(insight.concept_ids),
                    insight.description,
                    insight.potential_score,
                    insight.suggested_question,
                    insight.recommended_action,
                    now,
                ),
            )

    def list_curiosity_insights(self) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM curiosity_insights ORDER BY potential_score DESC"
            ).fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r["concept_ids"] = json.loads(r.pop("concept_ids_json", "[]") or "[]")
            result.append(r)
        return result

    # ------------------------------------------------------------------
    # Bulk load / reset
    # ------------------------------------------------------------------

    def clear_all(self) -> None:
        """Delete every concept, relation and derived analysis row."""
        with self._conn() as conn:
            for table in ("concepts", "relations", "fruitfulness_predictions",
                          "conjecture_scores", "curiosity_insights"):
                conn.execute(f"DELETE FROM {table}")

    def clear_analysis(self) -> None:
        """Drop derived rows so a re-run never leaves stale predictions behind."""
        with self._conn() as conn:
            for table in ("fruitfulness_predictions", "conjecture_scores", "curiosity_insights"):
                conn.execute(f"DELETE FROM {table}")

    def import_data(self, concepts: list[dict], relations: list[dict],
                    replace: bool = False, analyze: bool = True) -> dict:
        """
        Store validated concepts/relations (see data/importer.py) and, by
        default, re-run the full analysis. replace=True wipes existing data
        first; otherwise rows are merged (same concept_id is overwritten).
        """
        if replace:
            self.clear_all()
        for c in concepts:
            self.add_concept(c)
        for r in relations:
            self.add_relation(r)
        out = {"concepts_imported": len(concepts), "relations_imported": len(relations)}
        if analyze:
            self.clear_analysis()
            out["analysis"] = self.run_full_analysis()
        return out

    # ------------------------------------------------------------------
    # Analysis orchestration
    # ------------------------------------------------------------------

    def run_full_analysis(self) -> dict:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

        from engine.knowledge_graph import MathKnowledgeGraph
        from engine.embedding_engine import EmbeddingEngine
        from engine.fruitfulness_predictor import FruitfulnessPredictor
        from engine.conjecture_ranker import ConjectureRanker
        from engine.curiosity_engine import CuriosityEngine

        concepts = self.list_concepts()
        relations = self.list_relations()

        if not concepts:
            return {"fruitfulness": 0, "conjectures": 0, "insights": 0}

        # Build knowledge graph
        kg = MathKnowledgeGraph()
        for c in concepts:
            kg.add_concept(c)
        for r in relations:
            kg.add_relation(r["source_id"], r["target_id"], r["relation_type"])

        # Fit embedding engine
        embeddings = EmbeddingEngine(n_components=min(50, len(concepts)))
        embeddings.fit(concepts)

        # Fruitfulness predictions
        predictor = FruitfulnessPredictor()
        predictions = predictor.rank_all(concepts, kg, embeddings)
        for p in predictions:
            self.upsert_fruitfulness_prediction(p)

        # Conjecture rankings
        ranker = ConjectureRanker()
        scores = ranker.rank_conjectures(kg, embeddings)
        for s in scores:
            self.upsert_conjecture_score(s)

        # Curiosity insights
        curiosity = CuriosityEngine()
        insights = curiosity.find_insights(kg, embeddings)
        for i, ins in enumerate(insights):
            self.upsert_curiosity_insight(ins, f"INS-{i+1:03d}")

        return {
            "fruitfulness": len(predictions),
            "conjectures": len(scores),
            "insights": len(insights),
        }

    def dashboard_stats(self) -> dict:
        concepts = self.list_concepts()
        relations = self.list_relations()
        predictions = self.list_fruitfulness_predictions()
        insights = self.list_curiosity_insights()
        scores = self.list_conjecture_scores()

        domains = list({c["domain"] for c in concepts})
        top_fruitfulness = predictions[:5] if predictions else []
        critical_insights = [i for i in insights if i.get("potential_score", 0) >= 0.8]

        return {
            "total_concepts": len(concepts),
            "total_relations": len(relations),
            "domains_covered": len(domains),
            "domains": domains,
            "top_fruitfulness": top_fruitfulness,
            "critical_insights": len(critical_insights),
            "conjectures_ranked": len(scores),
            "total_insights": len(insights),
        }

    def copilot_query(self, text: str) -> dict:
        from engine.knowledge_graph import MathKnowledgeGraph
        from engine.embedding_engine import EmbeddingEngine

        concepts = self.list_concepts()
        if not concepts:
            return {
                "related_concepts": [],
                "research_gaps": [],
                "predictions": [],
                "open_problems": [],
                "explanation": "No mathematical concepts loaded.",
            }

        kg = MathKnowledgeGraph()
        for c in concepts:
            kg.add_concept(c)
        for r in self.list_relations():
            kg.add_relation(r["source_id"], r["target_id"], r["relation_type"])

        embeddings = EmbeddingEngine(n_components=min(30, len(concepts)))
        embeddings.fit(concepts)

        query_vec = embeddings.embed(text)
        if not query_vec:
            return {
                "related_concepts": [],
                "research_gaps": [],
                "predictions": [],
                "open_problems": [],
                "explanation": "Could not embed query.",
            }

        # Find most similar concepts
        import math
        sims = []
        for cid, emb in embeddings._embeddings.items():
            na = math.sqrt(sum(x * x for x in query_vec))
            nb = math.sqrt(sum(x * x for x in emb))
            if na > 0 and nb > 0:
                dot = sum(a * b for a, b in zip(query_vec, emb))
                sims.append((cid, max(0.0, dot / (na * nb))))
        sims.sort(key=lambda x: x[1], reverse=True)
        top_ids = [s[0] for s in sims[:5]]
        related = [kg.get_concept(cid) for cid in top_ids if kg.get_concept(cid)]

        # Research gaps: retrieve top curiosity insights
        insights = self.list_curiosity_insights()
        gaps = [i["description"] for i in insights[:3]]

        # Predictions for top related concepts
        preds = self.list_fruitfulness_predictions()
        pred_map = {p["concept_id"]: p for p in preds}
        predictions_out = [pred_map[c["concept_id"]] for c in related if c["concept_id"] in pred_map][:3]

        # Open problems from conjectures
        open_problems = [
            c["name"] for c in concepts
            if c.get("concept_type") == "conjecture" and not c.get("proven", False)
        ][:5]

        related_names = [c["name"] for c in related[:3]]
        explanation = (
            f"Query matched most closely with: {', '.join(related_names)}. "
            f"Found {len(gaps)} relevant research gaps and {len(open_problems)} open problems."
        )

        return {
            "related_concepts": related,
            "research_gaps": gaps,
            "predictions": predictions_out,
            "open_problems": open_problems,
            "explanation": explanation,
        }

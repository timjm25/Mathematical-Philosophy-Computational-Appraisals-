import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import io
import json
from pathlib import Path

import pytest

from data.connectors import ArxivConnector, ConnectorError
from data.importer import parse_concepts
from mdn import cli
from mdn.app import create_app
from mdn.model import Model

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "data" / "templates"
FEED = (Path(__file__).parent / "fixtures" / "arxiv_feed.xml").read_text()


def _upload(c, concepts=None, relations=None, **form):
    data = dict(form)
    if concepts is not None:
        data["concepts_file"] = (io.BytesIO(concepts[1]), concepts[0])
    if relations is not None:
        data["relations_file"] = (io.BytesIO(relations[1]), relations[0])
    return data


def _templates():
    return (("concepts.csv", (TEMPLATES / "concepts_template.csv").read_bytes()),
            ("relations.csv", (TEMPLATES / "relations_template.csv").read_bytes()))


# ---------------------------------------------------------------------------
# Web app
# ---------------------------------------------------------------------------

class TestAppImport:
    def test_empty_db_without_demo_redirects_to_import(self):
        c = create_app(":memory:", seed_demo=False).test_client()
        r = c.get("/")
        assert r.status_code == 302 and "/import" in r.headers["Location"]
        assert c.get("/api/v1/concepts").get_json() == []
        assert b"database is empty" in c.get("/import?empty=1").data

    def test_env_flag_disables_demo(self, monkeypatch):
        monkeypatch.setenv("MDN_SEED_DEMO", "0")
        c = create_app(":memory:").test_client()
        assert c.get("/api/v1/stats").get_json()["total_concepts"] == 0

    def test_demo_still_default(self, monkeypatch):
        monkeypatch.delenv("MDN_SEED_DEMO", raising=False)
        c = create_app(":memory:").test_client()
        assert c.get("/api/v1/stats").get_json()["total_concepts"] == 80

    def test_upload_page_then_every_page_renders_user_data(self):
        c = create_app(":memory:", seed_demo=False).test_client()
        cf, rf = _templates()
        r = c.post("/import", data=_upload(c, cf, rf), content_type="multipart/form-data")
        assert r.status_code == 200 and b"Imported 5 concept(s) and 4 relation(s)" in r.data
        for page in ["/", "/graph", "/conjecture", "/explore", "/history", "/copilot?q=prime"]:
            assert c.get(page).status_code == 200, page
        names = {x["name"] for x in c.get("/api/v1/concepts").get_json()}
        assert "Persistent Homology" in names
        assert [s["name"] for s in c.get("/api/v1/conjectures").get_json()] == ["Twin Prime Conjecture"]

    def test_invalid_rows_block_import_and_are_listed(self):
        c = create_app(":memory:", seed_demo=False).test_client()
        bad = (b"concept_id,name,domain,concept_type,year_introduced,importance_score\n"
               b"A,Good,Logic,axiom,1900,0.5\nB,Bad,Logic,axiom,1900,7\n")
        r = c.post("/import", data=_upload(c, ("c.csv", bad)), content_type="multipart/form-data")
        assert b"Nothing imported" in r.data and b"concepts row 3 (B)" in r.data
        assert c.get("/api/v1/stats").get_json()["total_concepts"] == 0
        r = c.post("/import", data=_upload(c, ("c.csv", bad), skip_invalid="1"),
                   content_type="multipart/form-data")
        assert b"Imported 1 concept(s)" in r.data

    def test_api_multipart_and_json(self):
        c = create_app(":memory:").test_client()          # demo loaded
        cf, rf = _templates()
        r = c.post("/api/v1/import", data=_upload(c, cf, rf, replace="1"),
                   content_type="multipart/form-data")
        body = r.get_json()
        assert r.status_code == 200 and body["imported"] and body["concepts"] == 5
        assert c.get("/api/v1/stats").get_json()["total_concepts"] == 5
        # JSON merge, relation pointing at a concept already in the DB
        r = c.post("/api/v1/import", json={
            "concepts": [{"concept_id": "N1", "name": "New", "domain": "Topology",
                          "concept_type": "theorem", "year_introduced": 2020}],
            "relations": [{"source_id": "N1", "target_id": "SAMPLE-002", "relation_type": "uses"}]})
        assert r.status_code == 200
        assert c.get("/api/v1/stats").get_json()["total_concepts"] == 6
        r = c.post("/api/v1/import", json={"relations": [
            {"source_id": "N1", "target_id": "NOPE", "relation_type": "uses"}]})
        assert r.status_code == 400 and "NOPE" in r.get_json()["errors"][0]
        assert c.post("/api/v1/import", json={}).status_code == 400

    def test_api_rejects_bad_file_type(self):
        c = create_app(":memory:", seed_demo=False).test_client()
        r = c.post("/api/v1/import", data=_upload(c, ("c.pdf", b"%PDF")),
                   content_type="multipart/form-data")
        assert r.status_code == 400 and "unsupported file type" in r.get_json()["errors"][0]

    def test_demo_button_templates_and_export(self):
        c = create_app(":memory:", seed_demo=False).test_client()
        assert c.post("/import/demo").status_code == 302
        assert c.get("/api/v1/stats").get_json()["total_concepts"] == 80
        r = c.get("/templates/concepts_template.csv")
        assert r.status_code == 200 and r.data.startswith(b"concept_id,name")
        assert c.get("/templates/secret.txt").status_code == 404
        exp = c.get("/export/concepts.csv")
        assert exp.status_code == 200 and exp.data.count(b"\n") == 81
        assert c.get("/export/relations.csv").data.startswith(b"source_id,target_id,relation_type")
        assert c.get("/export/other.csv").status_code == 404
        assert c.post("/api/v1/demo", json={"replace": True}).status_code == 200


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class TestCli:
    def test_import_dry_run_then_real(self, tmp_path, capsys):
        db = str(tmp_path / "t.db")
        args = ["--db", db, "import", "--concepts", str(TEMPLATES / "concepts_template.csv"),
                "--relations", str(TEMPLATES / "relations_template.csv")]
        assert cli.main(args + ["--dry-run"]) == 0
        assert Model(db).list_concepts() == []
        assert cli.main(args) == 0
        m = Model(db)
        assert len(m.list_concepts()) == 5 and len(m.list_fruitfulness_predictions()) == 5

    def test_import_errors_write_nothing(self, tmp_path, capsys):
        db = str(tmp_path / "t.db")
        p = tmp_path / "bad.csv"
        p.write_text("concept_id,name,domain,concept_type,year_introduced\nA,,Logic,axiom,x\n")
        assert cli.main(["--db", db, "import", "--concepts", str(p)]) == 2
        err = capsys.readouterr().err
        assert "'name' is empty" in err and "not a whole number" in err
        assert Model(db).list_concepts() == []

    def test_demo_export_clear(self, tmp_path, capsys):
        db = str(tmp_path / "t.db")
        assert cli.main(["--db", db, "demo"]) == 0
        out = tmp_path / "exp"
        assert cli.main(["--db", db, "export", "--out-dir", str(out)]) == 0
        assert (out / "concepts.csv").read_text().count("\n") == 81
        # exported files re-import cleanly into a fresh database
        db2 = str(tmp_path / "t2.db")
        assert cli.main(["--db", db2, "import", "--concepts", str(out / "concepts.csv"),
                         "--relations", str(out / "relations.csv")]) == 0
        assert len(Model(db2).list_concepts()) == 80
        assert cli.main(["--db", db, "clear"]) == 2          # needs --yes
        assert cli.main(["--db", db, "clear", "--yes"]) == 0
        assert Model(db).list_concepts() == []

    def test_analyze_and_stats(self, tmp_path, capsys):
        db = str(tmp_path / "t.db")
        cli.main(["--db", db, "demo"])
        capsys.readouterr()
        assert cli.main(["--db", db, "analyze"]) == 0
        assert json.loads(capsys.readouterr().out)["fruitfulness"] == 80
        assert cli.main(["--db", db, "stats"]) == 0
        assert json.loads(capsys.readouterr().out)["total_concepts"] == 80

    def test_arxiv_command_uses_connector(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr("data.connectors.ArxivConnector._http_get", lambda self, url: FEED)
        db = str(tmp_path / "t.db")
        saved = tmp_path / "arxiv.csv"
        assert cli.main(["--db", db, "arxiv", "persistence", "--max", "2",
                         "--save-csv", str(saved)]) == 0
        ids = {c["concept_id"] for c in Model(db).list_concepts()}
        assert ids == {"arXiv:2401.00001", "arXiv:2312.09999"}
        assert saved.read_text().startswith("concept_id,name")

    def test_arxiv_network_failure_is_clean(self, tmp_path, monkeypatch, capsys):
        def boom(self, url):
            raise ConnectorError("could not reach arXiv (offline)")
        monkeypatch.setattr("data.connectors.ArxivConnector._http_get", boom)
        assert cli.main(["--db", str(tmp_path / "t.db"), "arxiv", "x"]) == 3
        assert "could not reach arXiv" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# arXiv connector
# ---------------------------------------------------------------------------

class TestArxivConnector:
    def test_parse_feed_maps_to_schema(self):
        concepts = ArxivConnector(fetch=lambda url: FEED).fetch_concepts("persistence")
        a, b = concepts
        assert a["concept_id"] == "arXiv:2401.00001"          # version suffix dropped
        assert a["name"] == "Example Stability Results for Persistence Diagrams"
        assert a["domain"] == "Topology" and a["cross_domain_influence"] == ["Combinatorics"]
        assert a["year_introduced"] == "2024" and a["authors"] == ["Example Author One", "Example Author Two"]
        assert b["domain"] == "Number Theory"
        res = parse_concepts(concepts)
        assert res.ok and res.concepts[0]["year_introduced"] == 2024

    def test_build_url(self):
        conn = ArxivConnector(fetch=lambda u: FEED, base_url="https://example.invalid/api")
        url = conn.build_url("ricci flow", 5)
        assert url.startswith("https://example.invalid/api?") and "max_results=5" in url
        assert "all%3A%22ricci+flow%22" in url
        assert "cat%3Amath.AG" in conn.build_url("cat:math.AG AND all:schemes")
        with pytest.raises(ConnectorError):
            conn.build_url("", 5)
        with pytest.raises(ConnectorError):
            conn.build_url("x", 500)

    def test_bad_xml(self):
        with pytest.raises(ConnectorError, match="not valid XML"):
            ArxivConnector(fetch=lambda u: "<feed").fetch_concepts("x")

    def test_conjecture_type_marks_unproven(self):
        cs = ArxivConnector(fetch=lambda u: FEED).fetch_concepts("x", concept_type="conjecture")
        assert all(c["proven"] is False for c in cs)

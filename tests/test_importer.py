import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import io
import json
from pathlib import Path

import pytest

from data.importer import (
    CONCEPT_COLUMNS, ImportFileError, concepts_to_csv, load_files, parse_bundle,
    parse_concepts, parse_relations, read_tables, relations_to_csv,
)
from data.mock_corpus import get_concepts, get_relations
from mdn.model import Model

TEMPLATES = Path(__file__).resolve().parent.parent / "data" / "templates"
HEADER = ",".join(CONCEPT_COLUMNS)


def _row(**kw):
    base = {"concept_id": "X1", "name": "Thing", "domain": "Topology",
            "concept_type": "theorem", "year_introduced": "1900"}
    base.update(kw)
    return base


class TestTemplates:
    def test_template_header_matches_schema(self):
        header = (TEMPLATES / "concepts_template.csv").read_text().splitlines()[0]
        assert header == HEADER
        assert (TEMPLATES / "relations_template.csv").read_text().splitlines()[0] == \
            "source_id,target_id,relation_type"

    def test_templates_import_cleanly(self):
        res = load_files(TEMPLATES / "concepts_template.csv", TEMPLATES / "relations_template.csv")
        assert res.ok, res.errors
        assert len(res.concepts) == 5 and len(res.relations) == 4
        assert all(c["concept_id"].startswith("SAMPLE-") for c in res.concepts)
        twin = next(c for c in res.concepts if c["concept_type"] == "conjecture")
        assert twin["proven"] is False and twin["cross_domain_influence"] == ["Combinatorics"]


class TestConceptValidation:
    def test_defaults_and_types(self):
        res = parse_concepts([_row(authors="A; B", proven="yes")])
        c = res.concepts[0]
        assert c["year_introduced"] == 1900 and c["citation_count"] == 0
        assert c["importance_score"] == 0.5 and c["proven"] is True
        assert c["authors"] == ["A", "B"]

    def test_case_insensitive_headers_and_ontology_values(self):
        res = parse_concepts([{"Concept_ID": "X1", "Name": "T", "Domain": "number theory",
                               "Concept_Type": "Conjecture", "Year_Introduced": "1742"}])
        assert res.ok
        assert res.concepts[0]["domain"] == "Number Theory"
        assert res.concepts[0]["concept_type"] == "conjecture"

    def test_unknown_domain_is_a_warning_not_an_error(self):
        res = parse_concepts([_row(domain="Tropical Geometry", abstract="x")])
        assert res.ok and res.concepts[0]["domain"] == "Tropical Geometry"
        assert any("not in the ontology" in w for w in res.warnings)

    @pytest.mark.parametrize("field, value, fragment", [
        ("year_introduced", "nineteen", "not a whole number"),
        ("year_introduced", "99999", "is above"),
        ("citation_count", "-3", "below 0"),
        ("importance_score", "1.7", "between 0 and 1"),
        ("proven", "maybe", "true/false"),
        ("name", "", "'name' is empty"),
    ])
    def test_bad_values_name_row_and_field(self, field, value, fragment):
        res = parse_concepts([_row(), _row(concept_id="X2", **{field: value})])
        assert len(res.concepts) == 1
        assert any(e.startswith("concepts row 3 (X2)") and fragment in e for e in res.errors), res.errors

    def test_duplicate_id(self):
        res = parse_concepts([_row(), _row()])
        assert "duplicate concept_id (first on row 2)" in res.errors[0]

    def test_missing_required_column(self):
        with pytest.raises(ImportFileError, match="missing required column.*year_introduced"):
            parse_concepts([{"concept_id": "X", "name": "n", "domain": "d", "concept_type": "theorem"}])


class TestRelationValidation:
    def test_unknown_ids_type_and_self_loop(self):
        res = parse_relations(
            [{"source_id": "A", "target_id": "B", "relation_type": "depends_on"},
             {"source_id": "A", "target_id": "Z", "relation_type": "depends_on"},
             {"source_id": "A", "target_id": "B", "relation_type": "likes"},
             {"source_id": "A", "target_id": "A", "relation_type": "uses"},
             {"source_id": "A", "target_id": "B", "relation_type": "Depends On"}],
            known_ids=["A", "B"],
        )
        assert [r["relation_type"] for r in res.relations] == ["depends_on", "likes"]
        joined = "\n".join(res.errors)
        assert "target_id 'Z' is not a known concept_id" in joined
        assert "are the same" in joined
        assert any("relation_type 'likes' is not in the ontology" in w for w in res.warnings)
        assert any("duplicate relation" in w for w in res.warnings)

    def test_relations_may_reference_existing_db_ids(self):
        res = parse_bundle([_row(concept_id="NEW")],
                           [{"source_id": "NEW", "target_id": "C001", "relation_type": "uses"}],
                           known_ids=["C001"])
        assert res.ok and len(res.relations) == 1


class TestFileFormats:
    def test_csv_tsv_json(self, tmp_path):
        csv_p = tmp_path / "c.csv"
        csv_p.write_text("concept_id,name,domain,concept_type,year_introduced\nA,a,Logic,axiom,1900\n")
        tsv_p = tmp_path / "c.tsv"
        tsv_p.write_text("concept_id\tname\tdomain\tconcept_type\tyear_introduced\nB\tb\tLogic\taxiom\t1901\n")
        json_p = tmp_path / "b.json"
        json_p.write_text(json.dumps({
            "concepts": [_row(concept_id="J1", authors=["X", "Y"], proven=True, year_introduced=1950),
                         _row(concept_id="J2")],
            "relations": [{"source_id": "J1", "target_id": "J2", "relation_type": "extends"}]}))
        assert load_files(csv_p).concepts[0]["concept_id"] == "A"
        assert load_files(tsv_p).concepts[0]["year_introduced"] == 1901
        res = load_files(json_p)
        assert res.ok and res.concepts[0]["authors"] == ["X", "Y"] and len(res.relations) == 1

    def test_xlsx_two_sheets(self, tmp_path):
        openpyxl = pytest.importorskip("openpyxl")
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Concepts"
        ws.append(["concept_id", "name", "domain", "concept_type", "year_introduced", "proven"])
        ws.append(["E1", "First", "Algebra", "theorem", 1832, True])
        ws.append(["E2", "Second", "Algebra", "conjecture", 1900.0, 0])
        rs = wb.create_sheet("Relations")
        rs.append(["source_id", "target_id", "relation_type"])
        rs.append(["E2", "E1", "motivated_by"])
        p = tmp_path / "corpus.xlsx"
        wb.save(p)
        res = load_files(p)
        assert res.ok, res.errors
        assert [c["year_introduced"] for c in res.concepts] == [1832, 1900]
        assert res.concepts[1]["proven"] is False and len(res.relations) == 1

    def test_file_level_errors(self, tmp_path):
        assert "unsupported file type" in load_files(tmp_path / "c.docx").errors[0]
        assert "file not found" in load_files(tmp_path / "c.csv").errors[0]
        with pytest.raises(ImportFileError, match="invalid JSON"):
            read_tables("x.json", b"{not json")
        with pytest.raises(ImportFileError, match="not UTF-8"):
            read_tables("x.csv", "concept_id\n\xe9".encode("latin-1"))
        with pytest.raises(ImportFileError, match="could not open the Excel file"):
            pytest.importorskip("openpyxl")
            read_tables("x.xlsx", b"not a zip")


class TestModelImportAndExport:
    def test_import_replace_and_merge(self):
        m = Model()
        m.import_data(get_concepts(), get_relations())
        assert len(m.list_concepts()) == 80
        res = load_files(TEMPLATES / "concepts_template.csv", TEMPLATES / "relations_template.csv")
        out = m.import_data(res.concepts, res.relations, replace=True)
        assert len(m.list_concepts()) == 5 and len(m.list_relations()) == 4
        assert out["analysis"]["fruitfulness"] == 5
        assert {p["concept_id"] for p in m.list_fruitfulness_predictions()} == \
            {c["concept_id"] for c in res.concepts}
        assert [s["name"] for s in m.list_conjecture_scores()] == ["Twin Prime Conjecture"]

    def test_export_round_trips(self):
        concepts, relations = get_concepts(), get_relations()
        c_text, r_text = concepts_to_csv(concepts), relations_to_csv(relations)
        res = parse_bundle(read_tables("c.csv", c_text.encode())["rows"],
                           read_tables("r.csv", r_text.encode())["rows"])
        assert res.ok, res.errors[:3]
        assert len(res.concepts) == len(concepts)
        assert len(res.relations) == len({(r["source_id"], r["target_id"], r["relation_type"]) for r in relations})
        orig = {c["concept_id"]: c for c in concepts}
        for c in res.concepts:
            o = orig[c["concept_id"]]
            assert c["authors"] == o["authors"] and c["proven"] == o["proven"]
            assert c["year_introduced"] == o["year_introduced"]

    def test_clear_all(self):
        m = Model()
        m.import_data(get_concepts()[:5], [], analyze=True)
        m.clear_all()
        assert m.list_concepts() == [] and m.list_fruitfulness_predictions() == []

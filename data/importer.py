"""Import your own concepts and relations from CSV, TSV, Excel (.xlsx) or JSON.

Concept columns (one row per concept)
-------------------------------------
  concept_id              required  unique text id, e.g. "AG-017"
  name                    required  display name
  domain                  required  e.g. "Algebraic Geometry" (see data/ontology.py;
                                    other domains are accepted with a warning)
  concept_type            required  one of ontology.CONCEPT_TYPES, e.g. theorem, conjecture
  year_introduced         required  integer year (negative for BCE)
  abstract                optional  free text; drives the embeddings and the copilot
  authors                 optional  names separated by ";"
  citation_count          optional  integer >= 0                    (default 0)
  importance_score        optional  number in [0, 1]                (default 0.5)
  proven                  optional  true/false, yes/no, 1/0          (default false)
  downstream_theorems     optional  integer >= 0                    (default 0)
  cross_domain_influence  optional  domains separated by ";"

Relation columns (one row per directed edge)
--------------------------------------------
  source_id      required  a concept_id (from the same import or already in the database)
  target_id      required  a concept_id
  relation_type  required  e.g. depends_on, generalizes (ontology.RELATION_TYPES;
                           other values are accepted with a warning)

JSON: {"concepts": [...], "relations": [...]} or a bare list of rows; list
fields may be JSON arrays instead of ";"-separated text.
Excel: a workbook with sheets named "concepts" and "relations" (or one sheet
per file). Headers are matched case-insensitively; unknown columns are ignored.
"""
from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

from data.ontology import CONCEPT_TYPES, DOMAINS, RELATION_TYPES

CONCEPT_COLUMNS = [
    "concept_id", "name", "domain", "concept_type", "year_introduced", "abstract",
    "authors", "citation_count", "importance_score", "proven", "downstream_theorems",
    "cross_domain_influence",
]
CONCEPT_REQUIRED = ["concept_id", "name", "domain", "concept_type", "year_introduced"]
RELATION_COLUMNS = ["source_id", "target_id", "relation_type"]
SUPPORTED_SUFFIXES = (".csv", ".tsv", ".xlsx", ".json")
LIST_SEP = ";"

_TRUE = {"true", "yes", "y", "1", "proven", "proved"}
_FALSE = {"false", "no", "n", "0", "open", ""}


class ImportFileError(ValueError):
    """The file itself cannot be read (wrong type, empty, missing columns)."""


@dataclass
class ImportResult:
    concepts: list[dict] = field(default_factory=list)
    relations: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self) -> dict:
        return {
            "concepts": len(self.concepts),
            "relations": len(self.relations),
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


# ---------------------------------------------------------------------------
# Reading tables
# ---------------------------------------------------------------------------

def _suffix(filename: str) -> str:
    s = Path(filename or "").suffix.lower()
    if s not in SUPPORTED_SUFFIXES:
        raise ImportFileError(
            f"unsupported file type {s or '(none)'!r} for {filename!r}; "
            f"use one of {', '.join(SUPPORTED_SUFFIXES)}"
        )
    return s


def _xlsx_sheets(content: bytes) -> dict[str, list[dict]]:
    try:
        import openpyxl
    except ImportError:
        raise ImportFileError(
            "reading .xlsx needs openpyxl (`python3 -m pip install openpyxl`), or save as CSV"
        ) from None
    try:
        wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    except Exception as e:  # corrupt / not really xlsx
        raise ImportFileError(f"could not open the Excel file: {e}") from None
    sheets: dict[str, list[dict]] = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            sheets[ws.title] = []
            continue
        header = [str(h).strip() if h is not None else "" for h in rows[0]]
        sheets[ws.title] = [
            {h: v for h, v in zip(header, r) if h}
            for r in rows[1:]
            if any(v not in (None, "") for v in r)
        ]
    wb.close()
    return sheets


def read_tables(filename: str, content: bytes) -> dict[str, list[dict]]:
    """
    Read a file into named tables. CSV/TSV give {"rows": [...]}; JSON gives
    "concepts"/"relations" when it is a bundle, else "rows"; XLSX gives one
    table per sheet (keyed by lower-cased sheet name, plus "rows" = first sheet).
    """
    suffix = _suffix(filename)
    if suffix == ".xlsx":
        sheets = _xlsx_sheets(content)
        out = {name.strip().lower(): rows for name, rows in sheets.items()}
        if sheets:
            out["rows"] = next(iter(sheets.values()))
        return out
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ImportFileError(f"{filename!r} is not UTF-8 text; re-save it as UTF-8 CSV") from None
    if suffix == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ImportFileError(f"invalid JSON in {filename!r}: {e}") from None
        if isinstance(data, list):
            return {"rows": data}
        if isinstance(data, dict) and ("concepts" in data or "relations" in data):
            return {k: data.get(k) or [] for k in ("concepts", "relations")}
        raise ImportFileError(
            'JSON must be a list of rows or {"concepts": [...], "relations": [...]}'
        )
    reader = csv.DictReader(io.StringIO(text), delimiter="\t" if suffix == ".tsv" else ",")
    if not reader.fieldnames:
        raise ImportFileError(f"{filename!r} is empty; expected a header row")
    return {"rows": [r for r in reader if any((v or "").strip() for v in r.values() if isinstance(v, str))]}


def read_file(path: str | Path) -> dict[str, list[dict]]:
    path = Path(path)
    _suffix(path.name)
    if not path.exists():
        raise ImportFileError(f"file not found: {path}")
    return read_tables(path.name, path.read_bytes())


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _norm_row(row: dict) -> dict:
    if not isinstance(row, dict):
        return {}
    return {str(k).strip().lower(): v for k, v in row.items() if k is not None}


def _text(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def _split_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [_text(x) for x in v if _text(x)]
    return [p.strip() for p in str(v).split(LIST_SEP) if p.strip()]


def _canon(value: str, allowed: list[str]) -> str | None:
    low = value.strip().lower().replace("_", " ")
    for a in allowed:
        if a.lower().replace("_", " ") == low:
            return a
    return None


def _int(v, label: str, lo: int | None = None, hi: int | None = None) -> int:
    s = _text(v).replace(",", "")
    try:
        f = float(s)
    except ValueError:
        raise ValueError(f"{label}={_text(v)!r} is not a whole number") from None
    if not f.is_integer():
        raise ValueError(f"{label}={_text(v)!r} is not a whole number")
    n = int(f)
    if lo is not None and n < lo:
        raise ValueError(f"{label}={n} is below {lo}")
    if hi is not None and n > hi:
        raise ValueError(f"{label}={n} is above {hi}")
    return n


def _check_columns(rows: list[dict], required: list[str], what: str) -> None:
    if not rows:
        return
    present = set()
    for r in rows:
        present |= set(_norm_row(r))
    missing = [c for c in required if c not in present]
    if missing:
        raise ImportFileError(
            f"{what}: missing required column(s) {', '.join(missing)}; "
            f"found: {', '.join(sorted(present)) or 'none'}"
        )


def parse_concepts(rows: Iterable[dict], result: ImportResult | None = None) -> ImportResult:
    result = result or ImportResult()
    rows = list(rows or [])
    _check_columns(rows, CONCEPT_REQUIRED, "concepts")
    max_year = date.today().year + 1
    seen: dict[str, int] = {}
    for n, raw in enumerate(rows, start=2):        # row 1 is the header
        row = _norm_row(raw)
        where = f"concepts row {n}"
        problems: list[str] = []
        cid = _text(row.get("concept_id"))
        if cid:
            where += f" ({cid})"
        for col in CONCEPT_REQUIRED:
            if not _text(row.get(col)):
                problems.append(f"'{col}' is empty")
        if cid in seen:
            problems.append(f"duplicate concept_id (first on row {seen[cid]})")
        concept: dict = {"concept_id": cid, "name": _text(row.get("name"))}

        domain = _text(row.get("domain"))
        canon = _canon(domain, DOMAINS) if domain else None
        if domain and canon is None:
            result.warnings.append(f"{where}: domain {domain!r} is not in the ontology (kept as is)")
        concept["domain"] = canon or domain

        ctype = _text(row.get("concept_type"))
        canon = _canon(ctype, CONCEPT_TYPES) if ctype else None
        if ctype and canon is None:
            result.warnings.append(
                f"{where}: concept_type {ctype!r} is not in the ontology "
                f"(kept as is; only 'conjecture' rows are ranked as conjectures)"
            )
        concept["concept_type"] = canon or ctype

        try:
            if _text(row.get("year_introduced")):
                concept["year_introduced"] = _int(row.get("year_introduced"), "year_introduced", -3000, max_year)
        except ValueError as e:
            problems.append(str(e))
        for col in ("citation_count", "downstream_theorems"):
            try:
                concept[col] = _int(row.get(col), col, 0) if _text(row.get(col)) else 0
            except ValueError as e:
                problems.append(str(e))
        imp = _text(row.get("importance_score"))
        if imp:
            try:
                val = float(imp)
                if not 0.0 <= val <= 1.0:
                    raise ValueError
                concept["importance_score"] = val
            except ValueError:
                problems.append(f"importance_score={imp!r} must be a number between 0 and 1")
        else:
            concept["importance_score"] = 0.5
        pv = row.get("proven")
        if isinstance(pv, bool):
            concept["proven"] = pv
        else:
            ps = _text(pv).lower()
            if ps in _TRUE:
                concept["proven"] = True
            elif ps in _FALSE:
                concept["proven"] = False
            else:
                problems.append(f"proven={_text(pv)!r} must be true/false")
        concept["abstract"] = _text(row.get("abstract"))
        if not concept["abstract"] and cid:
            result.warnings.append(f"{where}: no abstract — embeddings will use only the name and domain")
        concept["authors"] = _split_list(row.get("authors"))
        concept["cross_domain_influence"] = _split_list(row.get("cross_domain_influence"))

        if problems:
            result.errors.extend(f"{where}: {p}" for p in problems)
            continue
        seen[cid] = n
        result.concepts.append(concept)
    return result


def parse_relations(
    rows: Iterable[dict],
    known_ids: Iterable[str] = (),
    result: ImportResult | None = None,
) -> ImportResult:
    result = result or ImportResult()
    rows = list(rows or [])
    _check_columns(rows, RELATION_COLUMNS, "relations")
    known = set(known_ids) | {c["concept_id"] for c in result.concepts}
    seen: set[tuple] = set()
    for n, raw in enumerate(rows, start=2):
        row = _norm_row(raw)
        where = f"relations row {n}"
        src, tgt, rtype = (_text(row.get(c)) for c in RELATION_COLUMNS)
        problems = [f"'{c}' is empty" for c, v in zip(RELATION_COLUMNS, (src, tgt, rtype)) if not v]
        canon = _canon(rtype, RELATION_TYPES) if rtype else None
        if rtype and canon is None:
            result.warnings.append(
                f"{where}: relation_type {rtype!r} is not in the ontology (kept as is; "
                f"known types: {', '.join(RELATION_TYPES)})"
            )
            canon = rtype
        for label, cid in (("source_id", src), ("target_id", tgt)):
            if cid and cid not in known:
                problems.append(f"{label} {cid!r} is not a known concept_id")
        if src and src == tgt:
            problems.append("source_id and target_id are the same")
        key = (src, tgt, canon)
        if not problems and key in seen:
            result.warnings.append(f"{where}: duplicate relation {src} -> {tgt} ({canon}) skipped")
            continue
        if problems:
            result.errors.extend(f"{where}: {p}" for p in problems)
            continue
        seen.add(key)
        result.relations.append({"source_id": src, "target_id": tgt, "relation_type": canon})
    return result


def parse_bundle(
    concept_rows: Iterable[dict] | None = None,
    relation_rows: Iterable[dict] | None = None,
    known_ids: Iterable[str] = (),
) -> ImportResult:
    result = ImportResult()
    try:
        if concept_rows:
            parse_concepts(concept_rows, result)
        if relation_rows:
            parse_relations(relation_rows, known_ids, result)
    except ImportFileError as e:
        result.errors.append(str(e))
    return result


def tables_to_rows(
    concepts_tables: dict | None, relations_tables: dict | None
) -> tuple[list[dict], list[dict]]:
    """Pick concept/relation rows out of what read_tables returned for one or two files."""
    concept_rows: list[dict] = []
    relation_rows: list[dict] = []
    if concepts_tables:
        if "concepts" in concepts_tables or "relations" in concepts_tables:
            concept_rows = concepts_tables.get("concepts") or []
            relation_rows = concepts_tables.get("relations") or []
        else:
            concept_rows = concepts_tables.get("rows") or []
    if relations_tables:
        relation_rows = (relations_tables.get("relations")
                         or relations_tables.get("rows") or [])
    return concept_rows, relation_rows


def load_files(
    concepts_path: str | Path | None = None,
    relations_path: str | Path | None = None,
    known_ids: Iterable[str] = (),
) -> ImportResult:
    """Read and validate one bundle file (JSON / two-sheet XLSX) or a concepts + relations pair."""
    try:
        ct = read_file(concepts_path) if concepts_path else None
        rt = read_file(relations_path) if relations_path else None
    except ImportFileError as e:
        return ImportResult(errors=[str(e)])
    c_rows, r_rows = tables_to_rows(ct, rt)
    if not c_rows and not r_rows:
        return ImportResult(errors=["no concept or relation rows found"])
    return parse_bundle(c_rows, r_rows, known_ids)


# ---------------------------------------------------------------------------
# Export (round-trips with the importer)
# ---------------------------------------------------------------------------

def concepts_to_csv(concepts: Iterable[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CONCEPT_COLUMNS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for c in concepts:
        row = dict(c)
        row["authors"] = f"{LIST_SEP} ".join(c.get("authors") or [])
        row["cross_domain_influence"] = f"{LIST_SEP} ".join(c.get("cross_domain_influence") or [])
        row["proven"] = "true" if c.get("proven") else "false"
        w.writerow(row)
    return buf.getvalue()


def relations_to_csv(relations: Iterable[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=RELATION_COLUMNS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in relations:
        w.writerow(r)
    return buf.getvalue()

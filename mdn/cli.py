"""Command-line tools for loading data into the Mathematical Discovery Navigator.

    python -m mdn.cli import --concepts data/templates/concepts_template.csv \\
                             --relations data/templates/relations_template.csv
    python -m mdn.cli import --concepts my_corpus.xlsx --replace   # sheets: concepts, relations
    python -m mdn.cli import --concepts bundle.json --dry-run      # validate only
    python -m mdn.cli demo  [--replace]       # load the built-in 80-concept demo corpus
    python -m mdn.cli arxiv "persistent homology" --max 20         # live arXiv search -> concepts
    python -m mdn.cli analyze                 # re-run all scoring
    python -m mdn.cli export --out-dir exported/
    python -m mdn.cli stats
    python -m mdn.cli clear --yes

The database defaults to $MDN_DB or ./mdn.db (the file run.py serves).
Imports are all-or-nothing: if any row is invalid nothing is written and every
problem is listed, unless --skip-invalid is given.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.importer import (  # noqa: E402
    ImportResult, concepts_to_csv, load_files, parse_concepts, relations_to_csv,
)
from mdn.model import Model  # noqa: E402

DEFAULT_DB = os.environ.get("MDN_DB", "mdn.db")


def _print_result(res: ImportResult, limit: int = 40) -> None:
    for w in res.warnings[:limit]:
        print(f"warning: {w}", file=sys.stderr)
    if len(res.warnings) > limit:
        print(f"warning: ... and {len(res.warnings) - limit} more", file=sys.stderr)
    for e in res.errors[:limit]:
        print(f"error: {e}", file=sys.stderr)
    if len(res.errors) > limit:
        print(f"error: ... and {len(res.errors) - limit} more", file=sys.stderr)


def _store(m: Model, res: ImportResult, args) -> int:
    _print_result(res)
    print(f"Validated {len(res.concepts)} concept(s), {len(res.relations)} relation(s); "
          f"{len(res.errors)} error(s), {len(res.warnings)} warning(s).")
    if res.errors and not args.skip_invalid:
        print("Nothing imported. Fix the rows above or rerun with --skip-invalid.", file=sys.stderr)
        return 2
    if not res.concepts and not res.relations:
        print("Nothing to import.", file=sys.stderr)
        return 2
    if args.dry_run:
        print("Dry run: database unchanged.")
        return 0
    out = m.import_data(res.concepts, res.relations, replace=args.replace,
                        analyze=not args.no_analyze)
    print(f"Imported into {m.db_path}: {json.dumps(out)}")
    return 0


def cmd_import(args) -> int:
    if not args.concepts and not args.relations:
        print("error: give --concepts and/or --relations", file=sys.stderr)
        return 2
    m = Model(args.db)
    known = [] if args.replace else [c["concept_id"] for c in m.list_concepts()]
    return _store(m, load_files(args.concepts, args.relations, known_ids=known), args)


def cmd_demo(args) -> int:
    from data.mock_corpus import get_concepts, get_relations
    m = Model(args.db)
    if m.list_concepts() and not args.replace:
        print("Database already has data; demo concepts were merged in (use --replace to start clean).")
    out = m.import_data(get_concepts(), get_relations(), replace=args.replace)
    print(f"Loaded demo corpus into {m.db_path}: {json.dumps(out)}")
    return 0


def cmd_arxiv(args) -> int:
    from data.connectors import ArxivConnector, ConnectorError
    try:
        raw = ArxivConnector().fetch_concepts(args.query, max_results=args.max,
                                              concept_type=args.type)
    except ConnectorError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    print(f"arXiv returned {len(raw)} paper(s) for {args.query!r}.")
    res = parse_concepts(raw)
    if args.save_csv:
        Path(args.save_csv).write_text(concepts_to_csv(res.concepts), encoding="utf-8")
        print(f"Saved concepts to {args.save_csv} (edit, add relations, then `import`).")
    return _store(Model(args.db), res, args)


def cmd_analyze(args) -> int:
    m = Model(args.db)
    m.clear_analysis()
    print(json.dumps(m.run_full_analysis()))
    return 0


def cmd_export(args) -> int:
    m = Model(args.db)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "concepts.csv").write_text(concepts_to_csv(m.list_concepts()), encoding="utf-8")
    (out / "relations.csv").write_text(relations_to_csv(m.list_relations()), encoding="utf-8")
    print(f"Wrote {out / 'concepts.csv'} and {out / 'relations.csv'}")
    return 0


def cmd_stats(args) -> int:
    s = Model(args.db).dashboard_stats()
    s.pop("top_fruitfulness", None)
    print(json.dumps(s, indent=2))
    return 0


def cmd_clear(args) -> int:
    if not args.yes:
        print("error: this deletes every concept, relation and score in "
              f"{args.db}; rerun with --yes to confirm", file=sys.stderr)
        return 2
    Model(args.db).clear_all()
    print(f"Cleared {args.db}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m mdn.cli", description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", default=DEFAULT_DB, help=f"SQLite file (default {DEFAULT_DB})")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def store_flags(p):
        p.add_argument("--replace", action="store_true", help="delete existing data first")
        p.add_argument("--skip-invalid", action="store_true", help="import the valid rows even if some fail")
        p.add_argument("--dry-run", action="store_true", help="validate only; write nothing")
        p.add_argument("--no-analyze", action="store_true", help="skip re-running the analysis")

    p = sub.add_parser("import", help="import concepts/relations from CSV, TSV, XLSX or JSON")
    p.add_argument("--concepts", help="concepts file, or one JSON/XLSX holding both tables")
    p.add_argument("--relations", help="relations file")
    store_flags(p)
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("demo", help="load the built-in demo corpus")
    p.add_argument("--replace", action="store_true")
    p.set_defaults(func=cmd_demo)

    p = sub.add_parser("arxiv", help="search arXiv and import the papers as concepts")
    p.add_argument("query")
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--type", default="theorem", help="concept_type for the imported papers")
    p.add_argument("--save-csv", help="also write the fetched concepts to this CSV")
    store_flags(p)
    p.set_defaults(func=cmd_arxiv)

    sub.add_parser("analyze", help="re-run all scoring").set_defaults(func=cmd_analyze)
    p = sub.add_parser("export", help="write concepts.csv and relations.csv")
    p.add_argument("--out-dir", default="exported")
    p.set_defaults(func=cmd_export)
    sub.add_parser("stats", help="print dashboard counts").set_defaults(func=cmd_stats)
    p = sub.add_parser("clear", help="delete all data")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_clear)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

"""Start the Mathematical Discovery Navigator web app.

    python run.py                    # serves ./mdn.db on http://127.0.0.1:5075, demo corpus if empty
    python run.py --no-demo          # start empty; import your data at /import
    python run.py --db my.db --port 8080
"""
import argparse
import os

from mdn.app import create_app

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Mathematical Discovery Navigator")
    ap.add_argument("--db", default=os.environ.get("MDN_DB", "mdn.db"), help="SQLite file (default mdn.db)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5075)
    ap.add_argument("--no-demo", action="store_true",
                    help="do not load the demo corpus into an empty database")
    args = ap.parse_args()
    create_app(args.db, seed_demo=False if args.no_demo else None).run(
        host=args.host, port=args.port, debug=False)

"""External data connectors.

The local default is file import (data/importer.py). This module adds a live
arXiv connector that turns search results into concept rows in the same
schema, so they go through the same validation before reaching the database.

arXiv's public API needs no account or key. Settings (all optional):
  MDN_ARXIV_URL         API endpoint (default https://export.arxiv.org/api/query)
  MDN_HTTP_TIMEOUT      seconds per request (default 20)
  MDN_CONTACT_EMAIL     added to the User-Agent, as arXiv asks of API clients

arXiv has no citation counts or citation graph, so imported papers get
citation_count 0, importance_score 0.5 and no relations; add relations with
a relations file afterwards. Network failures raise ConnectorError with a
plain message instead of a traceback.
"""
from __future__ import annotations

import os
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Callable

_ATOM = "{http://www.w3.org/2005/Atom}"
_ARXIV = "{http://arxiv.org/schemas/atom}"

# arXiv category -> ontology domain (data/ontology.py)
ARXIV_CATEGORY_DOMAINS = {
    "math.AG": "Algebraic Geometry",
    "math.NT": "Number Theory",
    "math.AT": "Topology", "math.GT": "Topology", "math.GN": "Topology",
    "math.CT": "Category Theory",
    "math.DG": "Differential Geometry", "math.SG": "Differential Geometry",
    "math.FA": "Functional Analysis", "math.OA": "Functional Analysis",
    "math.RT": "Representation Theory",
    "math.LO": "Logic",
    "math.PR": "Probability", "math.ST": "Probability",
    "math.DS": "Dynamical Systems",
    "math.AP": "PDEs",
    "math.MP": "Mathematical Physics", "math-ph": "Mathematical Physics",
    "quant-ph": "Quantum Information",
    "math.OC": "Optimization",
    "math.CO": "Combinatorics",
    "math.RA": "Algebra", "math.GR": "Algebra", "math.AC": "Algebra", "math.QA": "Algebra",
}


class ConnectorError(RuntimeError):
    """A connector could not fetch or parse data; the message says why."""


def _clean(s: str | None) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


class ArxivConnector:
    """Search arXiv and return concept dicts ready for data.importer.parse_concepts."""

    def __init__(self, fetch: Callable[[str], str] | None = None,
                 base_url: str | None = None, timeout: float | None = None) -> None:
        self.base_url = base_url or os.environ.get("MDN_ARXIV_URL", "https://export.arxiv.org/api/query")
        self.timeout = timeout or float(os.environ.get("MDN_HTTP_TIMEOUT", "20"))
        self._fetch = fetch or self._http_get

    def _http_get(self, url: str) -> str:
        contact = os.environ.get("MDN_CONTACT_EMAIL", "")
        ua = "MathematicalDiscoveryNavigator/1.0" + (f" (mailto:{contact})" if contact else "")
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise ConnectorError(f"arXiv returned HTTP {e.code}; try again later or narrow the query") from None
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            reason = getattr(e, "reason", e)
            raise ConnectorError(f"could not reach arXiv ({reason}); check your network connection") from None

    def build_url(self, query: str, max_results: int = 25, start: int = 0) -> str:
        query = (query or "").strip()
        if not query:
            raise ConnectorError("query is empty")
        if not 1 <= max_results <= 200:
            raise ConnectorError("max_results must be between 1 and 200")
        # Plain words search everything; text containing ':' is passed through
        # as arXiv query syntax, e.g. 'cat:math.AG AND all:schemes'.
        search = query if ":" in query else f'all:"{query}"'
        params = {"search_query": search, "start": start, "max_results": max_results,
                  "sortBy": "relevance", "sortOrder": "descending"}
        return f"{self.base_url}?{urllib.parse.urlencode(params)}"

    def parse_feed(self, xml_text: str, concept_type: str = "theorem") -> list[dict]:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            raise ConnectorError(f"arXiv response was not valid XML: {e}") from None
        concepts = []
        for entry in root.findall(f"{_ATOM}entry"):
            raw_id = _clean(entry.findtext(f"{_ATOM}id"))
            if not raw_id or "/abs/" not in raw_id:
                continue                      # arXiv reports query errors as an entry without /abs/
            arxiv_id = re.sub(r"v\d+$", "", raw_id.rsplit("/abs/", 1)[1])
            primary_el = entry.find(f"{_ARXIV}primary_category")
            primary = primary_el.get("term") if primary_el is not None else ""
            cats = [c.get("term") for c in entry.findall(f"{_ATOM}category") if c.get("term")]
            domain = ARXIV_CATEGORY_DOMAINS.get(primary) or next(
                (ARXIV_CATEGORY_DOMAINS[c] for c in cats if c in ARXIV_CATEGORY_DOMAINS), primary or "Unknown")
            cross = sorted({ARXIV_CATEGORY_DOMAINS[c] for c in cats
                            if c in ARXIV_CATEGORY_DOMAINS and ARXIV_CATEGORY_DOMAINS[c] != domain})
            published = _clean(entry.findtext(f"{_ATOM}published"))
            concepts.append({
                "concept_id": f"arXiv:{arxiv_id}",
                "name": _clean(entry.findtext(f"{_ATOM}title")),
                "domain": domain,
                "concept_type": concept_type,
                "year_introduced": published[:4],
                "abstract": _clean(entry.findtext(f"{_ATOM}summary")),
                "authors": [_clean(a.findtext(f"{_ATOM}name")) for a in entry.findall(f"{_ATOM}author")],
                "citation_count": 0,
                "importance_score": 0.5,
                "proven": concept_type != "conjecture",
                "downstream_theorems": 0,
                "cross_domain_influence": cross,
            })
        return concepts

    def fetch_concepts(self, query: str, max_results: int = 25,
                       concept_type: str = "theorem", start: int = 0) -> list[dict]:
        return self.parse_feed(self._fetch(self.build_url(query, max_results, start)), concept_type)

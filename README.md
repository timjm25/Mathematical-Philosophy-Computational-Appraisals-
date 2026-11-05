# Mathematical Discovery Navigator (MDN)

> **AI-powered mathematical intuition** — identifying tomorrow's discoveries before they happen.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.1-orange)](https://networkx.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-red)](https://scikit-learn.org)
[![Tests](https://img.shields.io/badge/Tests-163%20passing-brightgreen)]()

---

## The Crisis in Mathematical Discovery

Mathematics is expanding faster than humans can navigate it.

In 1900, a brilliant mathematician could reasonably survey most active research across all fields. By 1950 that was no longer true. Today, the arXiv alone receives over 15,000 mathematics preprints per year. MathSciNet indexes more than 3.5 million reviews. The zbMATH database covers over 4 million documents. The Lean theorem prover library Mathlib contains over 150,000 formal definitions.

**The fundamental problem is not capability — it is direction.**

Most mathematical researchers spend the majority of their careers in narrow specialties, often unaware of structurally identical results being proved in adjacent fields, cross-domain connections that could unlock breakthroughs, or the fact that the specific research direction they are pursuing has low expected yield relative to its difficulty.

The consequences are significant:

- **Duplication of effort**: Results are rediscovered independently across domains, years apart.
- **Missed connections**: The bridge between two powerful theories goes unbuilt for decades because no one is actively looking for it.
- **Misallocated talent**: Mathematicians of extraordinary ability spend years on tractable-but-unrewarding problems when transformative open questions sit nearby.
- **Slow transfer**: Proof techniques developed in one domain take a generation to propagate to adjacent fields where they are equally powerful.

---

## The Core Research Question

> Can machine learning discover hidden patterns in the historical evolution of mathematics that allow it to estimate the future "fruitfulness" of mathematical ideas before formal proofs exist?

Rather than answering: *"Is this theorem true?"*

The system answers: *"If this conjecture is true, will it open an entirely new branch of mathematics?"*

The objective is **not automated theorem proving**.

The objective is **automated mathematical intuition**.

The system functions as an AI research collaborator that recommends where mathematicians should direct their effort — functioning as a research telescope that reveals promising regions of mathematical space before humans recognize their significance.

---

## Scientific Foundation

MDN combines 13 AI and mathematical techniques:

| Technique | Role in MDN |
|-----------|-------------|
| **Graph Neural Networks** | Propagating information through the mathematical knowledge graph |
| **Transformer Architectures** | Encoding mathematical text (abstracts, theorems) into embeddings |
| **Geometric Deep Learning** | Understanding structural invariants of mathematical objects |
| **Knowledge Graphs** | Representing the web of mathematical dependencies |
| **Bayesian Learning** | Computing confidence intervals on fruitfulness predictions |
| **Active Learning** | Prioritizing which regions of math need most exploration |
| **Reinforcement Learning** | Learning reward functions from historical citation growth |
| **Topological Data Analysis** | Finding shape structure in the mathematical embedding space |
| **Representation Learning** | Building latent embeddings of mathematical concepts |
| **Scientific Foundation Models** | Pre-training on formal mathematics corpora |
| **Explainable AI** | Ensuring every prediction has a human-readable rationale |
| **Symbolic AI** | Incorporating formal logical structure from theorem provers |
| **Neural-Symbolic Computing** | Bridging numerical embeddings with symbolic reasoning |

---

## Mathematical Domains

MDN covers all major mathematical fields with extensible ontology support:

```
Algebra                  Category Theory         Number Theory
Algebraic Geometry       Differential Geometry   Functional Analysis
Topology                 Representation Theory   Logic
Probability              Dynamical Systems        PDEs
Mathematical Physics     Quantum Information     Optimization
Combinatorics
```

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                     Mathematical Discovery Navigator                    │
├─────────────────────────────────────────────────────────────────────────┤
│  DATA LAYER                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────────────┐ │
│  │ File import  │  │   Ontology   │  │  arXiv connector (extensible)  │ │
│  │ CSV/XLSX/JSON│  │  16 domains  │  │  + optional demo corpus        │ │
│  │ + validation │  │  15 types    │  │    (80 concepts, 120 rels)     │ │
│  └──────┬───────┘  └──────┬───────┘  └────────────────┬───────────────┘ │
│         └─────────────────┴──────────────────────────┘                  │
│                           │                                              │
│  ENGINE LAYER             ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │  MathKnowledgeGraph  (NetworkX DiGraph)                             │ │
│  │  centrality • bridges • domain clusters • missing connections       │ │
│  └────────────────────────┬────────────────────────────────────────────┘ │
│                           │                                              │
│  ┌────────────────────────▼────────────────────────────────────────────┐ │
│  │  EmbeddingEngine  (TF-IDF + SVD + PCA)                              │ │
│  │  fit • embed • similarity • nearest_neighbors • latent_coordinates  │ │
│  └──────┬──────────────────┬─────────────────────┬─────────────────────┘ │
│         │                  │                     │                        │
│  ┌──────▼───────┐  ┌───────▼──────┐  ┌──────────▼─────────┐             │
│  │ Fruitfulness │  │  Conjecture  │  │  Curiosity Engine  │             │
│  │  Predictor   │  │   Ranker     │  │  holes/bridges/gaps │             │
│  └──────┬───────┘  └───────┬──────┘  └──────────┬─────────┘             │
│         │                  │                     │                        │
│  ┌──────▼──────────────────▼─────────────────────▼─────────────────────┐ │
│  │   Historical Simulator     +     Explainability Layer               │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  PERSISTENCE LAYER                                                       │
│  SQLite (5 tables: concepts, relations, fruitfulness_predictions,        │
│          conjecture_scores, curiosity_insights)                          │
│                                                                          │
│  WEB LAYER                                                               │
│  Flask • 6 browser routes • 10 REST endpoints • Chart.js                │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## The 9 Major AI Modules

### 1. Mathematical Knowledge Graph

Every mathematical concept becomes a node. Every relationship becomes a directed edge.

**Concept types**: theorem, proof, axiom, conjecture, manifold, category, group, ring, operator, graph, tensor, equation, topological space, functor, homology class

**Relation types**: depends_on, generalizes, special_case_of, dual_of, uses, contradicts, motivated_by, equivalent_to, extends, historically_preceded, shares_proof_techniques, appears_in_applications

The graph is built from the mock corpus (~80 concepts, ~120 relations) with connectors available for arXiv, MathSciNet, Semantic Scholar, and formal proof libraries.

**Key analytics**:
- Betweenness centrality — which concepts are mathematical crossroads?
- Bridge detection — which concepts connect otherwise isolated clusters?
- Domain clustering — how does the community naturally organize?
- Missing connection detection — which same-domain concepts have no path between them?

### 2. Research Landscape Embedding

Every concept abstract is encoded using TF-IDF with Truncated SVD dimensionality reduction. The high-dimensional embedding space is projected to 2D using PCA for visualization.

- **Nearest neighbor search** — what concepts are semantically closest to a given query?
- **Latent gap detection** — where in embedding space is mathematical coverage sparse?
- **Concept clustering** — what are the natural semantic clusters?

### 3. Fruitfulness Prediction Engine

The fruitfulness score estimates the expected research yield of a mathematical concept:

```
fruitfulness = (
    0.25 × importance_score
  + 0.20 × citation_score_normalized
  + 0.20 × centrality_boost
  + 0.15 × neighbor_importance
  + 0.10 × cross_domain_score
  + 0.10 × downstream_theorem_score
) + conjecture_bonus (0.15 if open)
```

Predictions include:
- **Expected theorem yield** (0–10 scale)
- **Citation impact score** (0–1)
- **New subfield probability** (0–1)
- **Cross-disciplinary score** (0–1)
- **Proof difficulty estimate** (0–1)
- **Confidence interval** (0–1)
- **Human-readable explanation**
- **Comparable historical concepts**

### 4. Conjecture Ranking System

Every open conjecture is scored on five dimensions:

| Dimension | Description |
|-----------|-------------|
| **Novelty** | Age since introduction — older unsolved problems carry more depth |
| **Importance** | Estimated impact if proved |
| **Connectivity** | Graph centrality — how many results depend on this? |
| **Generalization** | Cross-domain influence — how many fields would benefit? |
| **Depth** | Conceptual depth estimate — how fundamental is the idea? |

For each conjecture, MDN generates a **research roadmap**: a sequential sequence of suggested investigative steps from literature survey to targeted lemma development.

### 5. Mathematical Curiosity Engine

Identifies five classes of high-potential mathematical opportunities:

| Insight Type | What it finds |
|--------------|---------------|
| **hole** | Domain pairs with sparse cross-domain connections |
| **bridge** | High-centrality concepts that could be generalized |
| **isolated** | Highly important concepts with few graph connections |
| **underexplored** | Large semantic gaps between concepts in embedding space |
| **missing_theory** | Same-domain concepts with no known mathematical path between them |

### 6. Historical Replay Simulator

Trains MDN on mathematics up to a historical cutoff year (1900, 1950, 1980, 1995, or 2010) and asks: what would we have predicted?

**Case studies included**:
- Grothendieck's algebraic geometry revolution (1960)
- Morse theory applications (1934–1960)
- Perelman's Ricci flow proof of Poincaré (2003)
- Mirror symmetry (1990)
- Topological data analysis / persistent homology (2002)
- Compressed sensing (2006)

### 7. Latent Mathematics Explorer

The 2D embedding projection allows visual navigation of the mathematical landscape — identifying clusters, gaps, and the semantic distance between arbitrary concepts.

### 8. Interactive Research Copilot

Enter any mathematical query (equation, theorem, conjecture, manifold, research area). Returns:
- Related concepts from the knowledge graph
- Research gaps relevant to the query
- Fruitfulness predictions for related concepts
- Open problems in the vicinity
- Explanation of why these results are relevant

### 9. Explainability Layer

**Every recommendation must include an explanation.**

Example outputs:
- *"This resembles developments preceding Morse Theory."*
- *"Historically similar concepts produced 12 downstream theorems."*
- *"This object bridges two disconnected mathematical communities."*
- *"Estimated impact is driven by its unusually high graph centrality."*

No unexplained neural predictions are returned.

---

## Quick Start

```bash
# Clone
git clone https://github.com/timjm25/Mathematical-Philosophy-Computational-Appraisals-
cd Mathematical-Philosophy-Computational-Appraisals-

# Install dependencies
python3 -m pip install -r requirements.txt

# Run the server (serves ./mdn.db)
python3 run.py                 # loads the 80-concept demo corpus if the database is empty
python3 run.py --no-demo       # or start empty and import your own data
python3 run.py --db my_corpus.db --port 8080

# Open your browser
open http://localhost:5075

# Run the tests
python3 -m pytest -q
```

The demo corpus is optional: it loads automatically into an empty database
unless you pass `--no-demo` or set `MDN_SEED_DEMO=0`, and you can load it
later from the **Import Data** page or with `python3 -m mdn.cli demo`.

---

## Import Your Own Data

Templates with five clearly marked `SAMPLE` rows are in `data/templates/`
(also downloadable from the **Import Data** page):

- `data/templates/concepts_template.csv` — one row per concept
- `data/templates/relations_template.csv` — one row per directed relation

Copy them, replace the sample rows with your own, then either upload them at
`http://localhost:5075/import` or use the CLI:

```bash
python3 -m mdn.cli import --concepts my_concepts.csv --relations my_relations.csv --replace
python3 -m mdn.cli import --concepts my_corpus.xlsx      # one workbook, sheets "concepts" + "relations"
python3 -m mdn.cli import --concepts bundle.json --dry-run   # validate only
python3 -m mdn.cli export --out-dir exported/            # current data back out as CSV
python3 -m mdn.cli stats | analyze | demo | clear --yes
```

All commands take `--db PATH` (default `$MDN_DB` or `mdn.db`, the file
`run.py` serves). Accepted files: `.csv`, `.tsv`, `.xlsx`, `.json`
(`{"concepts": [...], "relations": [...]}` or a bare list of rows).

| Concept column | Required | Format |
|----------------|----------|--------|
| `concept_id` | yes | unique text id |
| `name` | yes | text |
| `domain` | yes | e.g. `Number Theory` (values in `data/ontology.py`; others accepted with a warning) |
| `concept_type` | yes | `theorem`, `conjecture`, `axiom`, … (only `conjecture` rows are ranked as conjectures) |
| `year_introduced` | yes | whole number (negative = BCE) |
| `abstract` | no | text; drives the embeddings and the copilot |
| `authors` | no | names separated by `;` |
| `citation_count`, `downstream_theorems` | no | whole numbers ≥ 0 (default 0) |
| `importance_score` | no | 0–1 (default 0.5) |
| `proven` | no | `true`/`false`, `yes`/`no`, `1`/`0` (default false) |
| `cross_domain_influence` | no | domains separated by `;` |

| Relation column | Required | Format |
|-----------------|----------|--------|
| `source_id`, `target_id` | yes | `concept_id`s from the same import or already in the database |
| `relation_type` | yes | `depends_on`, `generalizes`, `uses`, `motivated_by`, … (see `data/ontology.py`; others accepted with a warning) |

Headers match case-insensitively and extra columns are ignored. Every row is
validated before anything is written: wrong numbers, empty required fields,
duplicate ids, relations to unknown concepts and self-loops are listed by row
number, and **nothing is imported** until they are fixed (or you tick
"import the valid rows" / pass `--skip-invalid`). By default an import is
merged into the existing data (same `concept_id` overwrites); "Replace all
existing data" / `--replace` starts clean, which you will want the first time
if the demo corpus was loaded. The analysis re-runs after every import.

### Live arXiv search

```bash
python3 -m mdn.cli arxiv "persistent homology" --max 25 --save-csv arxiv_concepts.csv
python3 -m mdn.cli arxiv "cat:math.AG AND all:schemes" --type theorem --dry-run
```

`data/connectors.py` calls arXiv's public API (no account or key), maps each
paper's arXiv category to an ontology domain (`math.AG` → Algebraic
Geometry, `math.NT` → Number Theory, …) and sends the rows through the same
validation as a file import. Optional settings: `MDN_ARXIV_URL`,
`MDN_HTTP_TIMEOUT`, `MDN_CONTACT_EMAIL` (added to the User-Agent). arXiv has
no citation data, so papers arrive with `citation_count` 0, `importance_score`
0.5 and no relations — edit the saved CSV and add a relations file for
better scores. Network failures print a one-line error and change nothing.

### Still out of scope

- Citation-graph connectors (Semantic Scholar, OpenAlex, MathSciNet, Mathlib)
  that would create relations automatically.
- The copilot and embeddings are TF-IDF based; no LLM or math language model is called.
- The web app has no user accounts; run it locally (it binds to 127.0.0.1).

---

## Web Interface

| Route | Description |
|-------|-------------|
| `/` | Dashboard — fruitfulness chart, conjecture leaderboard, top insights |
| `/graph` | Knowledge graph explorer with domain filter and centrality analysis |
| `/conjecture` | Open conjecture rankings with research roadmaps |
| `/explore` | Latent space explorer — curiosity insights and embedding visualization |
| `/history` | Historical replay simulator |
| `/copilot` | Research copilot — natural language query interface |
| `/import` | Upload CSV/XLSX/JSON, download templates, export CSV, load the demo corpus |

With an empty database the analysis pages redirect to `/import`.

---

## REST API Reference

### Concepts

```bash
# List all concepts
curl http://localhost:5075/api/v1/concepts

# Filter by domain
curl http://localhost:5075/api/v1/concepts?domain=Number+Theory

# Filter by type
curl http://localhost:5075/api/v1/concepts?type=conjecture

# Get single concept
curl http://localhost:5075/api/v1/concept/C001
```

### Relations

```bash
# List all relations
curl http://localhost:5075/api/v1/relations

# Filter by source
curl http://localhost:5075/api/v1/relations?source_id=C001
```

### Fruitfulness Predictions

```bash
# All predictions (ranked by fruitfulness)
curl http://localhost:5075/api/v1/fruitfulness

# Filter by domain
curl http://localhost:5075/api/v1/fruitfulness?domain=Topology
```

### Conjecture Rankings

```bash
curl http://localhost:5075/api/v1/conjectures
```

### Curiosity Insights

```bash
curl http://localhost:5075/api/v1/insights
```

### Dashboard Statistics

```bash
curl http://localhost:5075/api/v1/stats
```

### Historical Simulation

```bash
# Simulate with 1980 cutoff
curl http://localhost:5075/api/v1/history/1980

# Supported cutoffs: 1900, 1950, 1980, 1995, 2010
curl http://localhost:5075/api/v1/history/1950
```

### Research Copilot

```bash
curl -X POST http://localhost:5075/api/v1/copilot \
  -H "Content-Type: application/json" \
  -d '{"query": "elliptic curves and modular forms"}'
```

Response:
```json
{
  "related_concepts": [...],
  "research_gaps": [...],
  "predictions": [...],
  "open_problems": [...],
  "explanation": "Query matched most closely with: Elliptic Curves, Modular Forms, ..."
}
```

### Trigger Analysis

```bash
curl -X POST http://localhost:5075/api/v1/run_analysis
```

### Import Data

```bash
# Upload files (same fields as the /import page); replace / skip_invalid are optional
curl -X POST http://localhost:5075/api/v1/import \
  -F concepts_file=@data/templates/concepts_template.csv \
  -F relations_file=@data/templates/relations_template.csv -F replace=1

# Or send rows as JSON
curl -X POST http://localhost:5075/api/v1/import -H "Content-Type: application/json" \
  -d '{"concepts": [{"concept_id": "N1", "name": "New result", "domain": "Topology",
                     "concept_type": "theorem", "year_introduced": 2024}]}'

# Load the demo corpus
curl -X POST http://localhost:5075/api/v1/demo -H "Content-Type: application/json" -d '{"replace": true}'
```

Returns `200` with counts, or `400` with `errors` (one line per bad row) and nothing written.
CSV exports: `GET /export/concepts.csv`, `GET /export/relations.csv`.

---

## Knowledge Graph Schema

### Concept Object

```json
{
  "concept_id": "C001",
  "name": "Riemann Hypothesis",
  "domain": "Number Theory",
  "concept_type": "conjecture",
  "year_introduced": 1859,
  "abstract": "All non-trivial zeros of the Riemann zeta function have real part equal to one-half...",
  "authors": ["Bernhard Riemann"],
  "citation_count": 15000,
  "importance_score": 1.0,
  "proven": false,
  "downstream_theorems": 0,
  "cross_domain_influence": ["Functional Analysis", "Algebra", "Mathematical Physics"]
}
```

### Fruitfulness Prediction Object

```json
{
  "concept_id": "C001",
  "domain": "Number Theory",
  "expected_theorem_yield": 8.7,
  "citation_impact_score": 0.75,
  "new_subfield_probability": 0.62,
  "cross_disciplinary_score": 0.75,
  "proof_difficulty_estimate": 0.91,
  "overall_fruitfulness": 0.87,
  "confidence": 0.73,
  "explanation": "Fruitfulness driven by: high graph centrality; cross-domain influence on 3 fields; open conjecture carries exploratory potential",
  "comparable_historical": ["Prime Number Theorem", "Fourier Analysis"]
}
```

---

## Extending MDN

### Adding New Domains

Edit `data/ontology.py`:

```python
DOMAINS = [
    ...,
    "Tropical Geometry",
    "Homotopy Theory",
    "Arithmetic Statistics",
]
```

### Adding Real Data Connectors

`data/connectors.py` holds a working `ArxivConnector`. A new connector only
has to return concept dicts in the import schema; pass them through the
importer so they are validated like a file:

```python
from data.connectors import ArxivConnector
from data.importer import parse_concepts
from mdn.model import Model

res = parse_concepts(ArxivConnector().fetch_concepts("algebraic geometry", max_results=100))
if res.ok:
    Model("mdn.db").import_data(res.concepts, res.relations)
```

### Real-World Data Sources

| Source | Status | What to extract |
|--------|--------|-----------------|
| arXiv | **built in** (`python3 -m mdn.cli arxiv ...`) | Recent papers, authors, abstracts, categories |
| CSV / Excel / JSON files | **built in** (`/import`, `python3 -m mdn.cli import`) | Anything you curate |
| Semantic Scholar | not yet | Citations, fields of study |
| OpenAlex | not yet | Concept hierarchy, citation graph |
| MathSciNet | not yet (subscription) | Formal classifications, reviews |
| Lean Mathlib | not yet | Formal theorems, dependencies |

---

## Project Structure

```
MathDiscoveryNavigator/
├── run.py                          # Entry point — port 5075
├── requirements.txt
├── README.md
│
├── data/
│   ├── ontology.py                 # Domain / concept / relation type definitions
│   ├── mock_corpus.py              # Optional demo corpus: 80 concepts, 120 relations
│   ├── importer.py                 # CSV/TSV/XLSX/JSON import + validation, CSV export
│   ├── connectors.py               # Live arXiv connector
│   └── templates/                  # concepts_template.csv, relations_template.csv
│
├── engine/
│   ├── knowledge_graph.py          # NetworkX DiGraph with analytics
│   ├── embedding_engine.py         # TF-IDF + SVD + PCA embeddings
│   ├── fruitfulness_predictor.py   # Composite fruitfulness scoring
│   ├── conjecture_ranker.py        # Open conjecture ranking + roadmaps
│   ├── curiosity_engine.py         # Gap/bridge/hole detection
│   ├── historical_simulator.py     # Historical replay simulation
│   └── explainability.py           # Human-readable explanation generation
│
├── mdn/
│   ├── model.py                    # SQLite persistence (5 tables)
│   ├── seed.py                     # Demo-corpus seeding
│   ├── cli.py                      # python3 -m mdn.cli import | demo | arxiv | export | ...
│   ├── app.py                      # Flask factory (browser routes + REST endpoints)
│   └── templates/                  # Dark-theme HTML templates with Chart.js
│       ├── base.html
│       ├── dashboard.html
│       ├── graph.html
│       ├── conjecture.html
│       ├── explore.html
│       ├── history.html
│       ├── copilot.html
│       └── import.html
│
└── tests/                          # 163 tests, 0 failures
    ├── test_knowledge_graph.py
    ├── test_embedding_engine.py
    ├── test_fruitfulness_predictor.py
    ├── test_conjecture_ranker.py
    ├── test_curiosity_engine.py
    ├── test_historical_simulator.py
    ├── test_model.py
    ├── test_importer.py
    └── test_import_app_cli.py
```

---

## The Mathematical Corpus

The mock corpus covers 80 historically significant concepts spanning 16 domains:

### Famous Open Problems (Millennium Prize and Beyond)

| Concept | Domain | Year | Status |
|---------|--------|------|--------|
| Riemann Hypothesis | Number Theory | 1859 | Open |
| P vs NP Problem | Logic | 1971 | Open |
| Birch-Swinnerton-Dyer Conjecture | Number Theory | 1965 | Open |
| Hodge Conjecture | Algebraic Geometry | 1950 | Open |
| Navier-Stokes Existence | PDEs | 1845 | Open |
| Yang-Mills Existence | Mathematical Physics | 1954 | Open |
| Goldbach Conjecture | Number Theory | 1742 | Open |
| Collatz Conjecture | Number Theory | 1937 | Open |
| Langlands Program | Number Theory | 1967 | Partial |

### Landmark Proved Theorems

| Concept | Domain | Year | Importance |
|---------|--------|------|------------|
| Gödel's Incompleteness Theorems | Logic | 1931 | 1.00 |
| Fermat's Last Theorem | Number Theory | 1637 | 0.97 |
| Poincaré Conjecture | Topology | 1904 | 0.98 |
| Atiyah-Singer Index Theorem | Topology | 1963 | 0.99 |
| Grothendieck's Schemes | Algebraic Geometry | 1960 | 0.99 |
| Fourier Analysis | Functional Analysis | 1822 | 0.98 |
| Spectral Theorem | Functional Analysis | 1929 | 0.97 |
| Galois Theory | Algebra | 1832 | 0.96 |

---

## Research Philosophy

MDN embodies a specific philosophical position about the nature of mathematical discovery.

**Discovery vs. Justification**: Philosophy of science distinguishes between the *context of discovery* (how an idea is found) and the *context of justification* (how it is verified). Automated theorem provers address justification. MDN addresses discovery.

**Structural intuition**: Great mathematicians describe their work as guided by aesthetic and structural intuition — a sense that a certain approach "feels right" before any formal argument exists. MDN attempts to model this intuition as a predictive function over the mathematical knowledge graph.

**The unreasonable effectiveness of cross-domain thinking**: Many of the most transformative mathematical results (Fermat's Last Theorem, the Atiyah-Singer Index Theorem, Mirror Symmetry) are fundamentally cross-domain: they derive their power from unexpected connections between fields. MDN's curiosity engine is specifically designed to identify these latent connections before they are formalized.

**Historical validation**: The historical simulator module tests the specific empirical claim: if MDN had existed in 1980, would it have recommended pursuing Ricci flow? Would it have flagged the potential of persistent homology? The ability to back-test against history distinguishes MDN from systems that merely rank current knowledge by apparent importance.

---

## License

MIT License

Copyright (c) 2026 timjm25

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Contributing

Contributions welcome. Areas of highest priority:

1. **More data connectors** — Semantic Scholar, OpenAlex (citation graph → relations), Lean Mathlib (arXiv and file import are built in)
2. **Better embeddings** — replace TF-IDF with mathematical language models (Llemma, MathBERT)
3. **Richer ontology** — formalize concept types to align with standard mathematical ontologies
4. **Validation studies** — systematic back-testing against historical mathematical development
5. **UI improvements** — interactive knowledge graph visualization with Cytoscape.js or D3.js

---

*Mathematical Discovery Navigator — the world's first AI system designed not to prove mathematics, but to model the dynamics of mathematical discovery itself.*

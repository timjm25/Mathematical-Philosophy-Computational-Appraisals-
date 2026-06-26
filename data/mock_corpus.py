"""Rich mock mathematical corpus with ~80 concepts and ~120 relations."""
from __future__ import annotations
import random

random.seed(42)


def get_concepts() -> list[dict]:
    return [
        # Number Theory
        {
            "concept_id": "C001",
            "name": "Riemann Hypothesis",
            "domain": "Number Theory",
            "concept_type": "conjecture",
            "year_introduced": 1859,
            "abstract": (
                "All non-trivial zeros of the Riemann zeta function have real part equal to one-half. "
                "This conjecture connects the distribution of prime numbers to complex analysis and "
                "has profound implications for analytic number theory."
            ),
            "authors": ["Bernhard Riemann"],
            "citation_count": 15000,
            "importance_score": 1.0,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Functional Analysis", "Algebra", "Mathematical Physics"],
        },
        {
            "concept_id": "C002",
            "name": "Fermat's Last Theorem",
            "domain": "Number Theory",
            "concept_type": "theorem",
            "year_introduced": 1637,
            "abstract": (
                "No three positive integers a, b, c satisfy a^n + b^n = c^n for n > 2. "
                "Proved by Andrew Wiles in 1995 using modular forms and elliptic curves, "
                "connecting number theory, algebraic geometry, and representation theory."
            ),
            "authors": ["Pierre de Fermat", "Andrew Wiles"],
            "citation_count": 12000,
            "importance_score": 0.97,
            "proven": True,
            "downstream_theorems": 85,
            "cross_domain_influence": ["Algebraic Geometry", "Representation Theory", "Algebra"],
        },
        {
            "concept_id": "C003",
            "name": "Goldbach Conjecture",
            "domain": "Number Theory",
            "concept_type": "conjecture",
            "year_introduced": 1742,
            "abstract": (
                "Every even integer greater than 2 can be expressed as the sum of two primes. "
                "One of the oldest unsolved problems in number theory with verified computational "
                "evidence up to 4×10^18."
            ),
            "authors": ["Christian Goldbach"],
            "citation_count": 8000,
            "importance_score": 0.88,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Combinatorics", "Logic"],
        },
        {
            "concept_id": "C004",
            "name": "Prime Number Theorem",
            "domain": "Number Theory",
            "concept_type": "theorem",
            "year_introduced": 1896,
            "abstract": (
                "The number of primes up to x is asymptotically x/ln(x). Proved independently "
                "by Hadamard and de la Vallée Poussin, establishing a deep connection between "
                "primes and complex analysis."
            ),
            "authors": ["Jacques Hadamard", "Charles de la Vallée Poussin"],
            "citation_count": 9500,
            "importance_score": 0.95,
            "proven": True,
            "downstream_theorems": 120,
            "cross_domain_influence": ["Functional Analysis", "Algebra"],
        },
        {
            "concept_id": "C005",
            "name": "Birch-Swinnerton-Dyer Conjecture",
            "domain": "Number Theory",
            "concept_type": "conjecture",
            "year_introduced": 1965,
            "abstract": (
                "The rank of an elliptic curve over the rationals equals the order of vanishing "
                "of its L-function at s=1. A Millennium Prize Problem connecting arithmetic, "
                "analysis, and geometry."
            ),
            "authors": ["Bryan Birch", "Peter Swinnerton-Dyer"],
            "citation_count": 7500,
            "importance_score": 0.94,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Algebraic Geometry", "Functional Analysis"],
        },
        {
            "concept_id": "C006",
            "name": "P vs NP Problem",
            "domain": "Logic",
            "concept_type": "conjecture",
            "year_introduced": 1971,
            "abstract": (
                "Is every problem whose solution can be quickly verified also quickly solvable? "
                "The most famous open question in theoretical computer science with far-reaching "
                "consequences for cryptography, optimization, and artificial intelligence."
            ),
            "authors": ["Stephen Cook", "Leonid Levin"],
            "citation_count": 20000,
            "importance_score": 1.0,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Combinatorics", "Optimization", "Algebra"],
        },
        {
            "concept_id": "C007",
            "name": "Collatz Conjecture",
            "domain": "Number Theory",
            "concept_type": "conjecture",
            "year_introduced": 1937,
            "abstract": (
                "Starting from any positive integer, repeatedly apply: if even divide by 2, "
                "if odd multiply by 3 and add 1. The sequence always reaches 1. Simple to state "
                "but deeply resistant to proof."
            ),
            "authors": ["Lothar Collatz"],
            "citation_count": 4500,
            "importance_score": 0.72,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Dynamical Systems", "Combinatorics"],
        },
        # Topology
        {
            "concept_id": "C008",
            "name": "Poincaré Conjecture",
            "domain": "Topology",
            "concept_type": "theorem",
            "year_introduced": 1904,
            "abstract": (
                "Every simply connected closed 3-manifold is homeomorphic to the 3-sphere. "
                "Proved by Grigori Perelman in 2003 using Ricci flow with surgery, "
                "revolutionizing geometric topology."
            ),
            "authors": ["Henri Poincaré", "Grigori Perelman"],
            "citation_count": 11000,
            "importance_score": 0.98,
            "proven": True,
            "downstream_theorems": 95,
            "cross_domain_influence": ["Differential Geometry", "Mathematical Physics"],
        },
        {
            "concept_id": "C009",
            "name": "Brouwer Fixed Point Theorem",
            "domain": "Topology",
            "concept_type": "theorem",
            "year_introduced": 1910,
            "abstract": (
                "Every continuous function from a convex compact subset of a Euclidean space "
                "to itself has a fixed point. Foundational result connecting topology, analysis, "
                "and applications in economics and game theory."
            ),
            "authors": ["Luitzen Brouwer"],
            "citation_count": 8800,
            "importance_score": 0.92,
            "proven": True,
            "downstream_theorems": 140,
            "cross_domain_influence": ["Functional Analysis", "Optimization", "Probability"],
        },
        {
            "concept_id": "C010",
            "name": "Atiyah-Singer Index Theorem",
            "domain": "Topology",
            "concept_type": "theorem",
            "year_introduced": 1963,
            "abstract": (
                "The analytical index of an elliptic differential operator equals its topological "
                "index. A profound bridge between topology, geometry, and analysis that unified "
                "vast areas of mathematics and theoretical physics."
            ),
            "authors": ["Michael Atiyah", "Isadore Singer"],
            "citation_count": 13000,
            "importance_score": 0.99,
            "proven": True,
            "downstream_theorems": 200,
            "cross_domain_influence": ["Differential Geometry", "Mathematical Physics", "Algebra"],
        },
        {
            "concept_id": "C011",
            "name": "Persistent Homology",
            "domain": "Topology",
            "concept_type": "theorem",
            "year_introduced": 2002,
            "abstract": (
                "A method to compute topological features of data at multiple scales, tracking "
                "when homological features appear and disappear. Foundation of topological data "
                "analysis with broad scientific applications."
            ),
            "authors": ["Herbert Edelsbrunner", "John Harer"],
            "citation_count": 6000,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 75,
            "cross_domain_influence": ["Algebra", "Combinatorics", "Probability"],
        },
        {
            "concept_id": "C012",
            "name": "Hodge Conjecture",
            "domain": "Algebraic Geometry",
            "concept_type": "conjecture",
            "year_introduced": 1950,
            "abstract": (
                "Certain de Rham cohomology classes of a projective algebraic variety are "
                "rational linear combinations of the cohomology classes of algebraic cycles. "
                "A Millennium Prize Problem connecting geometry and algebra."
            ),
            "authors": ["William Hodge"],
            "citation_count": 7000,
            "importance_score": 0.93,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Topology", "Algebra", "Number Theory"],
        },
        # Algebra
        {
            "concept_id": "C013",
            "name": "Classification of Finite Simple Groups",
            "domain": "Algebra",
            "concept_type": "theorem",
            "year_introduced": 1983,
            "abstract": (
                "Every finite simple group belongs to one of four classes: cyclic groups of prime "
                "order, alternating groups, groups of Lie type, or one of 26 sporadic groups. "
                "The longest collaborative proof in mathematics."
            ),
            "authors": ["Daniel Gorenstein", "Richard Lyons", "Ronald Solomon"],
            "citation_count": 9000,
            "importance_score": 0.96,
            "proven": True,
            "downstream_theorems": 180,
            "cross_domain_influence": ["Representation Theory", "Combinatorics"],
        },
        {
            "concept_id": "C014",
            "name": "Grothendieck's Schemes",
            "domain": "Algebraic Geometry",
            "concept_type": "category",
            "year_introduced": 1960,
            "abstract": (
                "A generalization of algebraic varieties that allows singularities and works over "
                "arbitrary commutative rings. Grothendieck's reformulation revolutionized algebraic "
                "geometry and led to the proof of the Weil conjectures."
            ),
            "authors": ["Alexander Grothendieck"],
            "citation_count": 14000,
            "importance_score": 0.99,
            "proven": True,
            "downstream_theorems": 350,
            "cross_domain_influence": ["Number Theory", "Topology", "Category Theory", "Algebra"],
        },
        {
            "concept_id": "C015",
            "name": "Langlands Program",
            "domain": "Number Theory",
            "concept_type": "conjecture",
            "year_introduced": 1967,
            "abstract": (
                "A vast web of conjectures connecting automorphic forms, Galois representations, "
                "and L-functions. Called the Grand Unified Theory of mathematics, it subsumes "
                "Fermat's Last Theorem as a special case."
            ),
            "authors": ["Robert Langlands"],
            "citation_count": 16000,
            "importance_score": 1.0,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Representation Theory", "Algebraic Geometry", "Algebra"],
        },
        # Category Theory
        {
            "concept_id": "C016",
            "name": "Yoneda Lemma",
            "domain": "Category Theory",
            "concept_type": "theorem",
            "year_introduced": 1954,
            "abstract": (
                "A functor from a locally small category to Set is naturally isomorphic to "
                "the hom-functor if and only if it is representable. The fundamental theorem "
                "of category theory, stating that objects are completely determined by their relationships."
            ),
            "authors": ["Nobuo Yoneda"],
            "citation_count": 5500,
            "importance_score": 0.9,
            "proven": True,
            "downstream_theorems": 160,
            "cross_domain_influence": ["Algebra", "Topology", "Logic"],
        },
        {
            "concept_id": "C017",
            "name": "Higher Category Theory",
            "domain": "Category Theory",
            "concept_type": "category",
            "year_introduced": 1998,
            "abstract": (
                "A generalization of category theory to n-categories with morphisms between "
                "morphisms at every level. Provides the language for homotopy theory, TQFT, "
                "and modern algebraic topology."
            ),
            "authors": ["John Baez", "James Dolan", "Jacob Lurie"],
            "citation_count": 5000,
            "importance_score": 0.87,
            "proven": True,
            "downstream_theorems": 120,
            "cross_domain_influence": ["Topology", "Mathematical Physics", "Algebra"],
        },
        # Logic and Foundations
        {
            "concept_id": "C018",
            "name": "Gödel's Incompleteness Theorems",
            "domain": "Logic",
            "concept_type": "theorem",
            "year_introduced": 1931,
            "abstract": (
                "Any consistent formal system capable of basic arithmetic contains true statements "
                "that cannot be proved within the system. Fundamental limits on mathematical formalization "
                "with profound philosophical implications."
            ),
            "authors": ["Kurt Gödel"],
            "citation_count": 18000,
            "importance_score": 1.0,
            "proven": True,
            "downstream_theorems": 250,
            "cross_domain_influence": ["Algebra", "Combinatorics", "Quantum Information"],
        },
        {
            "concept_id": "C019",
            "name": "Zermelo-Fraenkel Axioms",
            "domain": "Logic",
            "concept_type": "axiom",
            "year_introduced": 1922,
            "abstract": (
                "The standard axiomatic system for set theory including the axiom of choice. "
                "The foundation upon which most of modern mathematics is built."
            ),
            "authors": ["Ernst Zermelo", "Abraham Fraenkel"],
            "citation_count": 7000,
            "importance_score": 0.95,
            "proven": True,
            "downstream_theorems": 500,
            "cross_domain_influence": ["Algebra", "Topology", "Functional Analysis"],
        },
        # Differential Geometry
        {
            "concept_id": "C020",
            "name": "Ricci Flow",
            "domain": "Differential Geometry",
            "concept_type": "equation",
            "year_introduced": 1982,
            "abstract": (
                "A process that deforms the metric of a Riemannian manifold in a way formally "
                "analogous to heat diffusion. Key tool in Perelman's proof of the Poincaré Conjecture "
                "and geometrization of 3-manifolds."
            ),
            "authors": ["Richard Hamilton", "Grigori Perelman"],
            "citation_count": 8500,
            "importance_score": 0.96,
            "proven": True,
            "downstream_theorems": 110,
            "cross_domain_influence": ["Topology", "PDEs", "Mathematical Physics"],
        },
        {
            "concept_id": "C021",
            "name": "Morse Theory",
            "domain": "Differential Geometry",
            "concept_type": "theorem",
            "year_introduced": 1934,
            "abstract": (
                "Studies the topology of manifolds using differentiable functions. Critical points "
                "of smooth functions determine the topology. Fundamental connection between calculus "
                "and topology."
            ),
            "authors": ["Marston Morse"],
            "citation_count": 7800,
            "importance_score": 0.93,
            "proven": True,
            "downstream_theorems": 130,
            "cross_domain_influence": ["Topology", "Functional Analysis", "Mathematical Physics"],
        },
        {
            "concept_id": "C022",
            "name": "Gauss-Bonnet Theorem",
            "domain": "Differential Geometry",
            "concept_type": "theorem",
            "year_introduced": 1848,
            "abstract": (
                "The integral of the Gaussian curvature of a closed surface equals 2π times "
                "the Euler characteristic. A fundamental bridge between local differential geometry "
                "and global topology."
            ),
            "authors": ["Carl Friedrich Gauss", "Pierre Ossian Bonnet"],
            "citation_count": 6500,
            "importance_score": 0.91,
            "proven": True,
            "downstream_theorems": 145,
            "cross_domain_influence": ["Topology", "Mathematical Physics"],
        },
        # Functional Analysis
        {
            "concept_id": "C023",
            "name": "Spectral Theorem",
            "domain": "Functional Analysis",
            "concept_type": "theorem",
            "year_introduced": 1929,
            "abstract": (
                "Self-adjoint operators on Hilbert spaces have a spectral decomposition. "
                "Fundamental to quantum mechanics, providing the mathematical basis for "
                "observables and measurement."
            ),
            "authors": ["John von Neumann"],
            "citation_count": 10000,
            "importance_score": 0.97,
            "proven": True,
            "downstream_theorems": 200,
            "cross_domain_influence": ["Mathematical Physics", "Algebra", "Quantum Information"],
        },
        {
            "concept_id": "C024",
            "name": "Hahn-Banach Theorem",
            "domain": "Functional Analysis",
            "concept_type": "theorem",
            "year_introduced": 1929,
            "abstract": (
                "A bounded linear functional on a subspace of a normed vector space can be "
                "extended to the whole space preserving the norm. Cornerstone of functional "
                "analysis with applications throughout mathematics."
            ),
            "authors": ["Hans Hahn", "Stefan Banach"],
            "citation_count": 6000,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 180,
            "cross_domain_influence": ["Optimization", "PDEs"],
        },
        # PDEs
        {
            "concept_id": "C025",
            "name": "Navier-Stokes Existence",
            "domain": "PDEs",
            "concept_type": "conjecture",
            "year_introduced": 1845,
            "abstract": (
                "Do smooth solutions to the Navier-Stokes equations always exist in 3D? "
                "A Millennium Prize Problem fundamental to fluid dynamics and turbulence theory "
                "with implications for weather prediction and engineering."
            ),
            "authors": ["Claude-Louis Navier", "George Gabriel Stokes"],
            "citation_count": 9000,
            "importance_score": 0.95,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Mathematical Physics", "Functional Analysis", "Dynamical Systems"],
        },
        {
            "concept_id": "C026",
            "name": "Yang-Mills Existence",
            "domain": "Mathematical Physics",
            "concept_type": "conjecture",
            "year_introduced": 1954,
            "abstract": (
                "Do Yang-Mills gauge theories have a mass gap in 4D? A Millennium Prize Problem "
                "at the intersection of mathematics and quantum field theory. Resolution would "
                "explain why quarks are confined."
            ),
            "authors": ["Chen-Ning Yang", "Robert Mills"],
            "citation_count": 8500,
            "importance_score": 0.94,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["PDEs", "Topology", "Differential Geometry"],
        },
        # Algebraic Geometry
        {
            "concept_id": "C027",
            "name": "Weil Conjectures",
            "domain": "Algebraic Geometry",
            "concept_type": "theorem",
            "year_introduced": 1949,
            "abstract": (
                "Conjectures about the generating functions (zeta functions) of the number of "
                "points of algebraic varieties over finite fields. Proved by Deligne in 1974 "
                "using étale cohomology developed by Grothendieck."
            ),
            "authors": ["André Weil", "Pierre Deligne"],
            "citation_count": 8000,
            "importance_score": 0.95,
            "proven": True,
            "downstream_theorems": 115,
            "cross_domain_influence": ["Number Theory", "Topology", "Algebra"],
        },
        {
            "concept_id": "C028",
            "name": "Mirror Symmetry",
            "domain": "Algebraic Geometry",
            "concept_type": "conjecture",
            "year_introduced": 1990,
            "abstract": (
                "Two Calabi-Yau manifolds can be related such that the complex geometry of one "
                "equals the symplectic geometry of the other. Discovered in string theory, it "
                "predicts surprising equalities in enumerative geometry."
            ),
            "authors": ["Philip Candelas", "Xenia de la Ossa", "Paul Green", "Linda Parkes"],
            "citation_count": 7500,
            "importance_score": 0.92,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Mathematical Physics", "Topology", "Differential Geometry"],
        },
        # Probability
        {
            "concept_id": "C029",
            "name": "Central Limit Theorem",
            "domain": "Probability",
            "concept_type": "theorem",
            "year_introduced": 1920,
            "abstract": (
                "The sum of many independent random variables tends toward a normal distribution. "
                "Foundation of statistical inference and one of the most widely applied results "
                "in mathematics."
            ),
            "authors": ["Aleksandr Lyapunov", "Jarl Waldemar Lindeberg"],
            "citation_count": 11000,
            "importance_score": 0.95,
            "proven": True,
            "downstream_theorems": 300,
            "cross_domain_influence": ["Functional Analysis", "PDEs", "Mathematical Physics"],
        },
        {
            "concept_id": "C030",
            "name": "Ergodic Theory",
            "domain": "Dynamical Systems",
            "concept_type": "theorem",
            "year_introduced": 1931,
            "abstract": (
                "Time averages equal space averages for ergodic dynamical systems. "
                "Fundamental to statistical mechanics, connecting thermodynamics to measure theory "
                "and providing tools for understanding long-term behavior."
            ),
            "authors": ["John von Neumann", "George David Birkhoff"],
            "citation_count": 6500,
            "importance_score": 0.89,
            "proven": True,
            "downstream_theorems": 160,
            "cross_domain_influence": ["Probability", "Mathematical Physics", "Number Theory"],
        },
        # Representation Theory
        {
            "concept_id": "C031",
            "name": "Peter-Weyl Theorem",
            "domain": "Representation Theory",
            "concept_type": "theorem",
            "year_introduced": 1927,
            "abstract": (
                "The matrix coefficients of irreducible unitary representations of a compact "
                "group form an orthonormal basis of L²(G). Foundation of harmonic analysis on "
                "groups."
            ),
            "authors": ["Hermann Weyl", "Fritz Peter"],
            "citation_count": 4500,
            "importance_score": 0.85,
            "proven": True,
            "downstream_therems": 90,
            "downstream_theorems": 90,
            "cross_domain_influence": ["Functional Analysis", "Mathematical Physics"],
        },
        {
            "concept_id": "C032",
            "name": "Geometric Langlands",
            "domain": "Representation Theory",
            "concept_type": "conjecture",
            "year_introduced": 1987,
            "abstract": (
                "A geometric analog of the Langlands program relating D-modules on the stack "
                "of G-bundles to local systems. Recently proved by a large collaboration, "
                "yielding new tools in geometric representation theory."
            ),
            "authors": ["Vladimir Drinfeld", "Alexander Beilinson"],
            "citation_count": 5500,
            "importance_score": 0.91,
            "proven": True,
            "downstream_theorems": 80,
            "cross_domain_influence": ["Algebraic Geometry", "Category Theory", "Number Theory"],
        },
        # Quantum Information
        {
            "concept_id": "C033",
            "name": "Quantum Error Correction",
            "domain": "Quantum Information",
            "concept_type": "theorem",
            "year_introduced": 1995,
            "abstract": (
                "Quantum information can be protected from decoherence by encoding qubits into "
                "entangled states. The threshold theorem guarantees fault-tolerant quantum "
                "computation is possible."
            ),
            "authors": ["Peter Shor", "Andrew Steane"],
            "citation_count": 7000,
            "importance_score": 0.92,
            "proven": True,
            "downstream_theorems": 95,
            "cross_domain_influence": ["Algebra", "Topology", "Functional Analysis"],
        },
        # Optimization
        {
            "concept_id": "C034",
            "name": "Compressed Sensing",
            "domain": "Optimization",
            "concept_type": "theorem",
            "year_introduced": 2006,
            "abstract": (
                "Sparse signals can be recovered from far fewer measurements than Shannon-Nyquist "
                "requires, using convex optimization. Revolutionized signal processing and has "
                "applications in MRI, astronomy, and data science."
            ),
            "authors": ["Emmanuel Candès", "Terence Tao", "David Donoho"],
            "citation_count": 8000,
            "importance_score": 0.93,
            "proven": True,
            "downstream_theorems": 115,
            "cross_domain_influence": ["Probability", "Combinatorics", "Functional Analysis"],
        },
        # Combinatorics
        {
            "concept_id": "C035",
            "name": "Ramsey Theory",
            "domain": "Combinatorics",
            "concept_type": "theorem",
            "year_introduced": 1930,
            "abstract": (
                "Complete disorder is impossible: any sufficiently large structure must contain "
                "a regular substructure. Ramsey numbers quantify how large structures must be "
                "to guarantee regularity."
            ),
            "authors": ["Frank Ramsey"],
            "citation_count": 5000,
            "importance_score": 0.84,
            "proven": True,
            "downstream_theorems": 100,
            "cross_domain_influence": ["Logic", "Number Theory"],
        },
        # More concepts to reach ~80
        {
            "concept_id": "C036",
            "name": "Banach-Tarski Paradox",
            "domain": "Functional Analysis",
            "concept_type": "theorem",
            "year_introduced": 1924,
            "abstract": (
                "A solid ball can be decomposed into a finite number of pieces and reassembled "
                "into two identical balls. Demonstrates the counterintuitive consequences of the "
                "axiom of choice."
            ),
            "authors": ["Stefan Banach", "Alfred Tarski"],
            "citation_count": 4500,
            "importance_score": 0.8,
            "proven": True,
            "downstream_theorems": 50,
            "cross_domain_influence": ["Logic", "Algebra"],
        },
        {
            "concept_id": "C037",
            "name": "Four Color Theorem",
            "domain": "Combinatorics",
            "concept_type": "theorem",
            "year_introduced": 1976,
            "abstract": (
                "Any planar map can be colored with at most four colors such that no adjacent "
                "regions share the same color. The first major theorem proved with computer "
                "assistance."
            ),
            "authors": ["Kenneth Appel", "Wolfgang Haken"],
            "citation_count": 6000,
            "importance_score": 0.85,
            "proven": True,
            "downstream_theorems": 65,
            "cross_domain_influence": ["Topology", "Logic"],
        },
        {
            "concept_id": "C038",
            "name": "Serre Spectral Sequence",
            "domain": "Algebraic Geometry",
            "concept_type": "theorem",
            "year_introduced": 1951,
            "abstract": (
                "A spectral sequence relating the cohomology of a fibration to the cohomology "
                "of its fiber and base. A fundamental computational tool in algebraic topology "
                "and algebraic geometry."
            ),
            "authors": ["Jean-Pierre Serre"],
            "citation_count": 5500,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 140,
            "cross_domain_influence": ["Topology", "Algebra"],
        },
        {
            "concept_id": "C039",
            "name": "K-Theory",
            "domain": "Algebra",
            "concept_type": "theorem",
            "year_introduced": 1957,
            "abstract": (
                "A generalized cohomology theory built from vector bundles, K-theory provides "
                "invariants of topological spaces and algebraic varieties. Central to the "
                "Atiyah-Singer index theorem."
            ),
            "authors": ["Alexander Grothendieck", "Michael Atiyah", "Friedrich Hirzebruch"],
            "citation_count": 6500,
            "importance_score": 0.91,
            "proven": True,
            "downstream_theorems": 155,
            "cross_domain_influence": ["Topology", "Mathematical Physics", "Number Theory"],
        },
        {
            "concept_id": "C040",
            "name": "Non-Archimedean Geometry",
            "domain": "Algebraic Geometry",
            "concept_type": "theorem",
            "year_introduced": 1962,
            "abstract": (
                "Geometry over fields with non-Archimedean absolute values, such as p-adic fields. "
                "Tate's rigid analytic spaces provide a framework for p-adic analogues of complex "
                "analytic geometry."
            ),
            "authors": ["John Tate"],
            "citation_count": 4500,
            "importance_score": 0.86,
            "proven": True,
            "downstream_theorems": 100,
            "cross_domain_influence": ["Number Theory", "Topology", "Algebra"],
        },
        {
            "concept_id": "C041",
            "name": "Stochastic Calculus",
            "domain": "Probability",
            "concept_type": "theorem",
            "year_introduced": 1944,
            "abstract": (
                "Itô's lemma provides a change-of-variables formula for stochastic processes, "
                "enabling the analysis of systems driven by Brownian motion. Foundation of "
                "mathematical finance and stochastic differential equations."
            ),
            "authors": ["Kiyosi Itô"],
            "citation_count": 7500,
            "importance_score": 0.92,
            "proven": True,
            "downstream_theorems": 170,
            "cross_domain_influence": ["PDEs", "Mathematical Physics", "Optimization"],
        },
        {
            "concept_id": "C042",
            "name": "Homotopy Type Theory",
            "domain": "Logic",
            "concept_type": "axiom",
            "year_introduced": 2010,
            "abstract": (
                "An alternative foundation for mathematics based on Martin-Löf type theory "
                "where types are interpreted as homotopy types. Provides a connection between "
                "constructive mathematics and homotopy theory."
            ),
            "authors": ["Vladimir Voevodsky"],
            "citation_count": 3000,
            "importance_score": 0.82,
            "proven": True,
            "downstream_theorems": 60,
            "cross_domain_influence": ["Topology", "Category Theory"],
        },
        {
            "concept_id": "C043",
            "name": "Baum-Connes Conjecture",
            "domain": "Functional Analysis",
            "concept_type": "conjecture",
            "year_introduced": 1980,
            "abstract": (
                "The assembly map from the K-homology of the classifying space of a group to "
                "the K-theory of its reduced C*-algebra is an isomorphism. Implies the Novikov "
                "conjecture on higher signatures."
            ),
            "authors": ["Paul Baum", "Alain Connes"],
            "citation_count": 4000,
            "importance_score": 0.85,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Topology", "Algebra", "Representation Theory"],
        },
        {
            "concept_id": "C044",
            "name": "Floer Homology",
            "domain": "Topology",
            "concept_type": "homology class",
            "year_introduced": 1988,
            "abstract": (
                "An infinite-dimensional analogue of Morse homology defining invariants of "
                "3-manifolds and knots. Key to understanding symplectic topology and proving "
                "Arnold's conjectures."
            ),
            "authors": ["Andreas Floer"],
            "citation_count": 5500,
            "importance_score": 0.9,
            "proven": True,
            "downstream_theorems": 120,
            "cross_domain_influence": ["Differential Geometry", "Mathematical Physics", "Algebra"],
        },
        {
            "concept_id": "C045",
            "name": "Geometric Measure Theory",
            "domain": "Differential Geometry",
            "concept_type": "theorem",
            "year_introduced": 1960,
            "abstract": (
                "Extends measure theory and calculus of variations to geometric settings. "
                "Plateau's problem on minimal surfaces is resolved using currents. Foundation "
                "for modern PDE approaches to geometric variational problems."
            ),
            "authors": ["Herbert Federer", "Wendell Fleming"],
            "citation_count": 4000,
            "importance_score": 0.84,
            "proven": True,
            "downstream_theorems": 95,
            "cross_domain_influence": ["PDEs", "Topology", "Functional Analysis"],
        },
        {
            "concept_id": "C046",
            "name": "Motivic Cohomology",
            "domain": "Algebraic Geometry",
            "concept_type": "theorem",
            "year_introduced": 1987,
            "abstract": (
                "A cohomology theory for algebraic varieties that provides a universal target "
                "for Chern class maps. Voevodsky's construction of motivic cohomology resolved "
                "the Milnor and Bloch-Kato conjectures."
            ),
            "authors": ["Vladimir Voevodsky", "Andrei Suslin"],
            "citation_count": 4500,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 85,
            "cross_domain_influence": ["Number Theory", "Algebra", "Topology"],
        },
        {
            "concept_id": "C047",
            "name": "Szemerédi Regularity Lemma",
            "domain": "Combinatorics",
            "concept_type": "theorem",
            "year_introduced": 1975,
            "abstract": (
                "Every sufficiently large graph can be approximated by a random bipartite graph "
                "on each pair of vertex classes. A cornerstone result with applications throughout "
                "combinatorics, number theory, and computer science."
            ),
            "authors": ["Endre Szemerédi"],
            "citation_count": 5000,
            "importance_score": 0.87,
            "proven": True,
            "downstream_theorems": 105,
            "cross_domain_influence": ["Number Theory", "Logic", "Probability"],
        },
        {
            "concept_id": "C048",
            "name": "Topological Quantum Field Theory",
            "domain": "Mathematical Physics",
            "concept_type": "category",
            "year_introduced": 1989,
            "abstract": (
                "A quantum field theory that is invariant under smooth deformations of spacetime. "
                "Witten's approach led to new topological invariants of 3-manifolds including "
                "the Jones polynomial."
            ),
            "authors": ["Michael Atiyah", "Edward Witten"],
            "citation_count": 6000,
            "importance_score": 0.91,
            "proven": True,
            "downstream_theorems": 130,
            "cross_domain_influence": ["Topology", "Algebra", "Category Theory"],
        },
        {
            "concept_id": "C049",
            "name": "Borel-Cantelli Lemma",
            "domain": "Probability",
            "concept_type": "theorem",
            "year_introduced": 1909,
            "abstract": (
                "If the sum of probabilities of a sequence of events is finite then only finitely "
                "many occur almost surely. Fundamental tool in probability theory for establishing "
                "almost sure convergence."
            ),
            "authors": ["Émile Borel", "Francesco Cantelli"],
            "citation_count": 3500,
            "importance_score": 0.78,
            "proven": True,
            "downstream_theorems": 80,
            "cross_domain_influence": ["Dynamical Systems", "Number Theory"],
        },
        {
            "concept_id": "C050",
            "name": "Connes Noncommutative Geometry",
            "domain": "Algebra",
            "concept_type": "theorem",
            "year_introduced": 1994,
            "abstract": (
                "Extends Riemannian geometry to noncommutative spaces using spectral triples. "
                "Provides a unified framework for the Standard Model of particle physics and "
                "connects to number theory via the Riemann zeta function."
            ),
            "authors": ["Alain Connes"],
            "citation_count": 5500,
            "importance_score": 0.89,
            "proven": True,
            "downstream_theorems": 100,
            "cross_domain_influence": ["Mathematical Physics", "Number Theory", "Functional Analysis"],
        },
        {
            "concept_id": "C051",
            "name": "Algebraic K-Theory Conjecture",
            "domain": "Algebra",
            "concept_type": "conjecture",
            "year_introduced": 1973,
            "abstract": (
                "Deep relationships between algebraic K-groups of rings and arithmetic. "
                "Quillen's higher K-theory groups encode information about algebraic varieties "
                "relevant to the Lichtenbaum conjectures."
            ),
            "authors": ["Daniel Quillen"],
            "citation_count": 3500,
            "importance_score": 0.83,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Number Theory", "Algebraic Geometry"],
        },
        {
            "concept_id": "C052",
            "name": "Chaos Theory",
            "domain": "Dynamical Systems",
            "concept_type": "theorem",
            "year_introduced": 1963,
            "abstract": (
                "Deterministic dynamical systems can exhibit sensitive dependence on initial "
                "conditions, making long-term prediction impossible. Lorenz's discovery opened "
                "new perspectives on nonlinear dynamics."
            ),
            "authors": ["Edward Lorenz", "Stephen Smale"],
            "citation_count": 8000,
            "importance_score": 0.9,
            "proven": True,
            "downstream_theorems": 175,
            "cross_domain_influence": ["PDEs", "Mathematical Physics", "Probability"],
        },
        {
            "concept_id": "C053",
            "name": "Free Probability Theory",
            "domain": "Probability",
            "concept_type": "theorem",
            "year_introduced": 1991,
            "abstract": (
                "A noncommutative analogue of probability theory where independence is replaced "
                "by freeness. Connects to random matrix theory and the Connes embedding problem "
                "in operator algebras."
            ),
            "authors": ["Dan-Virgil Voiculescu"],
            "citation_count": 3000,
            "importance_score": 0.82,
            "proven": True,
            "downstream_theorems": 75,
            "cross_domain_influence": ["Functional Analysis", "Algebra", "Combinatorics"],
        },
        {
            "concept_id": "C054",
            "name": "Iwasawa Theory",
            "domain": "Number Theory",
            "concept_type": "theorem",
            "year_introduced": 1959,
            "abstract": (
                "Studies the growth of class groups and Selmer groups over towers of number "
                "fields. The main conjecture (proved by Mazur-Wiles) connects p-adic L-functions "
                "to arithmetic."
            ),
            "authors": ["Kenkichi Iwasawa"],
            "citation_count": 4000,
            "importance_score": 0.85,
            "proven": True,
            "downstream_theorems": 90,
            "cross_domain_influence": ["Algebraic Geometry", "Algebra"],
        },
        {
            "concept_id": "C055",
            "name": "Univalence Axiom",
            "domain": "Logic",
            "concept_type": "axiom",
            "year_introduced": 2006,
            "abstract": (
                "Equivalent types are identical. Voevodsky's univalence axiom provides a "
                "computational interpretation of equality in type theory compatible with "
                "homotopy-theoretic intuitions."
            ),
            "authors": ["Vladimir Voevodsky"],
            "citation_count": 2500,
            "importance_score": 0.8,
            "proven": True,
            "downstream_theorems": 55,
            "cross_domain_influence": ["Category Theory", "Topology"],
        },
        {
            "concept_id": "C056",
            "name": "Quantum Groups",
            "domain": "Algebra",
            "concept_type": "group",
            "year_introduced": 1985,
            "abstract": (
                "Noncommutative deformations of classical Lie groups and Hopf algebras, "
                "arising in quantum integrable systems and knot invariants. Provide new "
                "symmetry structures in mathematical physics."
            ),
            "authors": ["Vladimir Drinfeld", "Michio Jimbo"],
            "citation_count": 5500,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 120,
            "cross_domain_influence": ["Representation Theory", "Mathematical Physics", "Topology"],
        },
        {
            "concept_id": "C057",
            "name": "Minimal Model Program",
            "domain": "Algebraic Geometry",
            "concept_type": "theorem",
            "year_introduced": 1982,
            "abstract": (
                "A program to classify higher-dimensional algebraic varieties by finding "
                "canonical models. The existence of flips was proved by Hacon-McKernan, "
                "completing the MMP in many cases."
            ),
            "authors": ["Shigefumi Mori", "Christopher Hacon", "James McKernan"],
            "citation_count": 5000,
            "importance_score": 0.89,
            "proven": True,
            "downstream_theorems": 110,
            "cross_domain_influence": ["Differential Geometry", "Number Theory"],
        },
        {
            "concept_id": "C058",
            "name": "Donaldson Theory",
            "domain": "Differential Geometry",
            "concept_type": "theorem",
            "year_introduced": 1983,
            "abstract": (
                "Using instantons from Yang-Mills theory to define differential invariants of "
                "smooth 4-manifolds, Donaldson proved exotic smooth structures exist on R^4. "
                "Revolutionized 4-manifold topology."
            ),
            "authors": ["Simon Donaldson"],
            "citation_count": 5500,
            "importance_score": 0.9,
            "proven": True,
            "downstream_theorems": 100,
            "cross_domain_influence": ["Topology", "Mathematical Physics", "Algebra"],
        },
        {
            "concept_id": "C059",
            "name": "Thurston Geometrization",
            "domain": "Topology",
            "concept_type": "theorem",
            "year_introduced": 1982,
            "abstract": (
                "Every closed 3-manifold can be decomposed into pieces each admitting one of "
                "eight geometric structures. Proved by Perelman, subsuming the Poincaré Conjecture "
                "as a special case."
            ),
            "authors": ["William Thurston", "Grigori Perelman"],
            "citation_count": 6500,
            "importance_score": 0.94,
            "proven": True,
            "downstream_theorems": 125,
            "cross_domain_influence": ["Differential Geometry", "Mathematical Physics"],
        },
        {
            "concept_id": "C060",
            "name": "Richardson Variety",
            "domain": "Representation Theory",
            "concept_type": "manifold",
            "year_introduced": 1992,
            "abstract": (
                "Intersections of Schubert and opposite Schubert varieties in flag varieties. "
                "Key to understanding the geometry of Schubert calculus and cluster algebras "
                "in representation theory."
            ),
            "authors": ["Richard Richardson"],
            "citation_count": 2000,
            "importance_score": 0.75,
            "proven": True,
            "downstream_theorems": 45,
            "cross_domain_influence": ["Algebraic Geometry", "Combinatorics"],
        },
        {
            "concept_id": "C061",
            "name": "Langlands Functoriality",
            "domain": "Number Theory",
            "concept_type": "conjecture",
            "year_introduced": 1970,
            "abstract": (
                "Automorphic representations of different groups are related by natural transfers. "
                "Part of the Langlands program whose partial results already imply major theorems "
                "in number theory."
            ),
            "authors": ["Robert Langlands"],
            "citation_count": 5000,
            "importance_score": 0.91,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Representation Theory", "Algebra"],
        },
        {
            "concept_id": "C062",
            "name": "Calabi-Yau Manifolds",
            "domain": "Differential Geometry",
            "concept_type": "manifold",
            "year_introduced": 1954,
            "abstract": (
                "Complex manifolds with trivial canonical bundle. Yau's proof of the Calabi "
                "conjecture guarantees the existence of Ricci-flat metrics. Central objects in "
                "string theory compactification."
            ),
            "authors": ["Eugenio Calabi", "Shing-Tung Yau"],
            "citation_count": 8000,
            "importance_score": 0.93,
            "proven": True,
            "downstream_theorems": 160,
            "cross_domain_influence": ["Mathematical Physics", "Algebraic Geometry", "Topology"],
        },
        {
            "concept_id": "C063",
            "name": "Random Matrix Theory",
            "domain": "Probability",
            "concept_type": "theorem",
            "year_introduced": 1928,
            "abstract": (
                "Studies the spectral properties of large random matrices. The universality of "
                "eigenvalue spacing distributions connects to the Riemann Hypothesis, quantum "
                "chaos, and statistical physics."
            ),
            "authors": ["John Wishart", "Eugene Wigner", "Freeman Dyson"],
            "citation_count": 7000,
            "importance_score": 0.91,
            "proven": True,
            "downstream_theorems": 140,
            "cross_domain_influence": ["Number Theory", "Mathematical Physics", "Combinatorics"],
        },
        {
            "concept_id": "C064",
            "name": "Khovanov Homology",
            "domain": "Topology",
            "concept_type": "homology class",
            "year_introduced": 2000,
            "abstract": (
                "A categorification of the Jones polynomial providing stronger knot invariants. "
                "Represents the philosophy that polynomial invariants arise as Euler characteristics "
                "of chain complexes."
            ),
            "authors": ["Mikhail Khovanov"],
            "citation_count": 4000,
            "importance_score": 0.86,
            "proven": True,
            "downstream_theorems": 90,
            "cross_domain_influence": ["Algebra", "Representation Theory", "Mathematical Physics"],
        },
        {
            "concept_id": "C065",
            "name": "Arithmetic Langlands",
            "domain": "Number Theory",
            "concept_type": "conjecture",
            "year_introduced": 1972,
            "abstract": (
                "Global Langlands correspondence connecting Galois representations to automorphic "
                "forms over number fields. Proved for GL(1) by class field theory and GL(2) by "
                "modular forms."
            ),
            "authors": ["Robert Langlands", "Ngô Bảo Châu"],
            "citation_count": 6000,
            "importance_score": 0.93,
            "proven": False,
            "downstream_theorems": 0,
            "cross_domain_influence": ["Algebraic Geometry", "Representation Theory"],
        },
        {
            "concept_id": "C066",
            "name": "Perverse Sheaves",
            "domain": "Algebraic Geometry",
            "concept_type": "functor",
            "year_introduced": 1980,
            "abstract": (
                "A t-structure on the derived category of constructible sheaves whose heart "
                "provides geometric analogues of local systems. Used by Ngô to prove the "
                "fundamental lemma."
            ),
            "authors": ["Alexander Beilinson", "Joseph Bernstein", "Pierre Deligne"],
            "citation_count": 4500,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 100,
            "cross_domain_influence": ["Representation Theory", "Topology", "Category Theory"],
        },
        {
            "concept_id": "C067",
            "name": "Symplectic Topology",
            "domain": "Differential Geometry",
            "concept_type": "theorem",
            "year_introduced": 1985,
            "abstract": (
                "Gromov's non-squeezing theorem showed that symplectic geometry is fundamentally "
                "different from Riemannian geometry. Opened the field of symplectic topology and "
                "motivated Floer homology."
            ),
            "authors": ["Mikhail Gromov"],
            "citation_count": 5000,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 115,
            "cross_domain_influence": ["Topology", "Mathematical Physics", "PDEs"],
        },
        {
            "concept_id": "C068",
            "name": "Bourgain's Decoupling",
            "domain": "Functional Analysis",
            "concept_type": "theorem",
            "year_introduced": 2015,
            "abstract": (
                "Decoupling inequalities for curved manifolds in harmonic analysis with "
                "applications to exponential sums, PDEs, and number theory. Resolves "
                "Vinogradov's mean value conjecture."
            ),
            "authors": ["Jean Bourgain", "Ciprian Demeter"],
            "citation_count": 2500,
            "importance_score": 0.84,
            "proven": True,
            "downstream_theorems": 55,
            "cross_domain_influence": ["Number Theory", "PDEs", "Combinatorics"],
        },
        {
            "concept_id": "C069",
            "name": "Infinity Topos Theory",
            "domain": "Category Theory",
            "concept_type": "category",
            "year_introduced": 2006,
            "abstract": (
                "Lurie's higher topos theory generalizes Grothendieck toposes to the homotopy-"
                "coherent setting. Provides the framework for derived algebraic geometry and "
                "chromatic homotopy theory."
            ),
            "authors": ["Jacob Lurie"],
            "citation_count": 3500,
            "importance_score": 0.86,
            "proven": True,
            "downstream_theorems": 80,
            "cross_domain_influence": ["Algebraic Geometry", "Topology", "Logic"],
        },
        {
            "concept_id": "C070",
            "name": "Monstrous Moonshine",
            "domain": "Algebra",
            "concept_type": "theorem",
            "year_introduced": 1979,
            "abstract": (
                "The coefficients of the j-function are dimensions of representations of the "
                "Monster group. Proved by Borcherds using vertex algebras, connecting group "
                "theory, number theory, and string theory."
            ),
            "authors": ["John Conway", "Simon Norton", "Richard Borcherds"],
            "citation_count": 4500,
            "importance_score": 0.88,
            "proven": True,
            "downstream_theorems": 95,
            "cross_domain_influence": ["Number Theory", "Mathematical Physics", "Representation Theory"],
        },
        {
            "concept_id": "C071",
            "name": "Optimal Transport",
            "domain": "Optimization",
            "concept_type": "theorem",
            "year_introduced": 1781,
            "abstract": (
                "The Monge-Kantorovich problem of optimally transporting one distribution to "
                "another. Villani and Brenier's work connected it to PDEs, geometry, and "
                "machine learning."
            ),
            "authors": ["Gaspard Monge", "Leonid Kantorovich", "Cédric Villani"],
            "citation_count": 7000,
            "importance_score": 0.91,
            "proven": True,
            "downstream_theorems": 145,
            "cross_domain_influence": ["PDEs", "Probability", "Differential Geometry"],
        },
        {
            "concept_id": "C072",
            "name": "Perfectoid Spaces",
            "domain": "Algebraic Geometry",
            "concept_type": "topological space",
            "year_introduced": 2012,
            "abstract": (
                "Scholze's perfectoid spaces provide a framework for working simultaneously "
                "with characteristic 0 and characteristic p geometry. Led to proofs of major "
                "conjectures in p-adic Hodge theory and the weight-monodromy conjecture."
            ),
            "authors": ["Peter Scholze"],
            "citation_count": 5000,
            "importance_score": 0.93,
            "proven": True,
            "downstream_theorems": 85,
            "cross_domain_influence": ["Number Theory", "Algebra", "Topology"],
        },
        {
            "concept_id": "C073",
            "name": "Prismatic Cohomology",
            "domain": "Algebraic Geometry",
            "concept_type": "theorem",
            "year_introduced": 2019,
            "abstract": (
                "A new cohomology theory for p-adic formal schemes unifying crystalline, "
                "de Rham, and étale cohomology theories. Developed by Bhatt-Scholze to give "
                "a uniform treatment of p-adic comparison theorems."
            ),
            "authors": ["Bhargav Bhatt", "Peter Scholze"],
            "citation_count": 2000,
            "importance_score": 0.87,
            "proven": True,
            "downstream_theorems": 40,
            "cross_domain_influence": ["Number Theory", "Topology", "Algebra"],
        },
        {
            "concept_id": "C074",
            "name": "Tao-Green Primes",
            "domain": "Number Theory",
            "concept_type": "theorem",
            "year_introduced": 2004,
            "abstract": (
                "The primes contain arbitrarily long arithmetic progressions. Proof combined "
                "Fourier analysis, ergodic theory, and combinatorics in a new synthesis, "
                "proving a famous conjecture of Erdős."
            ),
            "authors": ["Ben Green", "Terence Tao"],
            "citation_count": 5500,
            "importance_score": 0.9,
            "proven": True,
            "downstream_theorems": 85,
            "cross_domain_influence": ["Combinatorics", "Dynamical Systems", "Functional Analysis"],
        },
        {
            "concept_id": "C075",
            "name": "Fukaya Category",
            "domain": "Differential Geometry",
            "concept_type": "category",
            "year_introduced": 1993,
            "abstract": (
                "An A-infinity category whose objects are Lagrangian submanifolds of a symplectic "
                "manifold. Central object in homological mirror symmetry and symplectic topology."
            ),
            "authors": ["Kenji Fukaya"],
            "citation_count": 3500,
            "importance_score": 0.85,
            "proven": True,
            "downstream_theorems": 80,
            "cross_domain_influence": ["Algebraic Geometry", "Category Theory", "Mathematical Physics"],
        },
        {
            "concept_id": "C076",
            "name": "Elliptic Curves",
            "domain": "Number Theory",
            "concept_type": "equation",
            "year_introduced": 1844,
            "abstract": (
                "Smooth projective algebraic curves of genus 1 with a marked point. "
                "Their study unifies number theory, complex analysis, and algebraic geometry. "
                "Central to the proof of Fermat's Last Theorem and modern cryptography."
            ),
            "authors": ["Karl Weierstrass", "Andrew Wiles", "Jean-Pierre Serre"],
            "citation_count": 11000,
            "importance_score": 0.96,
            "proven": True,
            "downstream_theorems": 220,
            "cross_domain_influence": ["Algebraic Geometry", "Algebra", "Cryptography"],
        },
        {
            "concept_id": "C077",
            "name": "Modular Forms",
            "domain": "Number Theory",
            "concept_type": "functor",
            "year_introduced": 1829,
            "abstract": (
                "Complex analytic functions on the upper half-plane invariant under the modular "
                "group. Their L-functions appear in the Langlands program, and their theory "
                "underpins Wiles's proof of Fermat's Last Theorem."
            ),
            "authors": ["Carl Jacobi", "Jean-Pierre Serre", "Andrew Wiles"],
            "citation_count": 10000,
            "importance_score": 0.97,
            "proven": True,
            "downstream_theorems": 195,
            "cross_domain_influence": ["Algebra", "Representation Theory", "Algebraic Geometry"],
        },
        {
            "concept_id": "C078",
            "name": "Galois Theory",
            "domain": "Algebra",
            "concept_type": "theorem",
            "year_introduced": 1832,
            "abstract": (
                "Connects field extensions to group theory through Galois groups. Resolves "
                "the ancient problem of when polynomial equations are solvable by radicals "
                "and provides a foundation for modern algebra."
            ),
            "authors": ["Évariste Galois"],
            "citation_count": 9000,
            "importance_score": 0.96,
            "proven": True,
            "downstream_theorems": 280,
            "cross_domain_influence": ["Number Theory", "Topology", "Logic"],
        },
        {
            "concept_id": "C079",
            "name": "Fourier Analysis",
            "domain": "Functional Analysis",
            "concept_type": "theorem",
            "year_introduced": 1822,
            "abstract": (
                "Decomposing functions into sinusoidal components. The Fourier transform "
                "is a foundational tool in PDEs, signal processing, number theory, and "
                "quantum mechanics."
            ),
            "authors": ["Joseph Fourier"],
            "citation_count": 15000,
            "importance_score": 0.98,
            "proven": True,
            "downstream_theorems": 400,
            "cross_domain_influence": ["PDEs", "Number Theory", "Probability", "Quantum Information"],
        },
        {
            "concept_id": "C080",
            "name": "Cohen Forcing",
            "domain": "Logic",
            "concept_type": "theorem",
            "year_introduced": 1963,
            "abstract": (
                "A method to construct models of set theory in which the continuum hypothesis "
                "fails. Proved the independence of CH from ZFC, showing that some mathematical "
                "questions cannot be resolved by the standard axioms."
            ),
            "authors": ["Paul Cohen"],
            "citation_count": 6000,
            "importance_score": 0.92,
            "proven": True,
            "downstream_theorems": 140,
            "cross_domain_influence": ["Algebra", "Topology", "Combinatorics"],
        },
    ]


def get_relations() -> list[dict]:
    """Return ~120 relations between concepts."""
    return [
        # Riemann Hypothesis connections
        {"source_id": "C001", "target_id": "C004", "relation_type": "motivated_by"},
        {"source_id": "C001", "target_id": "C079", "relation_type": "uses"},
        {"source_id": "C001", "target_id": "C063", "relation_type": "shares_proof_techniques"},
        {"source_id": "C001", "target_id": "C077", "relation_type": "equivalent_to"},
        # Fermat's Last Theorem
        {"source_id": "C002", "target_id": "C076", "relation_type": "depends_on"},
        {"source_id": "C002", "target_id": "C077", "relation_type": "depends_on"},
        {"source_id": "C002", "target_id": "C015", "relation_type": "special_case_of"},
        {"source_id": "C002", "target_id": "C078", "relation_type": "uses"},
        # Goldbach -> Number Theory
        {"source_id": "C003", "target_id": "C004", "relation_type": "motivated_by"},
        {"source_id": "C003", "target_id": "C074", "relation_type": "shares_proof_techniques"},
        # Prime Number Theorem
        {"source_id": "C004", "target_id": "C001", "relation_type": "historically_preceded"},
        {"source_id": "C004", "target_id": "C079", "relation_type": "uses"},
        # BSD Conjecture
        {"source_id": "C005", "target_id": "C076", "relation_type": "motivated_by"},
        {"source_id": "C005", "target_id": "C015", "relation_type": "special_case_of"},
        {"source_id": "C005", "target_id": "C054", "relation_type": "shares_proof_techniques"},
        # P vs NP
        {"source_id": "C006", "target_id": "C018", "relation_type": "motivated_by"},
        {"source_id": "C006", "target_id": "C035", "relation_type": "uses"},
        # Collatz
        {"source_id": "C007", "target_id": "C052", "relation_type": "motivated_by"},
        # Poincaré Conjecture
        {"source_id": "C008", "target_id": "C020", "relation_type": "depends_on"},
        {"source_id": "C008", "target_id": "C059", "relation_type": "special_case_of"},
        {"source_id": "C008", "target_id": "C021", "relation_type": "shares_proof_techniques"},
        # Brouwer Fixed Point
        {"source_id": "C009", "target_id": "C024", "relation_type": "shares_proof_techniques"},
        {"source_id": "C009", "target_id": "C011", "relation_type": "historically_preceded"},
        # Atiyah-Singer
        {"source_id": "C010", "target_id": "C039", "relation_type": "depends_on"},
        {"source_id": "C010", "target_id": "C022", "relation_type": "generalizes"},
        {"source_id": "C010", "target_id": "C021", "relation_type": "uses"},
        {"source_id": "C010", "target_id": "C026", "relation_type": "appears_in_applications"},
        # Persistent Homology
        {"source_id": "C011", "target_id": "C009", "relation_type": "uses"},
        {"source_id": "C011", "target_id": "C044", "relation_type": "shares_proof_techniques"},
        # Hodge Conjecture
        {"source_id": "C012", "target_id": "C038", "relation_type": "uses"},
        {"source_id": "C012", "target_id": "C027", "relation_type": "motivated_by"},
        {"source_id": "C012", "target_id": "C046", "relation_type": "motivated_by"},
        # Classification of Finite Simple Groups
        {"source_id": "C013", "target_id": "C078", "relation_type": "depends_on"},
        {"source_id": "C013", "target_id": "C070", "relation_type": "appears_in_applications"},
        # Grothendieck Schemes
        {"source_id": "C014", "target_id": "C027", "relation_type": "historically_preceded"},
        {"source_id": "C014", "target_id": "C016", "relation_type": "uses"},
        {"source_id": "C014", "target_id": "C038", "relation_type": "historically_preceded"},
        {"source_id": "C014", "target_id": "C046", "relation_type": "historically_preceded"},
        {"source_id": "C014", "target_id": "C072", "relation_type": "historically_preceded"},
        # Langlands Program
        {"source_id": "C015", "target_id": "C002", "relation_type": "generalizes"},
        {"source_id": "C015", "target_id": "C077", "relation_type": "depends_on"},
        {"source_id": "C015", "target_id": "C032", "relation_type": "motivated_by"},
        {"source_id": "C015", "target_id": "C061", "relation_type": "generalizes"},
        {"source_id": "C015", "target_id": "C065", "relation_type": "generalizes"},
        # Yoneda Lemma
        {"source_id": "C016", "target_id": "C017", "relation_type": "historically_preceded"},
        {"source_id": "C016", "target_id": "C069", "relation_type": "historically_preceded"},
        # Higher Category Theory
        {"source_id": "C017", "target_id": "C069", "relation_type": "historically_preceded"},
        {"source_id": "C017", "target_id": "C042", "relation_type": "motivated_by"},
        # Gödel
        {"source_id": "C018", "target_id": "C019", "relation_type": "motivated_by"},
        {"source_id": "C018", "target_id": "C055", "relation_type": "historically_preceded"},
        {"source_id": "C018", "target_id": "C080", "relation_type": "historically_preceded"},
        # ZFC
        {"source_id": "C019", "target_id": "C036", "relation_type": "appears_in_applications"},
        {"source_id": "C019", "target_id": "C080", "relation_type": "historically_preceded"},
        # Ricci Flow
        {"source_id": "C020", "target_id": "C025", "relation_type": "shares_proof_techniques"},
        {"source_id": "C020", "target_id": "C045", "relation_type": "shares_proof_techniques"},
        # Morse Theory
        {"source_id": "C021", "target_id": "C044", "relation_type": "historically_preceded"},
        {"source_id": "C021", "target_id": "C067", "relation_type": "historically_preceded"},
        # Gauss-Bonnet
        {"source_id": "C022", "target_id": "C010", "relation_type": "special_case_of"},
        # Spectral Theorem
        {"source_id": "C023", "target_id": "C024", "relation_type": "uses"},
        {"source_id": "C023", "target_id": "C033", "relation_type": "appears_in_applications"},
        {"source_id": "C023", "target_id": "C079", "relation_type": "uses"},
        # Hahn-Banach
        {"source_id": "C024", "target_id": "C023", "relation_type": "uses"},
        # Navier-Stokes
        {"source_id": "C025", "target_id": "C041", "relation_type": "shares_proof_techniques"},
        {"source_id": "C025", "target_id": "C079", "relation_type": "uses"},
        # Yang-Mills
        {"source_id": "C026", "target_id": "C058", "relation_type": "appears_in_applications"},
        {"source_id": "C026", "target_id": "C048", "relation_type": "motivated_by"},
        # Weil Conjectures
        {"source_id": "C027", "target_id": "C014", "relation_type": "depends_on"},
        {"source_id": "C027", "target_id": "C038", "relation_type": "uses"},
        # Mirror Symmetry
        {"source_id": "C028", "target_id": "C062", "relation_type": "depends_on"},
        {"source_id": "C028", "target_id": "C075", "relation_type": "motivated_by"},
        {"source_id": "C028", "target_id": "C048", "relation_type": "appears_in_applications"},
        # CLT
        {"source_id": "C029", "target_id": "C041", "relation_type": "historically_preceded"},
        {"source_id": "C029", "target_id": "C079", "relation_type": "uses"},
        # Ergodic Theory
        {"source_id": "C030", "target_id": "C074", "relation_type": "appears_in_applications"},
        {"source_id": "C030", "target_id": "C052", "relation_type": "motivates"},
        # Langlands connections
        {"source_id": "C032", "target_id": "C015", "relation_type": "special_case_of"},
        {"source_id": "C032", "target_id": "C066", "relation_type": "uses"},
        # Quantum Error Correction
        {"source_id": "C033", "target_id": "C023", "relation_type": "depends_on"},
        {"source_id": "C033", "target_id": "C078", "relation_type": "uses"},
        # Compressed Sensing
        {"source_id": "C034", "target_id": "C024", "relation_type": "uses"},
        {"source_id": "C034", "target_id": "C079", "relation_type": "uses"},
        # Ramsey Theory
        {"source_id": "C035", "target_id": "C047", "relation_type": "historically_preceded"},
        # K-Theory
        {"source_id": "C039", "target_id": "C014", "relation_type": "motivated_by"},
        {"source_id": "C039", "target_id": "C043", "relation_type": "appears_in_applications"},
        # Stochastic Calculus
        {"source_id": "C041", "target_id": "C029", "relation_type": "extends"},
        {"source_id": "C041", "target_id": "C071", "relation_type": "shares_proof_techniques"},
        # Floer Homology
        {"source_id": "C044", "target_id": "C021", "relation_type": "depends_on"},
        {"source_id": "C044", "target_id": "C067", "relation_type": "depends_on"},
        {"source_id": "C044", "target_id": "C064", "relation_type": "historically_preceded"},
        # Geometric Measure Theory
        {"source_id": "C045", "target_id": "C020", "relation_type": "shares_proof_techniques"},
        {"source_id": "C045", "target_id": "C071", "relation_type": "motivates"},
        # Motivic Cohomology
        {"source_id": "C046", "target_id": "C039", "relation_type": "generalizes"},
        {"source_id": "C046", "target_id": "C014", "relation_type": "depends_on"},
        # Szemerédi
        {"source_id": "C047", "target_id": "C074", "relation_type": "appears_in_applications"},
        # TQFT
        {"source_id": "C048", "target_id": "C017", "relation_type": "uses"},
        {"source_id": "C048", "target_id": "C064", "relation_type": "motivates"},
        # Connes NCG
        {"source_id": "C050", "target_id": "C023", "relation_type": "generalizes"},
        {"source_id": "C050", "target_id": "C001", "relation_type": "appears_in_applications"},
        # Chaos Theory
        {"source_id": "C052", "target_id": "C030", "relation_type": "depends_on"},
        # Random Matrix Theory
        {"source_id": "C063", "target_id": "C001", "relation_type": "shares_proof_techniques"},
        {"source_id": "C063", "target_id": "C023", "relation_type": "uses"},
        {"source_id": "C063", "target_id": "C053", "relation_type": "motivates"},
        # Khovanov Homology
        {"source_id": "C064", "target_id": "C044", "relation_type": "generalizes"},
        {"source_id": "C064", "target_id": "C056", "relation_type": "uses"},
        # Perverse Sheaves
        {"source_id": "C066", "target_id": "C014", "relation_type": "depends_on"},
        {"source_id": "C066", "target_id": "C038", "relation_type": "generalizes"},
        # Symplectic Topology
        {"source_id": "C067", "target_id": "C062", "relation_type": "appears_in_applications"},
        {"source_id": "C067", "target_id": "C028", "relation_type": "motivates"},
        # Infinity Topos
        {"source_id": "C069", "target_id": "C017", "relation_type": "generalizes"},
        {"source_id": "C069", "target_id": "C014", "relation_type": "generalizes"},
        # Monstrous Moonshine
        {"source_id": "C070", "target_id": "C013", "relation_type": "depends_on"},
        {"source_id": "C070", "target_id": "C056", "relation_type": "uses"},
        # Optimal Transport
        {"source_id": "C071", "target_id": "C024", "relation_type": "uses"},
        {"source_id": "C071", "target_id": "C029", "relation_type": "appears_in_applications"},
        # Perfectoid Spaces
        {"source_id": "C072", "target_id": "C014", "relation_type": "generalizes"},
        {"source_id": "C072", "target_id": "C040", "relation_type": "generalizes"},
        {"source_id": "C072", "target_id": "C073", "relation_type": "historically_preceded"},
        # Prismatic Cohomology
        {"source_id": "C073", "target_id": "C072", "relation_type": "depends_on"},
        {"source_id": "C073", "target_id": "C046", "relation_type": "generalizes"},
        # Tao-Green Primes
        {"source_id": "C074", "target_id": "C047", "relation_type": "uses"},
        {"source_id": "C074", "target_id": "C030", "relation_type": "uses"},
        # Fukaya Category
        {"source_id": "C075", "target_id": "C044", "relation_type": "uses"},
        {"source_id": "C075", "target_id": "C028", "relation_type": "appears_in_applications"},
        # Elliptic Curves
        {"source_id": "C076", "target_id": "C077", "relation_type": "depends_on"},
        {"source_id": "C076", "target_id": "C078", "relation_type": "uses"},
        # Modular Forms
        {"source_id": "C077", "target_id": "C079", "relation_type": "uses"},
        {"source_id": "C077", "target_id": "C015", "relation_type": "appears_in_applications"},
        # Galois Theory
        {"source_id": "C078", "target_id": "C013", "relation_type": "historically_preceded"},
        {"source_id": "C078", "target_id": "C015", "relation_type": "appears_in_applications"},
        # Fourier Analysis
        {"source_id": "C079", "target_id": "C023", "relation_type": "uses"},
        {"source_id": "C079", "target_id": "C068", "relation_type": "historically_preceded"},
        # Cohen Forcing
        {"source_id": "C080", "target_id": "C019", "relation_type": "depends_on"},
        {"source_id": "C080", "target_id": "C018", "relation_type": "extends"},
        # Calabi-Yau
        {"source_id": "C062", "target_id": "C022", "relation_type": "generalizes"},
        {"source_id": "C062", "target_id": "C028", "relation_type": "appears_in_applications"},
        # Fukaya and Mirror Symmetry
        {"source_id": "C075", "target_id": "C067", "relation_type": "uses"},
        # Peter-Weyl
        {"source_id": "C031", "target_id": "C079", "relation_type": "uses"},
        {"source_id": "C031", "target_id": "C023", "relation_type": "uses"},
        # Iwasawa Theory
        {"source_id": "C054", "target_id": "C077", "relation_type": "uses"},
        {"source_id": "C054", "target_id": "C076", "relation_type": "appears_in_applications"},
        # Homotopy Type Theory
        {"source_id": "C042", "target_id": "C055", "relation_type": "depends_on"},
        {"source_id": "C042", "target_id": "C017", "relation_type": "motivated_by"},
        # Free Probability
        {"source_id": "C053", "target_id": "C063", "relation_type": "uses"},
        {"source_id": "C053", "target_id": "C050", "relation_type": "shares_proof_techniques"},
        # Donaldson Theory
        {"source_id": "C058", "target_id": "C026", "relation_type": "depends_on"},
        {"source_id": "C058", "target_id": "C044", "relation_type": "motivates"},
        # Thurston
        {"source_id": "C059", "target_id": "C020", "relation_type": "depends_on"},
        {"source_id": "C059", "target_id": "C008", "relation_type": "generalizes"},
        # Bourgain Decoupling
        {"source_id": "C068", "target_id": "C079", "relation_type": "extends"},
        {"source_id": "C068", "target_id": "C074", "relation_type": "appears_in_applications"},
        # Minimal Model Program
        {"source_id": "C057", "target_id": "C014", "relation_type": "depends_on"},
        {"source_id": "C057", "target_id": "C062", "relation_type": "uses"},
        # Quantum Groups
        {"source_id": "C056", "target_id": "C078", "relation_type": "generalizes"},
        {"source_id": "C056", "target_id": "C048", "relation_type": "appears_in_applications"},
    ]

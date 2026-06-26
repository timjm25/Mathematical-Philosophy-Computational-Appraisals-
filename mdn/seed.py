"""Seed the database from the mock corpus."""
from __future__ import annotations


def seed(m) -> None:
    from data.mock_corpus import get_concepts, get_relations
    for concept in get_concepts():
        m.add_concept(concept)
    for relation in get_relations():
        m.add_relation(relation)
    m.run_full_analysis()

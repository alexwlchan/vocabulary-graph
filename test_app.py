#!/usr/bin/env python

import networkx as nx
import pytest

from app import get_nodes_within_distance


@pytest.mark.parametrize(
    "node, max_distance, expected_result",
    [
        ("A", 0, {0: set(["A"])}),
        ("A", 1, {0: set(["A"]), 1: set(["B"])}),
        ("A", 2, {0: set(["A"]), 1: set(["B"]), 2: set(["C", "E"])}),
        (
            "A",
            3,
            {0: set(["A"]), 1: set(["B"]), 2: set(["C", "E"]), 3: set(["D", "F", "H"])},
        ),
    ],
)
def test_get_nodes_within_distance(node, max_distance, expected_result):
    #
    #   A - B - C - D
    #       |   |   |
    #       E - F   G
    #       |
    #       H
    #
    G = nx.Graph()

    G.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
    G.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("B", "E"),
            ("C", "F"),
            ("D", "G"),
            ("E", "F"),
            ("E", "H"),
        ]
    )

    assert (
        get_nodes_within_distance(G, node=node, max_distance=max_distance)
        == expected_result
    )

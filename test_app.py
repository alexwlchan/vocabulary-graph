#!/usr/bin/env python

import networkx as nx
import pytest

from app import create_d3_data, get_nodes_within_distance


@pytest.mark.parametrize(
    "node, max_distance, expected_result",
    [
        ("A", 0, {"A": 0}),
        ("A", 1, {"A": 0, "B": 1}),
        ("A", 2, {"A": 0, "B": 1, "C": 2, "E": 2}),
        ("A", 3, {"A": 0, "B": 1, "C": 2, "E": 2, "D": 3, "F": 3, "H": 3}),
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
    graph = nx.Graph()

    graph.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
    graph.add_edges_from(
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
        get_nodes_within_distance(graph, node=node, max_distance=max_distance)
        == expected_result
    )


def test_create_d3_data():
    #
    #   A - B - C - D - E
    #       |   |
    #       F - G
    #       |
    #       H
    #
    graph = nx.Graph()

    graph.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
    graph.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "E"),
            ("B", "F"),
            ("C", "G"),
            ("F", "G"),
            ("F", "H"),
        ]
    )

    included_nodes = get_nodes_within_distance(graph, node="B", max_distance=2)

    d3_data = create_d3_data(graph, included_nodes=included_nodes)

    assert d3_data.keys() == {"nodes", "links"}
    assert sorted(d3_data["nodes"], key=lambda node: node["id"]) == [
        {"id": "A", "distance": 1},
        {"id": "B", "distance": 0},
        {"id": "C", "distance": 1},
        {"id": "D", "distance": 2},
        {"id": "F", "distance": 1},
        {"id": "G", "distance": 2},
        {"id": "H", "distance": 2},
    ]

    assert sorted(
        d3_data["links"], key=lambda node: node["source"] + node["target"]
    ) == [
        {"source": "A", "target": "B", "distance": 0},
        {"source": "B", "target": "C", "distance": 0},
        {"source": "B", "target": "F", "distance": 0},
        {"source": "C", "target": "D", "distance": 1},
        {"source": "C", "target": "G", "distance": 1},
        {"source": "F", "target": "G", "distance": 1},
        {"source": "F", "target": "H", "distance": 1},
    ]

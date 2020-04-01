#!/usr/bin/env python

from functools import reduce
from operator import or_

import networkx as nx

G = nx.Graph()

G.add_node("口")
G.add_node("吃饭")
G.add_node("喝")
G.add_node("咬")
G.add_node("喵")
G.add_node("猫")
G.add_node("狗")
G.add_node("渴")

G.add_edge("口", "吃饭")
G.add_edge("口", "喝")
G.add_edge("口", "咬")
G.add_edge("口", "喵")
G.add_edge("猫", "喵")
G.add_edge("猫", "狗")
G.add_edge("喝", "渴")

def get_nodes_within_distance(G, *, node, max_distance=2):
    """
    Get the nodes within a given distance of the selected node.

    e.g. if ``max_distance`` is 2, it would find all nodes that are at most
    two steps away from ``node``.
    """
    seen = set(node)
    result = {0: set(node)}

    for dist in range(1, max_distance + 1):
        new_neighbours = reduce(or_, [
            set(G.neighbors(node)) for node in result[dist - 1]
        ]) - seen

        seen |= new_neighbours
        result[dist] = new_neighbours

    return result

from pprint import pprint

pprint(get_nodes_within_distance(G, node="口"))

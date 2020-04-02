#!/usr/bin/env python

import json

import networkx as nx
from graph_logic import create_d3_data, get_nodes_within_distance

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


included_phrases = get_nodes_within_distance(G, node="猫", max_distance=2)

print(json.dumps(create_d3_data(G, included_nodes=included_phrases), indent=2))

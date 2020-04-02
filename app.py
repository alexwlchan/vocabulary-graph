#!/usr/bin/env python

import json
import random

from flask import Flask, redirect, render_template, request, url_for
import markdown
import networkx as nx
import pinyin

from graph_logic import create_d3_data, get_nodes_within_distance

G = nx.Graph()

G.add_node("口", meaning="mouth")
G.add_node("吃饭", meaning="to eat food")
G.add_node("喝", meaning="to drink")
G.add_node("咬", meaning="to bite")
G.add_node("喵", meaning="to meow, like a cat")
G.add_node("猫", meaning="cat")
G.add_node("狗", meaning="dog")
G.add_node("渴", meaning="thirsty")
G.add_node("你好", meaning="hello")
G.add_node("您好", meaning="hello, but polite you")
G.add_node("高兴", meaning="happy")
G.add_node("早", meaning="sunrise")
G.add_node("旦", meaning="early morning")
G.add_node("日", meaning="sun")
G.add_node("日本", meaning="Japan")

G.add_edge("口", "吃饭", note="Look at the 口 radical")
G.add_edge("口", "喝")
G.add_edge("口", "咬")
G.add_edge("口", "喵")
G.add_edge("猫", "喵")
G.add_edge("猫", "狗", note="Notice the matching radical!")
G.add_edge("喝", "渴")
G.add_edge("你好", "您好")
G.add_edge("早", "旦")
G.add_edge("早", "日")
G.add_edge("日", "旦")
G.add_edge("日", "日本")


included_phrases = get_nodes_within_distance(G, node="猫", max_distance=2)

# print(json.dumps(create_d3_data(G, included_nodes=included_phrases), indent=2))

app = Flask(__name__)


@app.template_filter("markdownify")
def markdownify(s):
    return markdown.markdown(s)


@app.route("/")
def index():
    selected_phrases = random.sample(G.nodes.items(), 5)

    selected_graph_nodes = {}

    for phrase, _ in selected_phrases:
        local_neighborhood = get_nodes_within_distance(
            G, node=phrase, max_distance=2
        )

        for phrase, distance in local_neighborhood.items():
            selected_graph_nodes[phrase] = min(
                [distance, selected_graph_nodes.get(phrase, float("inf"))]
            )

    for phrase, metadata in selected_phrases:
        metadata["pinyin"] = pinyin.get(phrase, delimiter=" ")

    return render_template(
        "index.html",
        phrases=selected_phrases,
        d3_data=create_d3_data(G, included_nodes=selected_graph_nodes)
    )


@app.route("/every_phrase")
def every_phrase():
    return render_template(
        "every_phrase.html",
        phrases=sorted(G.nodes.items()),
        d3_data=create_d3_data(G, included_nodes={node: 2 for node in G.nodes})
    )


@app.route("/phrase")
def phrase_detail():
    phrase = request.args["chars"]
    try:
        phrase_data = G.nodes[phrase]
    except KeyError:
        abort(404)

    phrase_data["pinyin"] = pinyin.get(phrase, delimiter=" ")

    local_neighborhood = get_nodes_within_distance(
        G, node=phrase, max_distance=2
    )

    related_phrases = {}

    related_edges = {}
    for edge in G.edges:
        if phrase in edge:
            other_char = next(c for c in edge if c != phrase)
            related_edges[other_char] = G.edges[edge]

    for neighbor_phrase, distance in local_neighborhood.items():
        if distance == 1:
            related_phrases[neighbor_phrase] = {
                "phrase": G.nodes[neighbor_phrase],
                "link": related_edges[neighbor_phrase]
            }

    return render_template(
        "phrase_detail.html",
        phrase_chars=phrase,
        phrase_data=phrase_data,
        related_phrases=related_phrases,
        d3_data=create_d3_data(G, included_nodes=local_neighborhood)
    )


@app.route("/shuffle")
def shuffle():
    phrase_chars = random.choice(list(G.nodes))
    return redirect(url_for("phrase_detail", chars=phrase_chars), code=302)


app.run(debug=True)

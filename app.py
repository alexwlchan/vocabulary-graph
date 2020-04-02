#!/usr/bin/env python

import random

from flask import abort, Flask, redirect, render_template, request, url_for
import markdown
import pinyin

from graph_logic import create_d3_data, get_nodes_within_distance
from phrase_graph import ChinesePhraseGraph

chinese_phrase_graph = ChinesePhraseGraph(path="phrases_zh.json")


app = Flask(__name__)


@app.template_filter("markdownify")
def markdownify(s):
    return markdown.markdown(s)


@app.route("/")
def index():
    selected_phrases = random.sample(
        chinese_phrase_graph.nodes().items(), min(5, len(chinese_phrase_graph.nodes()))
    )

    selected_graph_nodes = {}

    for phrase, _ in selected_phrases:
        local_neighborhood = get_nodes_within_distance(
            chinese_phrase_graph, node=phrase, max_distance=2
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
        d3_data=create_d3_data(
            chinese_phrase_graph, included_nodes=selected_graph_nodes
        ),
    )


@app.route("/every_phrase")
def every_phrase():
    for phrase, metadata in chinese_phrase_graph.nodes.items():
        metadata["pinyin"] = pinyin.get(phrase, delimiter=" ")

    return render_template(
        "every_phrase.html",
        phrases=sorted(chinese_phrase_graph.nodes.items()),
        d3_data=create_d3_data(
            chinese_phrase_graph,
            included_nodes={node: 1 for node in chinese_phrase_graph.nodes()},
        ),
    )


@app.route("/phrase")
def phrase_detail():
    phrase = request.args["chars"]
    try:
        phrase_data = chinese_phrase_graph.nodes()[phrase]
    except KeyError:
        abort(404)

    phrase_data["pinyin"] = pinyin.get(phrase, delimiter=" ")

    local_neighborhood = get_nodes_within_distance(
        chinese_phrase_graph, node=phrase, max_distance=2
    )

    related_phrases = {}

    related_edges = {}
    for edge in chinese_phrase_graph.edges():
        if phrase in edge:
            other_char = next(c for c in edge if c != phrase)
            related_edges[other_char] = chinese_phrase_graph.edges()[edge]

    for neighbor_phrase, distance in local_neighborhood.items():
        if distance == 1:
            related_phrases[neighbor_phrase] = {
                "phrase": chinese_phrase_graph.nodes[neighbor_phrase],
                "link": related_edges[neighbor_phrase],
            }

    return render_template(
        "phrase_detail.html",
        phrase_chars=phrase,
        phrase_data=phrase_data,
        related_phrases=related_phrases,
        d3_data=create_d3_data(chinese_phrase_graph, included_nodes=local_neighborhood),
    )


@app.route("/shuffle")
def shuffle():
    phrase_chars = random.choice(list(chinese_phrase_graph.nodes()))
    return redirect(url_for("phrase_detail", chars=phrase_chars), code=302)


if __name__ == "__main__":
    app.run(debug=True)

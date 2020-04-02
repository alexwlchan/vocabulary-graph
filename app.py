#!/usr/bin/env python

import functools
from functools import reduce
from operator import or_

import networkx as nx
from networkx.readwrite import json_graph

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


@functools.lru_cache()
def get_nodes_within_distance(graph, *, node, max_distance=2):
    """
    Get the nodes within a given distance of the selected node.

    e.g. if ``max_distance`` is 2, it would find all nodes that are at most
    two steps away from ``node``.
    """
    # Distance 0 from the target node is only the node itself.
    seen = set(node)
    result = {0: set(node)}

    for dist in range(max_distance):
        # Find all the direct neighbours of anything that's ``dist``
        # from the central node, and which we haven't seen before.
        new_neighbours = reduce(or_, [
            set(graph.neighbors(node)) for node in result[dist]
        ]) - seen

        # Anything that's one away from ``dist`` is ``dist + 1`` away
        # from the central node.
        result[dist + 1] = new_neighbours
        seen |= new_neighbours

    return result


def write_html(f_name):
    result = '''<script src="http://d3js.org/d3.v2.min.js?2.9.3"></script>
<style>
.link {
  stroke: #aaa;
}
.node text {
stroke:#333;
cursos:pointer;
}
.node circle{
stroke:#fff;
stroke-width:3px;
fill:#555;
}
</style>
<body>
<script>
var width = 300,
    height = 250
var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);
var force = d3.layout.force()
    .gravity(.1)
    .distance(100)
    .charge(-100)
    .size([width, height]);
'''
    result += 'd3.json("' + f_name + '", function(json) {'
    result += '''force
      .nodes(json.nodes)
      .links(json.links)
      .start();
  var link = svg.selectAll(".link")
      .data(json.links)
    .enter().append("line")
      .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.weight); });
  var node = svg.selectAll(".node")
      .data(json.nodes)
    .enter().append("g")
      .attr("class", "node")
      .call(force.drag);
  node.append("circle")
      .attr("r","5");
  node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(function(d) { return d.name });
  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
});
</script>
'''
    return result



from pprint import pprint

# pprint(get_nodes_within_distance(G, node="口"))

print(write_html("data.json"))

# print(json_graph.node_link_data(G))







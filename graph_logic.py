def get_nodes_within_distance(graph, *, node, max_distance):
    """
    Get the nodes within a given distance of the selected node.

    Returns a map (node -> distance), e.g. for the graph

        A - B - C - D
        |
        E

    if you looked up nodes that were distance 2 from "A", it would return

        {
            "A": 0,
            "B": 1, "E": 1,
            "C": 2
        }

    """
    # The only node at distance 0 from the target node is the target itself.
    result = {node: 0}

    for search_dist in range(max_distance):
        # Find all the direct neighbours of anything that's ``search_dist``
        # from the central node.
        nodes_at_search_dist = [
            node for node, node_dist in result.items() if node_dist == search_dist
        ]

        for node in nodes_at_search_dist:
            for new_neighbor in graph.neighbors(node):
                # Anything that's one away from ``search_dist`` is ``search_dist + 1``
                # away from the central node.
                if new_neighbor not in result:
                    result[new_neighbor] = search_dist + 1

    return result


def create_d3_data(graph, *, included_nodes):
    result = {"nodes": [], "links": []}

    # A node in the d3 graph is annotated with:
    #
    #   -   an ``id`` (identifies the node, and the text to display)
    #   -   a ``distance`` (how far is this from the centre?)
    #
    result["nodes"] = [
        {"id": node, "distance": distance} for node, distance in included_nodes.items()
    ]

    # A link in the d3 graph is annoted with:
    #
    #   -   ``source`` and ``target`` (the start/end points, although the
    #       displayed graph is not directed)
    #   -   ``distance`` (how far is this from the centre?)
    #
    for node_1, node_2 in graph.edges:
        try:
            link = {
                "source": node_1,
                "target": node_2,
                "distance": min([included_nodes[node_1], included_nodes[node_2]]),
            }
        except KeyError:
            pass
        else:
            result["links"].append(link)

    return result

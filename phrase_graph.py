import json
import os

import attr
from networkx.readwrite import json_graph
import pinyin


@attr.s
class PhraseGraph:
    path = attr.ib()
    _last_updated = attr.ib(default=None, repr=False, init=False)
    _graph = attr.ib(default=None, repr=False, init=False)

    def _read(self):
        try:
            data = json.load(open(self.path))
        except FileNotFoundError:
            data = {
                "directed": False,
                "graph": {},
                "links": [],
                "nodes": []
            }

        return json_graph.node_link_graph(data)

    def graph(self):
        if (
            self._last_updated is None or
            os.stat(self.path).st_mtime > self._last_updated
        ):
            try:
                self._last_updated = os.stat(self.path).st_mtime
            except FileNotFoundError:
                pass

            self._graph = self._read()

        return self._graph

    def _write(self, graph):
        json_string = json.dumps(
            json_graph.node_link_data(graph), indent=2, sort_keys=True
        )

        with open(self.path, "w") as out_file:
            out_file.write(json_string)

    def add_phrase(self, phrase, **kwargs):
        g = self.graph()
        g.add_node(phrase, **kwargs)
        self._write(g)

    def connect_phrases(self, phrase1, phrase2, **kwargs):
        g = self.graph()
        g.add_edge(phrase1, phrase2, **kwargs)
        self._write(g)


class ChinesePhraseGraph(PhraseGraph):
    def add_phrase(self, phrase, **kwargs):
        print(kwargs)
        kwargs.setdefault("pinyin", pinyin.get(phrase, delimiter=" "))
        return super().add_phrase(phrase, **kwargs)

    def connect_phrases(self, phrase1, phrase2, **kwargs):
        g = self.graph()

        # Add the new nodes manually, so they pick up the pinyin.
        for p in (phrase1, phrase2):
            if p not in g.nodes:
                self.add_phrase(p)

        return super().connect_phrases(phrase1, phrase2, **kwargs)

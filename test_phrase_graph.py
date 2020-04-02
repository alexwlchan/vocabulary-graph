import networkx as nx
import pytest

from phrase_graph import ChinesePhraseGraph, PhraseGraph


@pytest.fixture
def path(tmpdir):
    return tmpdir / "phrase_graph.json"


def test_default_phrase_graph_is_empty(path):
    graph = PhraseGraph(path).graph()

    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


def test_can_serialise_graph_to_json(path):
    phrase_graph = PhraseGraph(path)

    phrase_graph.add_phrase("graf")
    phrase_graph.add_phrase("teorija")
    phrase_graph.connect_phrases("graf", "teorija")

    assert path.exists()
    new_graph = PhraseGraph(path)

    assert phrase_graph.nodes == new_graph.nodes
    assert phrase_graph.edges == new_graph.edges


def test_loads_changes_from_disk(path):
    phrase_graph1 = PhraseGraph(path)
    phrase_graph2 = PhraseGraph(path)

    assert len(phrase_graph1.nodes) == 0
    assert len(phrase_graph2.nodes) == 0

    phrase_graph1.add_phrase("vozlišče")

    assert len(phrase_graph2.nodes) == 1


def test_only_reads_from_disk_when_file_changes(path):
    read_counter = [0]

    class CountingGraph(PhraseGraph):
        def _read(self):
            read_counter[0] += 1
            return super()._read()

    phrase_graph = CountingGraph(path)
    phrase_graph.add_phrase("brati")

    # One read to look up the contents of the graph before adding ``brati``.
    assert read_counter == [1]

    for _ in range(5):
        phrase_graph.graph()

    # A second read to look up the contents of the graph after adding
    # the new phrase.
    assert read_counter == [2]


def test_chinese_phrase_graph_adds_pinyin(path):
    phrase_graph = ChinesePhraseGraph(path)

    phrase_graph.add_phrase(phrase="你")
    assert phrase_graph.nodes["你"] == {"pinyin": "nǐ"}


def test_chinese_phrase_graph_does_not_overwrite_pinyin(path):
    phrase_graph = ChinesePhraseGraph(path)

    phrase_graph.add_phrase(phrase="什么", pinyin="shén me")
    assert phrase_graph.nodes["什么"] == {"pinyin": "shén me"}


def test_adds_pinyin_for_new_edges(path):
    phrase_graph = ChinesePhraseGraph(path)

    phrase_graph.add_phrase("弟弟")
    phrase_graph.connect_phrases(phrase1="弟弟", phrase2="哥哥", note="brothers")

    assert phrase_graph.nodes["哥哥"] == {"pinyin": "gē gē"}

    assert phrase_graph.edges[("弟弟", "哥哥")] == {"note": "brothers"}

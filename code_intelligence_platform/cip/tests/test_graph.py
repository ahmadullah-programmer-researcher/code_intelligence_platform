from cip.graph import find_cycles, strongly_connected_components

def test_detects_cycle():
    graph = {"a": ["b"], "b": ["c"], "c": ["a"], "d": []}
    assert ["a", "b", "c"] in find_cycles(graph)

def test_components_include_isolated_vertices():
    assert ["z"] in strongly_connected_components({"a": ["b"], "b": [], "z": []})

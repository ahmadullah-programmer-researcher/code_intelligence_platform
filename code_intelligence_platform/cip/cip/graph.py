"""Dependency graph utilities, including Tarjan strongly connected components."""
from collections import defaultdict

def strongly_connected_components(graph: dict[str, list[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    result: list[list[str]] = []

    def visit(v: str):
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v); on_stack.add(v)
        for w in graph.get(v, []):
            if w not in indices:
                visit(w); low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            component = []
            while True:
                w = stack.pop(); on_stack.remove(w); component.append(w)
                if w == v: break
            result.append(sorted(component))

    vertices = set(graph)
    for edges in graph.values(): vertices.update(edges)
    for vertex in sorted(vertices):
        if vertex not in indices: visit(vertex)
    return result

def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    return [c for c in strongly_connected_components(graph) if len(c) > 1 or (len(c) == 1 and c[0] in graph.get(c[0], []))]

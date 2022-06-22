from innvariant.networkx.generators import glock_graph


def test_generate_small_glock_graph():
    n_nodes = 5
    G = glock_graph(n_nodes, 2)

    assert G is not None
    assert len(G.nodes) == n_nodes


def test_generate_large_glock_graph():
    n_nodes = 50
    G = glock_graph(n_nodes, 10)

    assert G is not None
    assert len(G.nodes) == n_nodes

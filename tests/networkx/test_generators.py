import matplotlib.pyplot as plt

import networkx as nx

from innvariant.networkx.generators import glock_graph


def test_generate_small_glock_graph():
    G = glock_graph(5, 2)
    nx.draw(G)
    plt.show()


def test_generate_large_glock_graph():
    G = glock_graph(50, 10)
    nx.draw(G)
    plt.show()

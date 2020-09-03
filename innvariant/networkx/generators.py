from math import floor

import networkx as nx


def glock_graph(n: int, r: int):
    """
```bibtex
@inproceedings{riis2006information,
  title={Information flows, graphs and their guessing numbers},
  author={Riis, S{\o}ren},
  booktitle={2006 4th International Symposium on Modeling and Optimization in Mobile, Ad Hoc and Wireless Networks},
  pages={1--9},
  year={2006},
  organization={IEEE}
}
```
    """
    assert n > 1
    assert r <= floor((n - 1) / 2)

    def has_edge(u, v):
        return 0 < (u - v) % n <= r

    G = nx.empty_graph(0, nx.DiGraph)
    G.add_nodes_from(i for i in range(n))
    G.add_edges_from((u, v) for u in range(n) for v in range(n) if has_edge(u, v))

    return G

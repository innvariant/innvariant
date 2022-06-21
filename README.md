# Innvariant Tools  [![PyPI version](https://badge.fury.io/py/innvariant.svg)](https://badge.fury.io/py/innvariant) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/) ![Tests](https://github.com/innvariant/innvariant/workflows/Tests/badge.svg)
Provides some additional functionalities re-used over multiple experiments and tools of our group.


# Install
``poetry install innvariant[all]``


# Caching Tools



# NetworkX Additions
Generate a glock graph (see @[riis2006information]):
```python
from innvariant.networkx.generators import glock_graph

glock_graph(n=5, r=2)  # Glock Graph with guessing number r=2
```


# References

- <a name="ref-riis2006information">[Information flows, graphs and their guessing numbers](https://doi.org/10.37236/962)</a>

[riis2006information]:#ref-riis2006information "Information flows, graphs and their guessing numbers"
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

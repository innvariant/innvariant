# Innvariant Tools [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 3.6](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) ![Tests](https://github.com/innvariant/innvariant/workflows/Tests/badge.svg)
Provides some additional functionalities re-used over multiple experiments and tools of our group.


# Install
``poetry install innvariant[all]``

# NetworkX Additions
Generate a glock graph (see @[riis2006information]):
```python
from innvariant.networkx.generators import glock_graph

glock_graph(n=5, r=2)  # Glock Graph with guessing number r=2
```



# Development
- ``poetry install -E all`` (considering extra variants "all")
- Create wheel files in *dist/*: ``poetry build``
- Install wheel in current environment with pip: ``pip install path/to/pyklopp/dist/pyklopp-0.1.0-py3-none-any.whl``

## Running CI image locally
Install latest *gitlab-runner* (version 12.3 or up):
```bash
# For Debian/Ubuntu/Mint
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash

# For RHEL/CentOS/Fedora
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash

apt-get update
apt-get install gitlab-runner

$ gitlab-runner -v
Version:      12.3.0
```
Execute job *tests*: ``gitlab-runner exec docker test-python3.6``

## Running github action locally
Install *https://github.com/nektos/act*.
Run ``act``

## Running pre-commit checks locally
``poetry run pre-commit run --all-files``


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

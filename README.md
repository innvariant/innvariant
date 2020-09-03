# Innvariant Tools

# Install
``poetry install innvariant[all]``
``poetry install -E all`` (considering extra variants "all")



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

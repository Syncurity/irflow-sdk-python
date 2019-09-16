[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/irflow-client.svg)](https://badge.fury.io/py/irflow-client)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/47bf392599fb4d27931d4d1225e37835)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Syncurity/irflow-sdk-python&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/47bf392599fb4d27931d4d1225e37835)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=Syncurity/irflow-sdk-python&utm_campaign=Badge_Coverage)
[![CircleCI](https://circleci.com/gh/Syncurity/irflow-sdk-python.svg?style=svg&circle-token=19e583ed7083a852759e89dfac9e744a2d854088)](https://circleci.com/gh/Syncurity/irflow-sdk-python)

# irflow-sdk-python

## A python client for Syncurity IR-Flow REST API

logger.info: Python2 support will be removed at the beginning of January 2020.

### Documentation
View our documentation [here](https://syncurity-irflow-sdk-python.readthedocs-hosted.com/en/latest/)

### API Documentation
See the API functions [here](https://syncurity-irflow-sdk-python.readthedocs-hosted.com/en/latest/class.html#class)

### Installation To Use in Production
`pip install irflow_client`


### Upgrade
`pip install irflow_client --upgrade`


### Build from source / install extra packages
Clone the repo:
` git clone git@github.com:Syncurity/irflow-sdk-python.git`  


For running tests:
```bash
1. Clone the repo:

git clone git@github.com:Syncurity/irflow-sdk-python.git 

2. Install all requirements:

cd <project directory>
pip install .
pip install -r requirements-dev.txt

3. Run tests
pytest

4. Run tests with coverage
# With Coverage
cd tests
py.test --cov-report xml --cov-config .coveragerc --cov ../
```

### Contribute
Pull requests are always appreciated

### Support
Please open an issue in github

### Examples
To get started with examples, read the examples README.
It includes two sample python scripts that use the irflow_client.

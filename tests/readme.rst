### To run testing on irflow_client:

Acquire or build the test_data.py file, which includes API Keys and sample data to test against. Place in tests
directory.


Need the following packages:

    pytest-cov
    codacy-coverage

# From the testing directory
    ```cd tests```
    run:
    ```py.test --cov-report xml --cov-config .coveragerc --cov ../```
* To view coverage reports:
    ```coverage report```
# If you are sending this up to codacy for coverage reporting:
    ```export CODACY_PROJECT_TOKEN=<project_token>```
    ```python-codacy-coverage -r coverage.xml```


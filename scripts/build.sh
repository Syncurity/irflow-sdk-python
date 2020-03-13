#!/usr/bin/env bash

cd tests
py.test --cov-report xml --cov-config .coveragerc --cov ../
export CODACY_PROJECT_TOKEN=<somekey>
python-codacy-coverage -r coverage.xml


# build universal wheel and sdist (source)
cd ../
sudo python setup.py bdist_wheel --universal
sudo python setup.py sdist
gpg --detach-sign -a dist/irflow_client-1.4.6.tar.gz

# Sign
sudo gpg --detach-sign -a dist/irflow_client-1.4.6-py2.py3-none-any.whl
gpg --detach-sign -a dist/irflow_client-1.2.3.tar.gz

# upload
twine upload dist/irflow_client-1.2.3.tar.gz dist/irflow_client-1.2.3.tar.gz.asc
twine upload dist/irflow_client-1.2.3-py2.py3-none-any.whl dist/irflow_client-1.2.3-py2.py3-none-any.whl.asc

# Tag Release
echo "Remember to tag this release in Github and release a version"

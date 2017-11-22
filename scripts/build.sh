#!/usr/bin/env bash

# build universal wheel and sdist (source)
sudo python setup.py bdist_wheel --universal
sudo python setup.py sdist
gpg --detach-sign -a dist/irflow_client-1.4.5.tar.gz

# Sign
sudo gpg --detach-sign -a dist/irflow_client-1.4.5-py2.py3-none-any.whl

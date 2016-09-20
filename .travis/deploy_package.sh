#!/usr/bin/env bash

set -x # Print command traces before executing command

set -e # Exit immediately if a simple command exits with a non-zero status.

set -o pipefail # Return value of a pipeline as the value of the last command to
                # exit with a non-zero status, or zero if all commands in the
                # pipeline exit successfully.

PYPIREPO=$1

write_pypirc() {
PYPIRC=~/.pypirc

if [ -e "${PYPIRC}" ]; then
    rm ${PYPIRC}
fi

touch ${PYPIRC}
cat <<pypirc >${PYPIRC}
[distutils]
index-servers =
    pypi

[pypi]
repository: https://pypi.python.org/pypi
username: ${PYPIUSER}
password: ${PYPIPASS}

pypirc

if [ ! -e "${PYPIRC}" ]; then
    echo "ERROR: Unable to write file ~/.pypirc"
    exit 1
fi
}

# write .pypirc file with pypi repository credentials
set +x
write_pypirc
set -x

pip install -U wheel twine

# make bdist universal package
python setup.py bdist_wheel

# makes source package
python setup.py sdist

# install the package as user
pip install dist/*whl --user

# test if it works
$HOME/./local/bin/generatemc --version
$HOME/./local/bin/generatemc --help

# uninstall
pip uninstall -y mcpartools

# install the package as root
pip install dist/*whl

# test if it works
generatemc --version
generatemc --help

# upload only if tag present
if [[ $TRAVIS_TAG != "" ]]; then
    twine upload -r $PYPIREPO dist/*
fi

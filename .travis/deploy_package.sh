#!/usr/bin/env bash

set -x # Print command traces before executing command

set -e # Exit immediately if a simple command exits with a non-zero status.

set -o pipefail # Return value of a pipeline as the value of the last command to
                # exit with a non-zero status, or zero if all commands in the
                # pipeline exit successfully.

pip install -U wheel twine

# make bdist universal package
python setup.py bdist_wheel

# makes source package
python setup.py sdist

# install the package
pip install dist/*whl

# test if installed package works
generatemc --version
generatemc --help

# make pyinstaller package
pip install pyinstaller
pyinstaller main.spec
# check if file was generated
ls -al dist
# check if generated command works
./dist/generatemc --version
./dist/generatemc --help

# make nuitka files
./make_single_executable.sh

# prepare for shipment
mkdir -p release_files
cp generatemc.pyz release_files/
cp generatemc release_files/

# cleaning
rm -rf dist
rm -rf build

#!/usr/bin/env bash

set -e

code_home=${0%/*}
venv=${code_home}/../.venv
. ${venv}/bin/activate

python server.py
#!/bin/bash
# Don't run directly, just used by other scripts to setup
# PYTHONPATH

export PYTHONPATH=$(realpath $(dirname $0)/..)

echo $PYTHONPATH
python $1
#!/usr/bin/env bash

if [ ! -d local ]
then
    echo "Creating virtual env in ./local/"
    python -m venv local
    ./local/bin/pip install -r requirements.txt
fi

./local/bin/python -m minimal_server

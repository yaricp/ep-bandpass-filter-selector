#!/bin/bash

cd ../

python3 -m venv .venv

.venv/bin/pip3 install pip --upgrade
.venv/bin/pip3 install poetry

poetry install
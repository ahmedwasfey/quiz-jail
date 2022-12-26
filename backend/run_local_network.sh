#!/bin/bash

export PYTHONPATH=$PWD
export FLASK_APP=main.py
flask run --port 8500

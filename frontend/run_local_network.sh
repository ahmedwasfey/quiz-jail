#!/bin/bash

export PYTHONPATH=$PWD
export FLASK_APP=main.py
flask run --host 0.0.0.0

#!/usr/bin/env bash
""" Count total number of lines of python code for this project """
cat $(ls *.py */*.py */*/*.py */*/*/*.py) | wc -l

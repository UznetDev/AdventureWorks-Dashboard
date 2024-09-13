#!/bin/bash

source ./setup.sh

# Generate Junit results
python3 -m pytest -v --junitxml /tests/junit/mleap_sql.xml -o junit_suite_name=mleap_sql --durations=0 mleap_sql_tests.py

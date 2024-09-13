#!/bin/bash

echo "Cleaning up mleap_sql tests"

hadoop fs -rm /user/root/AdultCensusIncome.csv
rm AdultCensusIncome.csv

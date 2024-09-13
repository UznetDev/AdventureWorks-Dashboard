#!/bin/bash -e

echo "Setting up mleap_sql tests"

export PYSPARK_PYTHON=python3

export EXTENSIBILITY_TEST_SQL_USER=sa
export EXTENSIBILITY_TEST_SQL_PASSWORD=Yukon900

hadoop fs -mkdir -p /user/root
wget https://amldockerdatasets.azureedge.net/AdultCensusIncome.csv
hadoop fs -copyFromLocal AdultCensusIncome.csv /user/root

# Copy java ext jars to mssql-server container in master pod
#kubectl cp -c mssql-server ../jars/mssql_java_lang_extension.jar master-0:/opt/mssql/java/jars/
kubectl cp -c mssql-server ../jars/JavaTestPackage.jar master-0:/opt/mssql/java/jars/
kubectl cp -c mssql-server ../mssql-mleap-app/target/scala-2.11/mssql-mleap-app-assembly-1.0.jar master-0:/opt/mssql/java/jars/

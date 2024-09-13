# Automated Machine Learning using H2O in SQL Server 2019 Big Data Cluster

## Machine Learning using Spark

The new built-in notebooks in Azure Data Studio enable data scientists and data engineers to run Python, R, or Scala code against the cluster. This is a great way to explore the data and build machine learning models. Notebooks facilitate collaboration between teammates working on a shared data set.

This sample uses the automated machine learning capabilities of the third party H2O package running in Spark in a SQL Server 2019 Big Data Cluster to build a machine learning model that predicts powerplant output.

### Instructions

1. From Azure Data Studio, connect to the SQL Server Big Data Cluster endpoint. Information about how you connect from Azure Data Studio can be found [here](https://docs.microsoft.com/en-us/sql/azure-data-studio/sql-server-2019-extension?view=sql-server-ver15).

1. Download and save the notebook file [h2o-automl-powerplant.ipynb](h2o-automl-powerplant.ipynb/) locally.

1. Open the notebook file in Azure Data Studio (right click on the SQL Server big data cluster  server name-> **Manage**-> Open Notebook).

1. Wait for the “Kernel” and the target context (“Attach to”) to be populated. Set the “Kernel” to **PySpark3** and “Attach to” needs to be the IP address of your big data cluster endpoint.

1. Run each cell in the Notebook sequentially using Azure Data Studio. Expect the first cell to take 20 sec to finish. Other cells downloading and installing H2O, downloading data, and performing automated machine learning may take several minutes to finish.

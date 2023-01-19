# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Analyze data with Apache Spark
#
# https://learn.microsoft.com/en-ca/azure/synapse-analytics/spark/apache-spark-data-visualization-tutorial

# %%
import findspark
findspark.init()

from pyspark.sql import SparkSession

# %%
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook-index2mongo") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

# %%
spark

# %%
spark.conf.set("spark.sql.parquet.enableVectorizedReader","false")  

# %% [markdown]
# # Spark SQL

# %%
sdf = spark.read.option("overwriteSchema", "true").parquet('/home/jovyan/work/data/**/*.parquet.zst')

# %%
type(sdf)

# %%
sdf.tail(10)

# %% [markdown]
# # Pandas spark flavor

# %%
import pyspark.pandas as ps

# %%
psdf = ps.read_parquet('/home/jovyan/work/data/**/*.parquet.zst', index_col="productID")

# %%
type(psdf)

# %%
psdf.tail(10)

# %%

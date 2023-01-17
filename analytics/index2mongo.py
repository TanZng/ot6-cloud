# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import findspark
findspark.init()

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import os
os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"

# %%
# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook-index2mongo") \
        .config("spark.driver.memory", "512m") \
        .config("spark.mongodb.input.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.2') \
        .getOrCreate()

#         .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/test.myCollection") \
#         .config("spark.mongodb.read.connection.uri", "mongodb://mongodb:27017/test.myCollection") \
#         .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.5') \

spark

# %% [markdown]
# # Write data in MongoDB

# %%
df = spark.read.parquet('/home/jovyan/work/data/**/*.parquet.zst')
df

# %%
df.write.format("mongo").mode("append").save()
df.printSchema()

# %% [markdown]
# # Read data in MongoDB

# %%
df = spark.read.format("mongo").load()
df.printSchema()

# %%
df.select("productName").show()

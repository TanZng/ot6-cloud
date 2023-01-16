# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077").appName("jupyter-notebook").config("spark.driver.memory", "512m").getOrCreate()
sc = spark.sparkContext

# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(1000+1))
rdd.sum()
print("hello")
# 5050
# -


# # WOW
# Nose
#

spark.stop()
print("wow")

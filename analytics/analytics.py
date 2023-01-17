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

# %%
# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook") \
        .config("spark.driver.memory", "512m") \
        .config("spark.mongodb.input.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.2') \
        .getOrCreate()

#         .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/test.myCollection") \
#         .config("spark.mongodb.read.connection.uri", "mongodb://mongodb:27017/test.myCollection") \
#         .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.5') \

spark


# %%
sc = spark.sparkContext
sc

# %%
# Sum of the first 100 whole numbers
from pyspark.rdd import RDD

rdd = sc.parallelize(range(1000+1))
rdd.sum()

# %% [markdown]
# # Mongo Spark Connector
# Example
#

# %%
people = spark.createDataFrame([("Bilbo Baggins",  50), ("Gandalf", 1000), ("Thorin", 195), ("Balin", 178), ("Kili", 77),
   ("Dwalin", 169), ("Oin", 167), ("Gloin", 158), ("Fili", 82), ("Bombur", 50)], schema='name string, age int')

people.write.format("mongo").mode("append").save()
# people.write.format("mongodb").mode("append").save()

# If you need to write to a different MongoDB collection, use the .option() 
# method with .write().
# To write to a collection called contacts in a database called people, 
# specify the collection and database with .option():
# OLD: people.write.format("mongodb").mode("append").option("database","people").option("collection", "contacts").save()
# people.write.format("mongo").mode("append").option("database", "people").option("collection", "contacts").save()
people.show()

# %%
people.show()

# %%
people.printSchema()

# %%
# df = spark.read.format("mongodb").load()
df = spark.read.format("mongo").load()
df.printSchema()
# df = spark.read.format("mongo").option("uri", "mongodb://127.0.0.1/people.contacts").load()

# %%
pipeline = "{'$match': {'name': 'Gloin'}}"
df = spark.read.format("mongo").option("pipeline", pipeline).load()
df.show()



# %%
spark.stop()

# %%

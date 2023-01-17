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

# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook") \
        .config("spark.driver.memory", "512m") \
        .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config("spark.mongodb.read.connection.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.5') \
        .getOrCreate()
spark


# %%
sc = spark.sparkContext
sc

# %%
# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(1000+1))
rdd.sum()

# %% [markdown]
# # WOW
# Nose
#

# %%
people = spark.createDataFrame([("Bilbo Baggins",  50), ("Gandalf", 1000), ("Thorin", 195), ("Balin", 178), ("Kili", 77),
   ("Dwalin", 169), ("Oin", 167), ("Gloin", 158), ("Fili", 82), ("Bombur", 50)], schema='name string, age int')

people.write.format("mongodb").mode("append").save()

# If you need to write to a different MongoDB collection, use the .option() 
# method with .write().
# To write to a collection called contacts in a database called people, 
# specify the collection and database with .option():
# people.write.format("mongodb").mode("append").option("database","people").option("collection", "contacts").save()

people.show()

# %%
people.show()

# %%
people.printSchema()

# %%
df = spark.read.format("mongodb").load()
df.printSchema()

# %%
df.show()
# dt = spark.read.format("mongodb").load()
# x = df.filter(df['age'] >= 10)
# print(x.show(vertical=False))



# %%
spark.stop()

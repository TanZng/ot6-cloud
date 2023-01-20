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
from pyspark.sql.types import StringType
import pyspark.pandas as ps
import glob
import os

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"

# %%
# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook-index2mongo") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

spark

# %%
spark.conf.set("spark.sql.parquet.enableVectorizedReader","false")  

# %%
df = ps.read_parquet('/home/jovyan/work/data/**/*.parquet.zst')

#df = spark.read.option("overwriteSchema", "true").parquet('/home/jovyan/work/data/**/*.parquet.zst')

# %%
type(df)

# %%
df.tail(2)

# %%
df.tail(5)

# %%
# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook-index2mongo") \
        .config("spark.driver.memory", "512m") \
        .config("spark.mongodb.input.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/test.myCollection") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.2') \
        .getOrCreate()

spark

# %%

#pdf = pd.read_parquet('/home/jovyan/work/data/17_12_2022/')

files = glob.glob('/home/jovyan/work/data/**/*.parquet.zst')

# %%
pdf = pd.concat([pd.read_parquet(fp) for fp in files])
len(pdf)

# %%


df = vaex.from_pandas(pdf, copy_index=False) # assuming you don't care about the index, which i think spark also does not have by default
df

# %% [markdown]
# # Write data in MongoDB

# %%
spark.conf.set("spark.sql.parquet.enableVectorizedReader","false")  

# %%
df = spark.read.option("overwriteSchema", "true").parquet('/home/jovyan/work/data/**/*.parquet.zst')
#df = spark.read.option("overwriteSchema", "true").parquet('/home/jovyan/work/data/21_12_2022/2022-12-21.1.131762.parquet.zst')

df

# %%
df.printSchema()

# %%
df.select('productName').collect()

# %%
d2 = df.withColumn("zip_code",df["zip_code"].cast(StringType()))

# %%
d2.printSchema()

# %%
d2.write.format("mongo").mode("overwrite").option("overwriteSchema", "true").save()


# %%
d2.printSchema()

# %% [markdown]
# # Read data in MongoDB

# %%
df = spark.read.format("mongo").load()
df.printSchema()

# %%
df.select("productName").show(5)

# %%
import vaex
vdf = vaex.open('/home/jovyan/work/data/**/*.parquet.zst')
vdf

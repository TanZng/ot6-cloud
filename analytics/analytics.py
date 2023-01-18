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
import pyspark.pandas as ps

# %%
# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook-analytics") \
        .config("spark.driver.memory", "512m") \
        .getOrCreate()
spark.conf.set("spark.sql.parquet.enableVectorizedReader","false")  
spark


# %%
sc = spark.sparkContext
sc

# %%
pdf = ps.read_parquet('/home/jovyan/work/data/**/*.parquet.zst')

# %%
type(pdf)

# %%
df.columns

# %%
pdf["productCategory"].drop_duplicates()

# %%
pdf.iloc[1]

# %% [markdown]
# # Example rdd

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


# %%
# If you need to write to a different MongoDB collection, use the .option() 
# method with .write().
# To write to a collection called contacts in a database called people, 
# specify the collection and database with .option():
# OLD: people.write.format("mongodb").mode("append").option("database","people").option("collection", "contacts").save()
# people.write.format("mongo").mode("append").option("database", "people").option("collection", "contacts").save()
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

# %% [markdown]
# # Analytics

# %%
#df = spark.read.format("mongo").option("pipeline", pipeline).load()
df = spark.read.format("mongo").load()
df.printSchema()

# %%
# get all columnnames in order
df.columns

# %%
rdd = df.rdd

# %%
rdd2 = rdd.sample(False, 0.1, 81)
type(rdd2)

# %%
df2 = rdd2.toDF(df.columns)

# %%
x = df2.select("productCategory").distinct().show()
print(x)

# %%
# maybe faster as rdd

# %% [markdown]
# ## Analysis of out-of-stock products by category

# %%
#unavailableProductsDf = df.filter(df[productIsAvailable].isNull()).count()
categories = df.select("productCategory").distinct().show() # convert to list
dates = df.select("productDate").distinct().show()

# count unavailable products by category and date
for category in categories:
    for date in dates:
        filtered_df = df.filter((df.productCategory == category) & (df.productDate == date))
        #available_count = filtered_df.filter(filtered_df.productIsAvailable == "yes").count()
        unavailable_count = filtered_df.filter(filtered_df.productIsAvailable == "no").count()
        # see if total is always the same
        # include location?
    # each category one color line, x-axis date, y-axis count of unavailable products
    plt.plot(dates, unavailable_count, label = category)

plt.legend()
plt.show()

# %% [markdown]
# ## Analysis of out-of-stock products by departments

# %%
#departments = df.select("zip_code").map

rdd = spark.sparkContext.parallelize(df)
rdd2 = rdd.map(lambda x: "".join(list(x["zip_code"])[:1]))
#df2 = rdd2.toDF(["name","gender","new_salary"]   )
departments = df.select("zip_code").distinct().show()

for element in rdd2.collect():
    print(element)
for department in departments:
    for date in dates:
        # count avaiable and unavailable products
        filtered_df = df.filter((df.zip_code == department) & (df.productDate == date))
        #available_count = filtered_df.filter(filtered_df.productIsAvailable == "yes").count()
        unavailable_count = filtered_df.filter(filtered_df.productIsAvailable == "no").count()
        # see if total is always the same
    # each category one color line, x-axis date, y-axis count of unavailable products
    plt.plot(dates, unavailable_count, label = category)

plt.legend()
plt.show()

# %% [markdown]
# ## Evolution of prices over time and by department

# %%
for department in departments:
    for date in dates:
        filtered_df = df.filter((df.zip_code == department) & (df.productDate == date))
        # average prices over department
        prices = filtered_df.filter
        df.groupBy("zip_code").agg(F.mean('productPrice'), F.count('productPrice')).show()


# %% [markdown]
# ## Market share of customers (based on the brands)

# %%

# %% [markdown]
# ## Market shares by group

# %%

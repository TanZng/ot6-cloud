---
jupyter:
  jupytext:
    formats: ipynb,py
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Spark session & context
spark = SparkSession.builder.master("spark://spark:7077") \
        .appName("jupyter-notebook") \
        .config("spark.driver.memory", "512m") \
        .config("spark.mongodb.input.uri", "mongodb://mongodb:27017/database.collection") \
        .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/database.collection") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.13-10.1.0') \
        .getOrCreate()

sc = spark.sparkContext
```


```python
# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(1000+1))
rdd.sum()
```

# WOW
Nose


```python
people = spark.createDataFrame([("Bilbo Baggins",  50), ("Gandalf", 1000), ("Thorin", 195), ("Balin", 178), ("Kili", 77),
   ("Dwalin", 169), ("Oin", 167), ("Gloin", 158), ("Fili", 82), ("Bombur", None)], ["name", "age"])
people.write.format("mongo").mode("append").save()
people.show()
```


```python
spark.stop()
```

```python

```

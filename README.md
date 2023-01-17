# OT6 Cloud Project

- [Spark 3.3.0](https://spark.apache.org/docs/3.3.0/) 
- [PySpark 3.3.1](https://spark.apache.org/docs/3.3.1/api/python/reference/index.html) 
- [Mongo Spark Connector 3.0.2](https://www.mongodb.com/docs/spark-connector/v3.0/python-api/)
- [MongoDB Connector 3.0.2](https://www.mongodb.com/docs/spark-connector/v3.0/python-api/)
- [PyMongo 4.3.3](https://pymongo.readthedocs.io/en/4.3.3/)

## To run the analytics

Create an .env with these credentials:

```bash
SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXX
ACCESS_KEY_ID=XXXXXXXXXX
```

Run
```bash
docker compose up --scale spark-worker=3
```

Open http://localhost:8888/notebooks/work/data/analytics.ipynb

Stop using
```bash
docker compose down -v --remove-orphans
```


### Cluster overview

| Application     | URL                                      | Description                                                          |
| --------------- | ---------------------------------------- | -------------------------------------------------------------------- |
| JupyterNotebook | [localhost:8888](http://localhost:8888/) | Jupyter notebooks                                                    |
| Web UI          | [localhost:4040](http://localhost:4040/) | To monitor the status and resource consumption of your Spark cluster |
| Spark Master    | [localhost:8080](http://localhost:8080/) | Spark Driver                                                         |
| Spark Worker I  |                                          | Spark Worker node                                                    |
| Spark Worker II |                                          | Spark Worker node                                                    |


## To run the spider
Create a virtual env

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

```bash
pip -r requirements.txt
```

Create an .env file in ``./project/project/`` folder with these credentials:

```bash
SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXX
ACCESS_KEY_ID=XXXXXXXXXX
```

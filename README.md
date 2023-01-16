# OT6 Cloud Project

## To run the analytics

Create an .env with these credentials:

```bash
SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXX
ACCESS_KEY_ID=XXXXXXXXXX
```

Run
```bash
docker compose up -d
```

Open http://localhost:8888/notebooks/work/data/analytics.ipynb

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

FROM jupyter/pyspark-notebook:python-3.8

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["jupyter","notebook", "--ip","0.0.0.0","--port", "8888","--no-browser","--NotebookApp.token=''"]

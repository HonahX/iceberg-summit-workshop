FROM jupyter/all-spark-notebook:spark-3.5.0

RUN pip install "pyiceberg[s3fs,hive,pyarrow,sql-sqlite,pandas,duckdb,glue]==0.9.0"

COPY .pyiceberg.yaml /home/jovyan/.pyiceberg.yaml

WORKDIR /home/jovyan/notebooks


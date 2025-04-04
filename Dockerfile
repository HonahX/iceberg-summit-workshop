FROM jupyter/all-spark-notebook:spark-3.5.0

RUN pip install pyiceberg==0.9.0 pyarrow==19.0.1 pandas==2.0.3

COPY .pyiceberg.yaml /home/jovyan/.pyiceberg.yaml

WORKDIR /home/jovyan/notebooks

RUN mkdir -p /home/jovyan/data \
    && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet -o /home/jovyan/data/yellow_tripdata_2024-01.parquet \
    && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet -o /home/jovyan/data/yellow_tripdata_2024-02.parquet \
    && curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet -o /home/jovyan/data/yellow_tripdata_2024-03.parquet


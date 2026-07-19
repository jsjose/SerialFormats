FROM jupyter/pyspark-notebook:spark-3.5.0

USER root

# Configuración de Spark para Delta Lake + Qbeast
COPY spark-defaults.conf ${SPARK_HOME}/conf/spark-defaults.conf

# Cliente Python de Delta Lake (API DeltaTable) y requests para descargar el dataset
RUN pip install --no-cache-dir delta-spark==3.1.0 requests

USER ${NB_UID}

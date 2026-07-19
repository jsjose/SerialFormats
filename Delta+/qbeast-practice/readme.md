# Qbeast sobre Delta Lake

Entorno aislado para explorar [Qbeast](https://docs.qbeast.io/qbeast-spark/latest/getting-started), un formato de indexación multidimensional (O-Tree) que se apoya en **Delta Lake**, no en Iceberg.

## Por qué un entorno separado

Qbeast no se integra con catálogos Iceberg/Nessie: requiere que `spark.sql.catalog.spark_catalog` sea `QbeastCatalog` (una extensión del catálogo de Delta). Por eso no puede convivir en el mismo Spark session que el benchmark de `Iceberg/dremio-file-ingestion-practice`, que usa Nessie como catálogo Iceberg. Este directorio monta un Spark/Jupyter independiente, sin Nessie/MinIO, para no mezclar ambos mundos.

## Versiones

Fijadas según `project/Dependencies.scala` de la release [v0.7.1](https://github.com/Qbeast-io/qbeast-spark/blob/v0.7.1/project/Dependencies.scala) de qbeast-spark:

- Spark 3.5.x (imagen base `jupyter/pyspark-notebook:spark-3.5.0`)
- Delta Lake 3.1.0
- qbeast-spark 0.7.1
- Hadoop 3.3.4

## Uso

```bash
docker compose up --build
```

Jupyter queda disponible en http://localhost:8888 (sin token). El notebook `01_Qbeast_Delta_Exploracion.ipynb` en `notebooks/`:

1. Descarga el dataset NYC Yellow Taxi (enero 2024) a disco local dentro del contenedor (Spark no puede leer `https://` directamente sin un conector httpfs).
2. Escribe una tabla Delta "plana" como referencia.
3. Escribe la misma tabla con Qbeast, indexando columnas clave (`columnsToIndex`).
4. Compara el plan de una query filtrada (`explain`) y los ficheros leídos entre ambas tablas.
5. Inspecciona el índice de Qbeast con la API `QbeastTable` (revisiones, métricas del índice).

Las tablas se persisten en `./warehouse`, montado como volumen.

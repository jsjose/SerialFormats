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

Jupyter queda disponible en <http://localhost:8888> (sin token). El notebook `01_Qbeast_Delta_Exploracion.ipynb` en `notebooks/`:

1. Descarga el dataset NYC Yellow Taxi (enero 2024) a disco local dentro del contenedor (Spark no puede leer `https://` directamente sin un conector httpfs).
2. Escribe una tabla Delta "plana" como referencia.
3. Escribe la misma tabla con Qbeast, indexando columnas clave (`columnsToIndex`).
4. Compara el plan de una query filtrada (`explain`) y los ficheros leídos entre ambas tablas.
5. Inspecciona el índice de Qbeast con la API `QbeastTable` (revisiones, métricas del índice).

Las tablas se persisten en `./warehouse`, montado como volumen.

## Resultados obtenidos

**Conclusión:** con qbeast-spark 0.7.1 (la versión estable más reciente, sobre Spark 3.5.0 + Delta 3.1.0, exactamente la combinación que el propio proyecto declara compatible) **no se observó ningún data-skipping real**, ni por filtros de predicado ni mediante su función insignia de sampling estadístico. Todo apunta a una regresión del propio qbeast-spark entre versiones, no a un problema de configuración de este entorno ni del dataset elegido.

### Pruebas realizadas

Se probó en 8 configuraciones distintas antes de concluir, todas con el mismo resultado (0% de ficheros descartados):

| # | Prueba | Resultado |
| --- | --- | --- |
| 1 | NYC Taxi, 2,79M filas, filtros exactos (punto categórico, rango selectivo, rango multidimensional) | Siempre 100% de ficheros leídos |
| 2 | Lectura vía catálogo (`saveAsTable` + `QbeastCatalog`) en vez de por ruta | Mismo resultado |
| 3 | Solo `QbeastSparkSessionExtension` (sin `DeltaSparkSessionExtension` duplicada) | Mismo resultado |
| 4 | `.sample(0.05)` — la función insignia de Qbeast | `PushedFilters: []` en el plan físico; sigue leyendo el 100% |
| 5 | Tras ejecutar `qbeastTable.optimize()` | Sin cambios en las métricas del índice ni en el pruning |
| 6 | NYC Taxi ampliado a 6 meses reales, 18.094.251 filas | Un filtro que solo 6 filas cumplen sigue leyendo el 100% (52/52 ficheros) |
| 7 | Reproducción exacta del [demo oficial de Qbeast](https://github.com/Qbeast-io/qbeast-spark/blob/main/docs/sample_pushdown_demo.ipynb) (TPC-DS `store_sales`, mismo dataset, misma receta de indexado) sobre 0.7.1 | 100% de ficheros leídos (5/5) |

### La prueba más concluyente

El propio README de qbeast-spark demuestra su beneficio (`.sample(0.1)`) usando la tabla `store_sales` de TPC-DS (`s3a://qbeast-public-datasets/store_sales`, indexado por `ss_cdemo_sk, ss_hdemo_sk`, `cubeSize=300000`), pero con una pila mucho más antigua: **qbeast-spark 0.2.0 + delta-core 1.0.0 + Spark 3.1.1**.

| | Su demo oficial (0.2.0) | Réplica exacta en este entorno (0.7.1) |
| --- | --- | --- |
| Ficheros totales | 21 | 5 |
| Ficheros leídos en `.sample(0.1)` | **1** | **5 (el 100%)** |

Con el mismo dataset y la misma receta de indexado, la versión antigua sí muestra el skipping prometido; la versión estable actual no. Esto descarta tanto el dataset (NYC Taxi) como la configuración de este entorno como causa — apunta a una regresión real en qbeast-spark entre esas versiones.

### Recomendación

Si el objetivo es *data skipping* fiable hoy mismo, **Iceberg con Z-Order** (ya montado y funcionando en `Iceberg/dremio-file-ingestion-practice`) es la vía con resultados demostrados. Antes de invertir más tiempo en Qbeast, valdría la pena abrir un issue en su GitHub usando la reproducción del punto 7 como caso mínimo, o probar explícitamente con una pila antigua (0.2.0/Delta 1.0.0/Spark 3.1.1) para confirmar en qué versión se introdujo la regresión.

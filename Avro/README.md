# Apache Avro

Este directorio contiene pruebas de concepto utilizando [Apache Avro](https://avro.apache.org/), un sistema de serialización de datos que se basa en esquemas JSON.

## Contenido

* `schema.avsc`: Archivo JSON que define el esquema de los datos. Avro requiere que los esquemas estén definidos al momento de escribir y leer los datos.
* `AvroExample.py`: Script en Python (3.11.9) que demuestra cómo serializar y deserializar datos utilizando el esquema definido.
* `test.avro`: Archivo binario de salida generado por el script.

## Características principales evaluadas

* Compresión de datos.
* Evolución de esquemas (Schema Evolution).
* Integración nativa con Python.

# Exploración de Formatos de Datos y Protocolos de Serialización

Este repositorio contiene pruebas de concepto (PoCs), ejemplos y entornos de evaluación para diferentes formatos de almacenamiento de datos, protocolos de serialización y arquitecturas de Data Lakehouse.

## 🛠️ Requisitos Previos

* **Python:** 3.11.9 (utilizado para scripts y pruebas locales).
* **Docker y Docker Compose:** Para levantar las arquitecturas complejas (ej. Data Lakehouse con Iceberg/Dremio).

## 📁 Estructura del Proyecto

A continuación se detallan los formatos y protocolos explorados en este repositorio. Cada directorio contiene su propio `README.md` con instrucciones detalladas.

### 1. Avro

Ejemplos de serialización de datos usando Apache Avro en Python (`AvroExample.py`, `schema.avsc`). Incluye esquemas y generación de ficheros binarios.

### 2. gRPC

Implementaciones de comunicación RPC de alto rendimiento.

* **Recursos:** Introducción a gRPC
* **Ejemplos:** `helloworld`, `route_guide`.

### 3. Parquet

Exploración del formato de almacenamiento columnar Apache Parquet.

* **Recursos:** Tutorial y Buenas Prácticas

### 4. Delta Lake

Pruebas con Delta Lake, formato de almacenamiento que aporta transacciones ACID a Apache Spark.

* **Recursos:**
  * Apache Spark via Homebrew
  * Delta Lake Quickstart
  * Introducción con PySpark

### 5. Apache Iceberg

Implementaciones de arquitecturas Data Lakehouse utilizando el formato de tabla abierta Apache Iceberg.

* Contiene entornos completos dockerizados (ej. integración con Dremio, Nessie, Kafka y Spark).
* **Recursos:**
  * Iceberg Spark Quickstart
  * PyIceberg Documentación
  * Leyendo Iceberg con Python
  * Arquitectura Local Dremio/Nessie/Iceberg
  
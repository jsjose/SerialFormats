# gRPC (Google Remote Procedure Call)

Este directorio explora gRPC, un framework RPC universal de alto rendimiento desarrollado por Google. Utiliza Protocol Buffers (protobuf) por defecto como lenguaje de definición de interfaz (IDL) y formato de intercambio de mensajes subyacente.

## Contenido / Ejemplos

* **helloworld:** Implementación básica de cliente/servidor gRPC demostrando una llamada Unary RPC simple.
* **route_guide:** Ejemplo más avanzado que explora los diferentes tipos de streaming en gRPC (Server streaming, Client streaming y Bidirectional streaming).

## Referencias

* Introducción oficial a gRPC

## Notas

Estos ejemplos requieren la compilación previa de los archivos `.proto` para generar el código base (stubs) en Python.

# Ejemplo de entrada — prompt-chaining-design

## Solicitud del usuario

> Tengo que auditar la calidad de un repositorio con 80 archivos Python y producir un
> único reporte que liste los hallazgos por archivo y las 5 deudas técnicas más graves
> a nivel de repo. Diséñame la cadena: un pase local que analice cada archivo por
> separado y un pase de integración que solo lea los resúmenes y tolere archivos que
> fallen el parseo.

## Inputs requeridos presentes

- **Lote de unidades**: 80 archivos Python del repositorio. [DOC]
- **Unidad atómica**: un archivo `.py`. Cada archivo es analizable de forma
  independiente. [DOC]
- **Objetivo del pase de integración**: producir un reporte con hallazgos por archivo +
  las 5 deudas técnicas más graves a nivel de repo. [DOC]

## Señales de activación

- Volumen alto (80 unidades) que no cabe con calidad en una sola ventana de atención.
- Unidades independientes que solo se integran al final (map → reduce).
- Requisito explícito de tolerar fallos por unidad (parseo) sin abortar el lote.

## Restricciones declaradas

- El pase de integración debe leer **solo resúmenes**, nunca el código crudo.
- Un archivo que falle el parseo no debe tumbar la auditoría completa.

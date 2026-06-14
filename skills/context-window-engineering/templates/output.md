# Plan de ensamblado de ventana de contexto — <agente>

> Entregable de la skill context-window-engineering. Cada afirmación lleva tag de evidencia.

## 1. Inputs

- Proveedor y soporte de prefix caching: <proveedor> — <sí/no> [DOC/SUPUESTO]
- Límite de ventana objetivo: <N tokens> [DOC]
- Tasa de crecimiento del historial: <descripción> [INFERENCIA]
- Señal de qué cambia por-turno: <timestamp / contadores / último mensaje / ids> [DOC]

## 2. Partición estático vs dinámico

| Bloque | Contenido | ¿Cambia por-turno? | ¿Regla crítica? | Destino |
|---|---|---|---|---|
| role | rol + herramientas | no | — | prefijo |
| policies | reglas críticas | no | sí | prefijo (borde inicial) |
| schema | esquema de salida | no | — | prefijo |
| few-shot | ejemplos | no | — | prefijo |
| history | historial | sí (crece) | — | zona compactable |
| reminder | hora + estado + reafirmación | sí | sí (reafirmada) | cola dinámica (borde final) |

## 3. Orden del prefijo (byte-idéntico)

1. <bloque> 2. <bloque> 3. <bloque>
Normalización de whitespace: <regla>. Auditoría `grep timestamp|now|request_id|uuid|counter` en prefijo: <limpio/hallazgos>. [CÓDIGO]

## 4. Ubicación del estado volátil

Todo valor por-turno vive en el bloque `<reminder>` final: <lista>. Ninguno en el prefijo. [DOC]

## 5. Edge placement de reglas críticas

- Borde inicial (prefijo): <reglas>.
- Borde final (reafirmadas, solo irrenunciables): <reglas>.
- En el centro: ninguna regla crítica. [DOC]

## 6. Política de compactación

- Umbral: <>55% u otro> — justificación: <...>. [CONFIG]
- Algoritmo: resumir historial intermedio; bordes intactos. [DOC]
- Compactar vs truncar: <decisión + trade-off>. [INFERENCIA]

## 7. Plan de medición

- Cache-hit rate: <método, valor esperado/medido>. [DOC]
- Prueba de retención: <escenario de contexto largo, resultado>. [DOC]

## 8. Decisiones y trade-offs

- <decisión> → <trade-off>. [INFERENCIA]

## 9. Reporte del compilador determinístico

`compile-context-window.py <contexto.json>` → prefijo / zona compactable / cola dinámica / reglas críticas / validaciones. Rechazos detectados: <ninguno/lista>. [SUPUESTO]

## 10. Veredicto del gate

- [ ] Prefijo byte-idéntico sin valor por-turno
- [ ] Estado dinámico en `<reminder>` final
- [ ] Reglas críticas en ambos bordes
- [ ] Umbral de compactación explícito que no toca bordes
- [ ] Cache-hit rate y retención medidos

Resultado: **PASA / RECHAZA** — <evidencia>.

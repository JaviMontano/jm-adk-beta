<!-- distilled from alfa skills/katas-false-positive-criteria -->
<!-- Criterios categoricos con ejemplos positivos y negativos por severidad para reducir falsos positivos; disable temporal por categoria. -->
# Katas False Positive Criteria

Kata 30 · Criterios Explícitos para Reducir Falsos Positivos. Escenarios canónicos: Customer Support, CI/CD, Structured Extraction.

## Qué es

Las instrucciones vagas ("be conservative", "only high-confidence", "reporta findings de alta confianza") fallan porque el modelo las interpreta distinto en cada turno: no hay umbral estable detrás de esas palabras. [INFERENCIA] La alternativa que funciona: criterios categóricos con ejemplos positivos y negativos por nivel de severidad, que producen clasificación consistente turno tras turno. [DOC] Punto clave del kata: un FP rate alto en UNA categoría destruye la confianza en TODAS, así que conviene deshabilitarla temporalmente mientras se afina, en vez de tolerar ruido. [DOC]

## Por qué importa (falla que evita)

Si el reviewer reporta "potential security issue" sobre código seguro 1 de cada 5 veces, los devs terminan ignorando TODOS los flags de seguridad, incluso los reales. [INFERENCIA] La precisión es prerrequisito de la utilidad: un clasificador ruidoso no es débil, es inservible, porque la confianza es cross-categoría y se erosiona globalmente con cualquier categoría ruidosa. [DOC]

## Modelo mental

- "confidence" como filtro no funciona: el modelo está mal calibrado y un mismo caso recibe scores distintos entre corridas. [INFERENCIA]
- Criterios categóricos en vez de adjetivos: "reporta solo cuando el comentario claim X pero el código hace Y", no "reporta inconsistencias". [DOC]
- Severidad declarada con ejemplos de código positivo y negativo por cada criterio (qué SÍ dispara, qué NO). [DOC]
- Se mide FP rate POR CATEGORÍA, nunca el agregado: el agregado esconde la categoría tóxica. [DOC]
- Si una categoría arrastra FPs, se deshabilita temporalmente mientras se afina; así se preserva la confianza global cross-categoría. [DOC]

## Patrón correcto

```text
SYSTEM_EXPLICIT = """
Reporta findings SOLO si cumplen UNO de estos criterios:
- security.hardcoded_secret: literal API key en código.
    Positivo: OPENAI_KEY='sk-abc...'
    Negativo: OPENAI_KEY=os.environ['OPENAI_KEY']
- bug.null_deref: dereferencia un value sin chequeo cuando puede ser None.
NO reportes: estilo, patterns 'que podrían ser problemáticos'.
Severidad: error (rompe runtime), warning (degrada edge case).
"""
```

## Anti-patrón

```text
SYSTEM_VAGUE = "Eres reviewer. Reporta findings de alta confianza. Sé conservador con los flags."
# interpretado distinto cada turno: 'conservador' y 'alta confianza' no tienen umbral estable.
```

## Supuestos y límites (anti-scope)

- Asume un set de categorías nombradas y mutuamente distinguibles; categorías que se solapan vuelven a introducir ambigüedad de turno. [SUPUESTO] Verificar: pedir al autor un criterio Positivo/Negativo por categoría antes de medir.
- Reduce FPs por criterio mal definido; NO corrige FPs por código de entrada ambiguo ni por bug del propio modelo de base. [INFERENCIA]
- No cubre falsos NEGATIVOS (findings reales omitidos): criterios muy estrechos suben precisión a costa de recall. La decisión precision/recall queda fuera de este kata. [DOC]
- Disable temporal es mitigación, no fix: una categoría deshabilitada deja de detectar; reactivar es obligatorio, no opcional. [INFERENCIA]

## Edge cases y failure modes

- Criterio con ejemplo Positivo pero sin Negativo: el modelo sobre-dispara en los bordes. Siempre par P/N. [INFERENCIA]
- Una sola categoría con FP alto y agregado "aceptable": el promedio enmascara la tóxica → medir siempre por categoría. [DOC]
- Categoría deshabilitada y nunca reactivada: pérdida silenciosa de cobertura. Registrar fecha de disable y dueño de re-enable. [SUPUESTO] Verificar con un TODO/issue trazable.
- Severidad sin definición operativa ("error" vs "warning" a criterio del modelo): vuelve a ser un adjetivo vago. Anclar severidad a efecto observable (rompe runtime vs degrada edge case). [DOC]
- Ejemplos Negativos que en realidad SÍ son issues: envenenan el criterio y suprimen findings reales. Revisar ejemplos como código, no como prosa. [INFERENCIA]

## Ejemplo trabajado (disable → afinar → reactivar)

1. Medición: `null_deref` FP=22%, resto <5%. El agregado (8%) ocultaba la tóxica. [INFERENCIA]
2. Disable temporal de `null_deref`; confianza cross-categoría se recupera para las demás. [DOC]
3. Afinar: añadir Negativo (`x` ya validado con guard antes del deref) al criterio.
4. Reactivar y re-medir sobre el mismo set fijo; aceptar solo si FP<5% sin caída de recall. [SUPUESTO] Verificar con set de regresión etiquetado.

## Argumento de certificación

- Reescribir prompts vagos en criterios categóricos con ejemplos positivos y negativos por severidad.
- Medir FP rate POR CATEGORÍA, no agregada.
- Usar disable temporal de categorías problemáticas para preservar la confianza cross-categoría.
- Argumentar por qué "confidence" como filtro no funciona (modelo mal calibrado).

## Acceptance criteria

- Cada categoría tiene criterio accionable + ejemplo Positivo y Negativo de código. [DOC]
- Severidad anclada a efecto observable, no a adjetivo. [DOC]
- FP rate reportado POR categoría sobre un set fijo, nunca solo el agregado. [DOC]
- Toda categoría deshabilitada tiene dueño y condición de reactivación registrados. [SUPUESTO] Verificar: issue/TODO trazable.

## Cuándo activar

- Reescribir un prompt de clasificación/review que usa lenguaje vago de confianza.
- Diagnosticar por qué los devs ignoran los flags de un reviewer automático.
- Diseñar criterios de severidad con ejemplos para extracción estructurada o pipelines CI/CD.
- Decidir qué hacer con una categoría que dispara demasiados falsos positivos.

## Skills relacionadas

- `katas-provenance-preservation`
- `katas-multipass-prompt-chaining`
- `katas-context-dilution-mitigation`

<!-- distilled from alfa skills/katas-fewshot-edge-calibration -->
<!-- Few-shot para calibrar bordes subjetivos con 2-4 ejemplos del mismo schema; complementa, no reemplaza, al schema. -->
# Katas Fewshot Edge Calibration

> Kata 14 · "Few-Shot para Calibrar Bordes" · escenario base: Structured Extraction.

## Qué es

Cuando la tarea es subjetiva (tono, formato no estándar, juicio estético), una descripción zero-shot deja al modelo en su default genérico. [INFERENCIA] Entre 2 y 4 ejemplos `input/output` desplazan su distribución hacia el formato deseado más rápido y barato que un párrafo de instrucciones. [DOC] Few-shot es la forma más eficiente de comunicar ground truth para casos sin definición rígida, y se compone con schema (Kata 5). [DOC]

## Por qué importa (falla que evita)

Decir "responde en estilo casual chileno" o "clasifica usando criterio profesional" no produce el resultado deseado: el modelo interpreta la prosa abstracta distinto cada vez. [INFERENCIA] Mostrar 3 ejemplos de cómo se ve el output sí lo produce. La prosa vaga genera salidas inconsistentes turno a turno; los ejemplos fijan el ground truth observable. [DOC] El fallo es silencioso: cada llamada parece razonable en aislamiento, pero la varianza solo aparece al comparar muchas salidas contra una rúbrica fija. [INFERENCIA]

## Modelo mental

- Los ejemplos son del **mismo schema** que la salida esperada. [DOC]
- Cubren los **bordes del dominio**, no el caso fácil del centro. [DOC]
- 2 a 4 suelen bastar; más de 5 dispersa atención (Kata 11) y rompe caches (Kata 10) sin mejorar calidad. [INFERENCIA]
- Few-shot **complementa, no reemplaza**, al schema: el schema impone forma, los ejemplos calibran juicio. [DOC]
- Si few-shot contradice el schema, **gana el schema** (restricción sintáctica dura): re-escribir los ejemplos para alinearlos. [INFERENCIA]
- Ejemplos al inicio = parte estática del prompt: maximiza prefix cache (Kata 10) y queda en el borde de atención alta (Kata 11). [INFERENCIA]
- Los ejemplos son **enseñables**: si un revisor humano no puede etiquetar el output con la misma clase, el ejemplo no comunica nada. [SUPUESTO]

## Supuestos y límites (anti-scope)

- Aplica a juicio subjetivo o formato no estándar; para tareas con definición rígida, el schema solo (Kata 5) basta y los ejemplos son overhead. [INFERENCIA]
- NO sustituye validación determinística: few-shot reduce la varianza del juicio, no garantiza schema válido — la salida sigue requiriendo parseo/validación dura. [INFERENCIA]
- NO escala como base de conocimiento: si el dominio necesita decenas de casos, es retrieval (RAG), no few-shot; >5 ejemplos diluye atención sin ganancia. [SUPUESTO] Medir calidad a 2/3/4/5 ejemplos antes de añadir más.
- Los ejemplos consumen tokens en CADA llamada: en prompts ya largos o de alto volumen, el coste fijo puede superar el de instrucciones precisas. [SUPUESTO]
- Sesgo de los ejemplos: el modelo copia patrones espurios (longitud, orden, vocabulario) además del criterio. Variar superficie, fijar criterio. [INFERENCIA]

## Patrón correcto

```python
prompt = (
    "Clasifica el ticket. Ejemplos:\n"
    "ticket:'no me llega la factura desde hace 3 meses' clase:'billing',urgencia:'high'\n"
    "ticket:'tengo una sugerencia para la app' clase:'feedback',urgencia:'low'\n"
    "ticket:'no puedo entrar, token expirado' clase:'auth',urgencia:'high'\n"
    "ahora clasifica:\n"
    "ticket:'{user_text}'"
)
```

Los tres ejemplos cubren bordes distintos (billing/high, feedback/low, auth/high) y van al inicio como bloque estático. [CÓDIGO] El bloque de ejemplos es invariante entre llamadas; solo `{user_text}` cambia, así que entra entero en prefix cache. [INFERENCIA]

## Anti-patrón

```python
prompt = (
    "Clasifica usando criterio profesional, considerando urgencia, dominio, "
    "impacto, severidad operacional, prioridad SLA y política interna."
)
```

Párrafo abstracto sin ejemplos: el modelo lo interpreta de forma distinta en cada llamada y no converge al formato esperado. [INFERENCIA] Apilar más adjetivos ("profesional", "severidad", "SLA") no reduce la ambigüedad; un solo ejemplo observable comunica más que seis criterios en prosa. [INFERENCIA]

```python
# Anti-patrón 2: tres ejemplos, todos del centro fácil
"ticket:'no funciona el login' clase:'auth',urgencia:'high'\n"
"ticket:'error al iniciar sesión' clase:'auth',urgencia:'high'\n"
"ticket:'no puedo loguearme' clase:'auth',urgencia:'high'\n"
```

Ejemplos redundantes del mismo borde: gastan tokens y atención sin enseñar los límites donde el modelo realmente duda (billing vs feedback, low vs high). [INFERENCIA]

## Modos de falla (qué vigilar)

- **Contradicción ejemplo↔schema**: un ejemplo emite un campo que el schema prohíbe; el modelo intenta complacer ambos y produce salida inválida. Gana el schema: reescribir el ejemplo. [INFERENCIA]
- **Sesgo de recencia/orden**: el modelo sobre-pesa el último ejemplo. Si las clases están desbalanceadas en orden, baraja o equilibra la secuencia. [SUPUESTO]
- **Fuga de patrón espurio**: todos los ejemplos `high` son largos y los `low` cortos; el modelo clasifica por longitud, no por contenido. Romper la correlación superficie↔etiqueta. [INFERENCIA]
- **Deriva de cache**: editar un ejemplo invalida el prefix cache desde ese punto (Kata 10); versiona el bloque de ejemplos como una unidad estable. [INFERENCIA]
- **Sobre-ajuste a 5+ ejemplos**: añadir ejemplos "por si acaso" diluye atención (Kata 11) y encarece sin subir calidad medida. [SUPUESTO]

## Casos límite

- Clases mutuamente excluyentes en un mismo ticket (auth + billing): incluye un ejemplo que muestre la regla de desempate, no dejes que el modelo la invente. [INFERENCIA]
- Idioma/registro mixto: si la entrada real mezcla español/inglés, al menos un ejemplo debe reflejarlo o el modelo asume monolingüe. [SUPUESTO]
- Clase rara (<1% del tráfico): un ejemplo del borde raro vale más que tres del común; prioriza cobertura de frontera sobre frecuencia. [INFERENCIA]

## Argumento de certificación

- Identificar cuándo few-shot supera a instrucciones en prosa. [DOC]
- Diseñar ejemplos que cubran **bordes** y no el centro del dominio. [DOC]
- Combinar few-shot con schema (Kata 5) para tareas subjetivas con formato estricto, sin saturar atención. [DOC]
- Justificar por qué 2-4 y no 1 ni 8: cobertura de frontera vs dilución de atención y rotura de cache. [INFERENCIA]

## Criterios de aceptación

- El prompt contiene entre 2 y 4 ejemplos `input/output`, todos en el **mismo schema** que la salida esperada. [DOC]
- Los ejemplos cubren **bordes distintos** del dominio (no duplican la misma clase/severidad). [DOC]
- Ningún ejemplo contradice el schema; ante conflicto, el ejemplo fue reescrito para alinearse. [INFERENCIA]
- El bloque de ejemplos está al **inicio** y es invariante entre llamadas (solo cambia el input dinámico). [INFERENCIA]
- Cada `[SUPUESTO]` de este diseño (nº de ejemplos, orden, idioma) tiene una medición asociada antes de fijarse. [DOC]

## Cuándo activar

- Tarea subjetiva: tono, formato no estándar, juicio estético, clasificación con criterio. [DOC]
- La descripción en prosa no logra el formato deseado de forma consistente. [INFERENCIA]
- Se necesita comunicar ground truth para casos sin definición rígida. [DOC]

## Skills relacionadas

- `katas-schema-tool-extraction` (Kata 5: el schema impone forma)
- `katas-prefix-caching` (Kata 10: ejemplos estáticos al inicio maximizan cache)
- `katas-context-dilution-mitigation` (Kata 11: bordes de atención alta, no saturar con >5 ejemplos)

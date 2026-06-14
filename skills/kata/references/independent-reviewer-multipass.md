<!-- distilled from alfa skills/katas-independent-reviewer-multipass -->
<!-- Multi-pass review con reviewer independiente en sesion limpia; per-file y cross-file; rechazo de quorum N-de-M. -->
# Katas Independent Reviewer Multipass

## Qué es

El modelo que generó código retiene el contexto de su propio razonamiento: por eso es un mal revisor de su propio output. [INFERENCIA] Una instancia independiente —sesión nueva, sin la cadena de generación— ve únicamente el código resultante y detecta más issues reales. [DOC] Para PRs grandes la revisión se descompone en dos pases: **Pass A** de profundidad per-file (un deep dive por archivo) y **Pass B** de integración cross-file (interacciones, duplicados de findings, contratos rotos entre módulos). [DOC]

## Por qué importa (falla que evita)

El self-review produce reviews superficiales o auto-justificativas: el modelo defiende decisiones que tomó momentos antes, da feedback inconsistente y omite bugs obvios porque su atención sigue anclada a la narrativa de generación. [INFERENCIA] Un single-pass sobre 14 archivos dispersa la atención y diluye los hallazgos. [DOC] Y "consensuar 2 de 3 reviews" (quorum N-de-M) parece robusto pero suprime issues raros legítimos: un bug que solo un reviewer detecta se descarta por minoría justo cuando más valor aporta. [INFERENCIA]

## Modelo mental

- **Self-review:** misma sesión, contexto sesgado por la generación, ineficaz para detectar fallos propios. [INFERENCIA]
- **Independent reviewer:** sesión limpia, sin la cadena de generación; ve solo el código resultante. [DOC]
- **Pass A:** per-file deep dive, un archivo a la vez, atención concentrada. [DOC]
- **Pass B:** cross-file integration; opera solo sobre los resúmenes tipados del Pass A, no sobre el código crudo completo. [DOC]
- **Quorum 2-de-3 NO es solución:** filtra issues raros legítimos en lugar de compensar el sesgo de contexto. [INFERENCIA]

## Patrón correcto

```python
def review_pr(client, files):
    # Pass A: cada archivo revisado por una SESIÓN NUEVA e independiente.
    per_file = [
        review_file_independent(client, path, content)
        for path, content in files.items()
    ]
    # Pass B: integración cross-file solo sobre los resúmenes tipados.
    summary = json.dumps(per_file)
    return create(
        system="Detecta interacciones cross-file y duplicados de findings.",
        messages=[summary],
    )

# review_file_independent usa una SESIÓN NUEVA: el reviewer NO vio la generación.
```

Cada `review_file_independent` arranca sin historial de generación; Pass B recibe resúmenes tipados (no el código crudo) para no rediluir la atención que Pass A concentró. [INFERENCIA]

## Anti-patrón

```python
# ANTI: self-review en la misma sesión que generó el código.
resp_gen = create(messages=[{"role": "user", "content": "Genera el módulo X"}])
# ...misma sesión, contexto sesgado...
create(messages=[resp_gen, {"role": "user", "content": "Ahora revisa lo que escribiste"}])

# ANTI: quorum 2-de-3 que descarta señal genuina.
# si solo 1 de 3 reviewers reporta el bug => se descarta (FALSO NEGATIVO)
```

Dos errores: el reviewer hereda la narrativa de generación (no es independiente), y el quorum trata un hallazgo único como ruido cuando suele ser la señal más valiosa. [INFERENCIA]

## Casos límite

- **PR de 1 archivo** → Pass A basta; Pass B no aporta (no hay interacciones cross-file que integrar). [SUPUESTO]
- **Findings duplicados entre archivos** → es trabajo de Pass B deduplicarlos; no los suprimas en Pass A, donde el contexto per-file es incompleto. [DOC]
- **Reviewer "independiente" que recibe el prompt de generación** → deja de ser independiente; la sesión debe arrancar limpia, solo con el código resultante. [DOC]
- **Pass B sobre código crudo completo** → reintroduce dispersión de atención; usa solo los resúmenes tipados del Pass A. [INFERENCIA]
- **Contrato roto entre módulos visible solo en conjunto** → lo detecta Pass B, no Pass A; por eso ningún pase es prescindible en PRs multi-archivo. [INFERENCIA]

## Anti-scope

- No define **cómo** clasificar un finding como falso positivo (ver `katas-false-positive-criteria`). [DOC]
- No cubre el muestreo de qué archivos revisar en PRs masivos (ver `katas-confidence-stratified-sampling`). [DOC]
- No es un mecanismo de consenso: rechaza el quorum, no propone otro esquema de votación. [DOC]
- No reemplaza tests ni análisis estático; es revisión semántica por LLM independiente. [SUPUESTO]

## Criterios de aceptación

- El reviewer arranca en sesión limpia, sin la cadena de generación (independencia verificable). [DOC]
- Pass A y Pass B están separados explícitamente; Pass B consume resúmenes tipados, no código crudo. [DOC]
- Ningún finding se descarta por minoría: el quorum N-de-M queda rechazado con su justificación (filtra señal rara). [INFERENCIA]
- Findings cross-file (contratos rotos, duplicados, interacciones) se atribuyen a Pass B, no a Pass A. [DOC]

## Argumento de certificación

- Enunciar por qué el self-review es subóptimo (contexto sesgado de la generación). [INFERENCIA]
- Separar explícitamente el Pass A (per-file) del Pass B (cross-file integration). [DOC]
- Argumentar contra el quorum N-de-M: filtra señal genuina rara en vez de compensar el sesgo. [INFERENCIA]
- Asegurar sesiones limpias para los reviewers independientes (sin la cadena de generación). [DOC]

## Cuándo activar

- PRs o changesets grandes (varios archivos) que requieren revisión profunda. [DOC]
- Pipelines de CI/CD donde el reviewer debe ser independiente del generador. [DOC]
- Escenarios Code Gen donde el mismo modelo generó y se pediría que revise. [DOC]
- Cuando alguien propone "consensuar varias reviews por mayoría" y hay que rechazar el quorum. [DOC]

## Skills relacionadas

- `katas-multipass-prompt-chaining`
- `katas-false-positive-criteria`
- `katas-confidence-stratified-sampling`

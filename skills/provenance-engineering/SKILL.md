---
name: provenance-engineering
version: 1.1.0
last_updated: 2026-06-11
description: "Disenar pipelines de extraccion/sintesis con provenance tipada: invariante no hay claim sin source, conflictos marcados y escalados a humano, nunca promediados ni resueltos en silencio."
owner: "JM Labs"
triggers:
  - provenance engineering
  - claim source invariant
  - conflict marking
  - typed provenance
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Provenance Engineering

## Capacidad

Disenar e implementar pipelines de extraccion/sintesis donde cada claim transporta su provenance tipada y donde la invariante "no hay claim sin source" es **estructural, no aspiracional**. [DOC] Cubre tres decisiones de ingenieria:

1. Modelar cada afirmacion como objeto con `source[]` obligatorio (id, locator, fecha). [DOC]
2. Detectar y representar conflictos entre fuentes con `conflict=true` conservando **todas** las fuentes, en lugar de promediarlas o elegir una en silencio. [DOC]
3. Escalar los conflictos a revision humana con la fecha visible; nunca resolverlos automaticamente. [DOC]

Resultado: un artefacto auditable donde un humano traza cualquier dato hasta su origen y ve que fuentes lo respaldan o lo contradicen. [INFERENCIA]

## Cuando usarla

- Pipeline que extrae datos de multiples documentos (KYC, due diligence, research multi-fuente) y el output se usa para **decidir, firmar o citar**. [DOC]
- Distintas fuentes pueden contradecirse (dos fechas, dos cifras, dos direcciones) y promediar o elegir una destruye informacion critica. [DOC]
- El consumidor es un humano que necesita auditar el origen de cada dato antes de actuar. [DOC]
- Necesitas un test estructural que **falle el build** si aparece un claim sin source. [DOC]

**No la uses** (anti-scope) cuando el output es prosa exploratoria sin consecuencias de decision, o cuando una sola fuente de verdad es indiscutible y no hay posibilidad de conflicto. [DOC] Forzarla ahi anade ceremonia sin valor de auditoria. [INFERENCIA]

## Inputs / Outputs

**Inputs requeridos** [INFERENCIA]
- Inventario de fuentes: cada `source_id` con su documento, version y fecha (`as_of`).
- Atributos a extraer y, por atributo, su locator dentro de cada fuente (pagina, celda, span).
- Consumidor declarado (quien audita) y la consecuencia de decision.

**Outputs** [INFERENCIA]
- Conjunto de `Claim` tipados con `source[]` no vacio y `as_of`.
- Cola de escalacion con los claims `conflict=true` y sus fuentes en conflicto.
- Render que expone source + fecha + marcador de conflicto junto a cada dato.
- Test estructural que blinda la invariante en CI.

**Vacio critico**: si falta el inventario de fuentes o el locator de un atributo, detente y pide — no inventes un `source_id`. [DOC]

## Como construir

1. **Modela el claim tipado.** Define `Claim` con `value`, `source[]` no vacio y `as_of`. El `source[]` vacio debe ser invalido **por construccion** (tipo, schema o validacion en el constructor), no por convencion. [CÓDIGO]
2. **Captura provenance en extraccion.** Adjunta `source_id`, locator (pagina, span, celda) y fecha del documento. Ningun claim nace sin esos campos. [DOC]
3. **Detecta conflictos al fusionar.** Al consolidar claims del mismo atributo desde varias fuentes, compara valores **normalizados** (trim, casing, formato de fecha/moneda) antes de comparar — diferencias de formato no son conflictos reales. [INFERENCIA] Si los valores normalizados difieren, marca `conflict=true` y conserva todas las fuentes; no colapses a un valor unico. [CÓDIGO]
4. **Escala, no resuelvas.** Enruta los `conflict=true` a una cola humana con ambas fuentes y la fecha visible. El pipeline no decide cual gana. [DOC]
5. **Hazlo visible.** En el render, expon `source_id` y `as_of` junto a cada claim; los conflictos se muestran como tales, no enterrados. [DOC]
6. **Blinda con test estructural.** Test que recorra el output y falle si existe cualquier claim con `source[]` vacio, `source_id` desconocido (fuera del inventario) o conflicto resuelto en silencio. [CÓDIGO]

### Decisiones y trade-offs

- **Conservar ambas fuentes vs elegir una.** Conservar cuesta verbosidad en el render, pero elegir en silencio destruye auditabilidad de forma irreversible — el conflicto desaparece sin rastro. Se prioriza auditabilidad. [INFERENCIA]
- **Escalar vs resolver con heuristica (mas reciente gana).** "Mas reciente" parece razonable pero es una resolucion silenciosa disfrazada: produce un valor que solo una fuente afirma y oculta que hubo desacuerdo. Se escala siempre. [INFERENCIA]
- **Invariante por construccion vs por test.** El test atrapa regresiones; el tipo las previene. Se usan **ambos**: el tipo bloquea el caso comun, el test cubre el output ya serializado. [INFERENCIA]

## Assets y validacion offline

> Bundle determinista materializado en `assets/` (`assets/quality-rubric.json`, `assets/checklist.md`, `assets/README.md`, `assets/manifest.json`): rubrica del guardian y checklist del gate de aceptacion. [CÓDIGO]

> Los assets/scripts siguientes son el contrato deterministico previsto del skill; aun no estan materializados en el repo, por eso van tagueados `[SUPUESTO]`, no `[CÓDIGO]`. [SUPUESTO]

- `assets/provenance-engineering-contract.json` — reportes JSON auditables. [SUPUESTO]
- `assets/claim-source-policy.json` — exige `source_id`, `locator`, `as_of`, `source_type`. [SUPUESTO]
- `assets/conflict-policy.json` — bloquea promedio, primera fuente, fuente mas reciente y cualquier resolucion silenciosa. [SUPUESTO]
- `assets/escalation-policy.json` — exige escalacion humana por conflicto. [SUPUESTO]
- `assets/render-policy.json` — muestra source, fecha y marcador de conflicto. [SUPUESTO]
- `assets/structural-test-policy.json` — convierte la invariante en test offline. [SUPUESTO]

Al producir un reporte JSON de provenance, validalo con:

```bash
bash skills/provenance-engineering/scripts/check.sh   # [SUPUESTO]: script previsto, aun no en repo
```

El validator falla si hay claims sin source, `source_id` desconocidos, conflictos no preservados, conflictos no escalados, fechas ocultas, tests estructurales incompletos o Guardian con pass y validacion falsa. [SUPUESTO]

## Patron correcto

```python
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Source:
    source_id: str
    locator: str   # page 4, cell B7, span 120-138
    as_of: date

@dataclass(frozen=True)
class Claim:
    attribute: str
    value: str
    sources: tuple[Source, ...]
    conflict: bool = False

    def __post_init__(self) -> None:
        if not self.sources:
            raise ValueError(f"claim '{self.attribute}' has no source")  # GOOD: invariante por construccion

def merge(attribute: str, candidates: list[Claim]) -> Claim:
    values = {c.value for c in candidates}          # comparar valores ya normalizados upstream
    all_sources = tuple(s for c in candidates for s in c.sources)
    # GOOD: conflicto preservado con ambas fuentes, nunca promediado ni elegido en silencio
    return Claim(attribute, value=" | ".join(sorted(values)), sources=all_sources,
                 conflict=len(values) > 1)

def assert_provenance(claims: list[Claim], known_ids: set[str]) -> None:
    for c in claims:
        assert c.sources, f"claim '{c.attribute}' lost its source"          # GOOD: test estructural
        for s in c.sources:
            assert s.source_id in known_ids, f"unknown source_id {s.source_id!r}"  # GOOD: rechaza id fuera de inventario
```
<!-- [CÓDIGO]: patron presente en este archivo -->

## Anti-patron

```python
# ANTI: resumen en prosa sin source_id, sin fecha, sin senal de conflicto
def summarize(records: list[dict]) -> str:
    name = records[0]["name"]                                     # ANTI: elige la primera fuente en silencio
    revenue = sum(r["revenue"] for r in records) / len(records)   # ANTI: promedia un conflicto
    return f"{name} reported revenue of {revenue}."               # sin provenance, sin as_of, conflicto borrado
```
<!-- [CÓDIGO]: anti-patron presente en este archivo -->

Esto destruye la auditabilidad: el humano no sabe de donde salio el nombre, el conflicto de cifras quedo promediado en un numero que **ninguna fuente afirma**, y no hay fecha. Un dato asi no sostiene una decision. [INFERENCIA]

### Otros anti-patrones a rechazar [DOC]
- "Mas reciente gana" / "mas confiable gana" como resolucion automatica — es escalacion encubierta.
- Promedio, mediana o concatenacion que pierda la atribucion fuente-por-valor.
- `source[]` poblado con un placeholder ("varias fuentes", "interno") en vez de ids reales.
- Marcar `conflict=true` pero no enrutarlo a la cola humana (conflicto visible pero no accionado).

## Edge cases

- **Mismo valor, fuentes distintas** → no es conflicto; consolida y conserva todas las fuentes como respaldo. [INFERENCIA]
- **Diferencia solo de formato** (USD 4.2M vs 4,200,000) → normaliza antes de comparar; no marques conflicto espurio. [INFERENCIA]
- **Una sola fuente** → claim valido con `source[]` de un elemento; no fuerces conflicto. [INFERENCIA]
- **Fuente sin fecha** → `as_of` es obligatorio; si la fuente no la trae, es vacio critico, no `as_of=None`. [DOC]
- **`source_id` fuera del inventario** → falla duro; un id desconocido es indistinguible de un claim inventado. [DOC]

## Self-correction (detente y corrige si…)

- Estas a punto de devolver un valor unico donde habia desacuerdo → preserva y escala. [INFERENCIA]
- Un claim tiene `source[]` vacio o un placeholder → bloquea el output, no lo emitas. [DOC]
- Vas a normalizar "resolviendo" la fecha o la cifra ganadora → eso es resolucion silenciosa; revierte. [INFERENCIA]
- El render no muestra `as_of` o el marcador de conflicto → no esta listo para un auditor. [INFERENCIA]
- Marcaste conflicto pero no hay item en la cola humana → la invariante de escalacion esta rota. [DOC]

## Gate de aceptacion (checklist de validacion)

El output aprueba solo si **todas** se cumplen: [DOC]

- [ ] Cada claim transporta `source[]` no vacio (id + locator + fecha). 
- [ ] Cada `source_id` existe en el inventario de fuentes declarado.
- [ ] Los conflictos estan marcados con `conflict=true` y conservan **todas** las fuentes.
- [ ] Los conflictos se escalan a humano, no se resuelven ni promedian automaticamente.
- [ ] `as_of` es visible para el humano en el render.
- [ ] Existe un test estructural que falla si aparece un claim sin source, con id desconocido, o un conflicto silenciado.
- [ ] No hay valor agregado (promedio/mediana/concat) que ninguna fuente afirme.

## Katas y skills relacionadas

- Kata 20. [DOC]
- Relacionadas: `katas-provenance-preservation`. [DOC]

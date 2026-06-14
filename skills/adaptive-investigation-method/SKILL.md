---
name: adaptive-investigation-method
version: 1.1.0
description: "Investigar dominios desconocidos (repos, datasets, corpus) con mapeo barato, budget de exploracion acotado y re-plan disciplinado que solo dispara al invalidar una hipotesis."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - adaptive investigation method
  - dynamic decomposition
  - exploration budget
  - disciplined replan
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Adaptive Investigation Method

## Capacidad

Construir agentes que investigan dominios desconocidos (codebases, datasets, documentos) sin quemar el budget de contexto. Combina tres movimientos de ingenieria: **mapeo barato** de la superficie del problema, **priorizacion explicita** de donde invertir, y **deep-dive selectivo** solo en nodos prometedores. El re-plan no es reflejo de cada turno; dispara unicamente cuando una hipotesis queda invalidada por evidencia. Un budget duro (lecturas o tokens) es la cota de seguridad que garantiza terminacion aunque el dominio sea infinito. [DOC]

El artefacto construible es un loop con: (1) scratchpad persistido que separa `plan`, `hypotheses` y `findings`; (2) contador de budget que decrementa por cada lectura cara; (3) regla de re-plan tipada que solo corre ante `hypothesis_invalidated`. [INFERENCIA]

## Cuando usarla

- Un agente debe entender un repo o corpus grande antes de actuar y leerlo todo es inviable.
- El costo de exploracion debe estar acotado por diseno (latencia, tokens, llamadas a tools).
- Quieres evitar re-planificacion en cada turno y loops de duda.
- Necesitas trazabilidad: por que se exploro un area y por que se descarto otra. [INFERENCIA]

**NO la uses cuando** el dominio es pequeno y leerlo entero es mas barato que mapearlo (umbral practico: < ~15 archivos o cabe en una ventana de contexto); ni cuando la tarea es determinista y no requiere descubrimiento; ni cuando ya conoces el nodo objetivo y solo necesitas leerlo. [SUPUESTO]

## Contrato de entrada/salida

| | Campo | Obligatorio | Nota |
|---|---|---|---|
| **In** | `goal` | si | Pregunta concreta a resolver, no "entender el repo". [DOC] |
| **In** | `budget` | si | Entero de lecturas caras o tokens. Sin esto → detener y pedir. [DOC] |
| **In** | `surface_root` | si | Raiz a mapear (path, glob o dataset). [CONFIG] |
| **In** | `cheap_tools` | default | `Glob`/`Grep`/`Bash` de listado. [CONFIG] |
| **Out** | `findings[]` | si | Cada uno con `node` + evidencia + tag de provenance. |
| **Out** | `replans[]` | si | Cada re-plan con la hipotesis invalidada que lo disparo. |
| **Out** | `stop_reason` | si | `budget_exhausted` o `goal_resolved`. |
| **Out** | `deliverable` | si | Sintetizado desde `findings`, nunca desde memoria difusa. |

Si falta `goal` o `budget`, emite `{VACIO_CRITICO}` y pide el dato; no auto-completes el budget. [DOC]

## Como construir

1. **Define el budget duro.** Fija `budget = N` lecturas caras o tokens antes de empezar y persiste el contador en el scratchpad. Sin esto el loop no tiene condicion de paro. [DOC]
2. **Mapea barato.** Usa `Glob`/`Grep` (no lecturas completas) para mapear la superficie: estructura, nombres, entrypoints. Cada item es candidato a deep-dive, no contenido leido. El mapeo NO decrementa budget. [INFERENCIA]
3. **Formula hipotesis priorizadas.** Lista ordenada por valor esperado / costo. Cada hipotesis apunta a los nodos del mapa que la confirmarian o invalidarian. Sin hipotesis no hay deep-dive: leer "lo que parezca interesante" es el anti-patron. [INFERENCIA]
4. **Deep-dive selectivo.** Lee en detalle solo los nodos top-ranked. Cada `Read` decrementa el budget. Registra `findings` con referencia al nodo y un tag de provenance. [DOC]
5. **Re-plan disciplinado.** Tras cada deep-dive: si la evidencia **invalida** la hipotesis activa, re-prioriza la lista. Si la confirma o la deja intacta, continua con el siguiente nodo sin re-planificar. [DOC]
6. **Cierra al agotar budget o resolver el objetivo.** Emite el deliverable desde `findings`. Registra `stop_reason`. [DOC]

### Decisiones y trade-offs

- **Budget duro vs adaptativo.** Elegimos cota dura porque garantiza terminacion y es auditable; el costo es que un dominio mas profundo de lo previsto puede quedar parcialmente mapeado. Mitigacion: el deliverable declara cobertura parcial, no la oculta. [INFERENCIA]
- **Mapeo barato vs leer-todo.** El mapa pierde detalle (solo nombres/estructura) a cambio de cubrir N veces mas superficie por unidad de budget. Justificado cuando la senal de relevancia vive en la estructura (paths, nombres, imports), no en el cuerpo de cada archivo. [INFERENCIA]
- **Re-plan solo-al-invalidar vs cada turno.** Re-planificar siempre maximiza adaptacion pero produce loops de duda y gasta razonamiento; disparar solo ante invalidacion conserva impulso. Trade-off: una hipotesis "casi" refutada sobrevive un turno extra — aceptable frente al costo del thrash. [INFERENCIA]

## Paquete deterministico

Usa el compilador local cuando el loop deba quedar validado antes de entregarse o integrarse en otro agente. [DOC]

```bash
python3 scripts/compile-adaptive-investigation.py --input path/to/investigation.json --format markdown
python3 scripts/compile-adaptive-investigation.py --input path/to/investigation.json --format json --output investigation-report.json
```

El compilador carga: [CÓDIGO]

| Archivo | Proposito |
|---|---|
| `assets/investigation-schema.json` | Campos requeridos: objetivo, budget, mapa, hipotesis, deep-dives, replans, stop condition, deliverable. |
| `assets/investigation-policy.json` | Reglas de budget, tools baratas/caras, triggers de re-plan, motivos de paro, anti-patrones bloqueados. |
| `assets/report-template.md` | Forma estable del reporte Markdown. |

Ejecuta `bash scripts/check.sh` despues de editar esta skill, sus assets o fixtures. El check valida casos positivos y **rechaza** investigaciones sin budget duro o con re-plan reflejo. [CÓDIGO]

## Patron correcto

```python
# GOOD: cheap map -> ranked hypotheses -> selective deep-dive -> disciplined replan
def adaptive_investigate(goal, budget=8):
    scratch = {"plan": [], "hypotheses": rank(initial_hypotheses(goal)), "findings": []}
    surface = cheap_map()  # glob/grep only, no full reads, no budget spent
    while budget > 0 and not goal_resolved(scratch):
        hyp  = scratch["hypotheses"][0]
        node = pick_node(surface, hyp)
        evidence = deep_dive(node)   # one expensive Read
        budget -= 1
        scratch["findings"].append({"node": node, "evidence": evidence})
        if invalidates(evidence, hyp):
            scratch["hypotheses"] = rank(reprioritize(scratch["hypotheses"], evidence))
        # else: keep going, do NOT replan reflexively
        persist(scratch)
    return synthesize(scratch["findings"], stop_reason(budget, scratch))
```

## Anti-patron

```python
# ANTI: rigid upfront plan, read everything, reflexive replan every turn
def naive_investigate(goal):
    plan = make_full_plan_upfront(goal)   # rigid, no adaptation
    data = read_all_files()               # blows the context budget
    for step in plan:
        plan = make_full_plan_upfront(goal)  # reflexive replan -> loop of doubt
        act(step, data)
    return summarize(data)
```

### Anti-scope (no es trabajo de esta skill)

- Ejecutar cambios o escribir codigo en el dominio investigado — esto solo descubre y reporta. [DOC]
- Investigacion exhaustiva / cobertura total: el objetivo es resolver `goal` dentro del budget, no auditar todo. [INFERENCIA]
- Re-mapear en cada turno: el mapa se construye una vez; solo se amplia si una invalidacion abre una region nueva. [INFERENCIA]

## Ejemplo concreto

`goal`: "donde se valida auth en un monorepo de 4000 archivos", `budget=8`. [DOC]

1. **Map** (0 budget): `Glob **/auth*`, `Grep -l "validateToken|requireAuth"` → 11 nodos candidatos.
2. **Rank**: H1 `middleware/auth.ts` (entrypoint, alto valor) > H2 `services/session/*` > H3 tests.
3. **Deep-dive H1** (budget 8→7): exporta `requireAuth`, pero **delega** la validacion real → H1 parcialmente invalidada (no es donde se valida).
4. **Re-plan**: la delegacion apunta a `lib/jwt/verify.ts`; sube al top.
5. **Deep-dive** `lib/jwt/verify.ts` (7→6): contiene la verificacion de firma y expiracion → `goal_resolved`.
6. **Cierra**: `stop_reason=goal_resolved`, deliverable cita los 2 nodos. Budget restante 6 (cobertura eficiente). [INFERENCIA]

## Gate de validacion (acceptance criteria)

Toda investigacion debe satisfacer **todas** estas condiciones para considerarse completa: [DOC]

- ☐ Existe un budget de exploracion duro y un contador que decrementa por lectura cara.
- ☐ El mapeo inicial es barato (`Glob`/`Grep`), sin lecturas completas, y no consume budget.
- ☐ Las hipotesis estan priorizadas por valor/costo **antes** del primer deep-dive.
- ☐ El criterio de re-plan es explicito y solo dispara ante hipotesis invalidada.
- ☐ `plan` y `findings` se persisten en scratchpad tipado (no en prosa difusa).
- ☐ Hay `stop_reason` registrada (budget agotado u objetivo resuelto).
- ☐ Cada finding lleva referencia al nodo y un tag de provenance. [DOC]

## Self-correction (sintomas → accion)

| Sintoma | Diagnostico | Accion |
|---|---|---|
| El loop no termina | Sin budget duro o sin decremento | Detener; instalar contador antes de seguir. [DOC] |
| Re-planificas cada turno | Re-plan reflejo, no tipado | Solo re-prioriza ante `hypothesis_invalidated`. [DOC] |
| Budget cae rapido sin senal | Deep-dives sin hipotesis que los justifique | Vuelve a `rank`; no leas "lo interesante". [INFERENCIA] |
| Mapeo consume budget | Estas leyendo archivos completos en el map | Usa `Glob`/`Grep`; el cuerpo se lee solo en deep-dive. [DOC] |
| Deliverable no rastreable | Sintetizaste desde memoria | Reconstruye desde `findings` con sus nodos. [INFERENCIA] |
| Dos hipotesis empatadas siempre | Ranking sin desempate | Prioriza la mas barata de invalidar (mas informacion/budget). [SUPUESTO] |

## Edge cases

- **Budget=0 o ausente** → `{VACIO_CRITICO}`: detener y pedir, nunca auto-fijar. [DOC]
- **Mapa vacio** (Glob/Grep sin hits) → reportar "sin superficie detectable" y revisar `surface_root`; no empieces deep-dives a ciegas. [INFERENCIA]
- **Todas las hipotesis invalidadas con budget restante** → genera hipotesis nuevas desde los findings acumulados; si no surgen, cierra con `goal_unresolved` honesto. [INFERENCIA]
- **Goal resuelto en el primer deep-dive** → cierra de inmediato; el budget no usado es exito, no desperdicio. [INFERENCIA]
- **Dominio cambia mid-investigation** (archivos editados) → invalida el mapa afectado; ver `session-lifecycle-management` para fork vs fresh. [SUPUESTO]

## Katas y skills relacionadas

- Kata 19 (investigacion adaptativa con budget).
- Skill relacionada: `katas-adaptive-investigation`.
- Complementarias: `provenance-engineering` (trazar cada finding a su fuente), `session-lifecycle-management` (fork vs fresh cuando el mundo cambia). [DOC]

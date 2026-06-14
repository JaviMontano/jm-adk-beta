<!-- distilled from alfa skills/katas-adaptive-investigation -->
<!-- Investigacion adaptativa: mapeo barato, budget de exploracion acotado y re-plan disciplinado solo al invalidar la hipotesis. -->
# Kata 19 · Investigacion Adaptativa (Descomposicion Dinamica)

## Que es

En un dominio desconocido no se planifica al detalle de antemano. El agente mapea la topologia primero (un `glob` barato sobre nombres de archivo, `regex` sobre imports y simbolos), genera un plan priorizado a partir de esa topologia, y re-adapta el plan cuando un hallazgo invalida la hipotesis vigente. Todo el ciclo ocurre dentro de un presupuesto de exploracion acotado: un maximo duro de archivos, queries o minutos.

Escenarios donde aplica: Multi-Agent Orchestration, Dev Productivity, Code Generation.

## Por que importa (falla que evita)

Un plan rigido en territorio desconocido garantiza desperdicio: el agente sigue ramas muertas porque "estaba en el plan", no porque la evidencia las sostenga. La investigacion adaptativa prioriza la atencion sobre lo que la realidad muestra, no sobre lo que la hipotesis inicial asumio. Sin presupuesto, ademas, el agente quema contexto leyendo el repo entero antes de tener una sola pregunta enfocada.

## Supuestos y limites (anti-scope)

- **Supone** un repo/dominio inspeccionable con herramientas locales (`glob`, `regex`, lectura de archivo); no cubre dominios solo accesibles por red, UI o ejecucion.
- **Supone** que el mapeo barato es representativo: nombres, imports y simbolos predicen donde vive la señal. Si el codigo esta ofuscado, generado o sin convencion de nombres, el supuesto cae y hay que priorizar por otra heuristica (p.ej. cobertura de tests o churn de git).
- **No** es para tareas ya especificadas con plan estable y trivial (ver "Cuando activar"): ahi el ciclo adaptativo añade overhead sin valor.
- **No** garantiza completitud: con presupuesto duro, cerrar reportando lo no explorado es el resultado correcto, no un fallo.
- **No** sustituye verificacion: un finding mapeado debe confirmarse en deep-dive antes de tratarse como evidencia.

## Modelo mental

- **Fase 1 - mapeo barato.** Escanear la topologia con `glob` de nombres y `regex` de imports/simbolos. Sin leer cuerpos completos todavia.
- **Fase 2 - priorizacion declarada.** Construir un plan ordenado a partir de la topologia y enunciar por que cada objetivo esta arriba.
- **Fase 3 - deep-dive selectivo.** Leer en profundidad SOLO los objetivos priorizados, nunca todo.
- **Re-planificar SOLO si un hallazgo INVALIDA el plan**, no si solo lo refina. Esto evita loops de re-planificacion reflejos en cada turno.
- **Presupuesto duro.** Maximo de archivos, queries y minutos; cuando se agota, se reporta lo encontrado y lo pendiente.
- **Persistir plan y findings en un scratchpad** (ver `katas-scratchpad-pattern`, Kata 18) para que el estado sobreviva al contexto.

Distincion clave **invalida vs refina** (el gate mas confundido):

| Hallazgo | Efecto en la hipotesis | Accion |
|---|---|---|
| El parser real es ANTLR, no regex casero | la rama "buscar regex" ya no aplica | **re-plan**: invalida |
| El regex esta en `lexer.py`, no en `parser.py` | misma hipotesis, otro archivo | append + reordenar plan, **sin** re-plan |
| El bug no esta donde se creia pero la causa raiz sigue siendo el lexer | hipotesis intacta | deep-dive el siguiente objetivo, **sin** re-plan |

## Patron correcto

```python
topology = scan_repo(globs=['src/**/*.py'])      # Fase 1: barato, sin leer cuerpos
budget = Budget(files=50, queries=20, minutes=15)
plan = prioritize(topology)                        # Fase 2: orden + razon declarada
while plan and budget.remaining():
    target = plan.pop()                            # mayor prioridad primero
    budget.spend(files=1)                          # el presupuesto SIEMPRE decrementa
    finding = deep_dive(target, budget)            # Fase 3: lectura profunda selectiva
    scratchpad.append('Hallazgos', finding)        # persistir antes de decidir
    if finding.invalidates_hypothesis:             # gate estricto, no "refina"
        plan = re_plan(topology, finding)          # re-prioriza sobre la MISMA topologia
# salida deterministica aun si el budget se agota antes de vaciar el plan:
scratchpad.append('Pendientes', plan)              # lo no explorado es parte del reporte
report = emit_report(scratchpad, budget)           # cumple el contrato JSON
```

Edge cases que el loop debe manejar explicitamente:

- **Budget agotado con plan no vacio**: cerrar y reportar `plan` restante como pendiente; nunca silenciar.
- **Topologia vacia** (glob sin matches): no hay nada que priorizar; reportar dominio fuera de alcance del mapeo y pedir otra heuristica, no leer todo.
- **Re-plan en cascada**: si cada finding invalida, se esta re-mapeando mal; cap de re-plans (p.ej. 3) y luego degradar a reporte de incertidumbre.
- **deep_dive que excede budget a mitad**: abortar ese target, registrar parcial, no entrar al siguiente.

## Anti-patron

```python
# Plan rigido upfront: nunca se actualiza con la evidencia
plan = make_full_plan_upfront(repo)
for task in plan:
    do(task)

# o leer todo sin presupuesto
read_all_files()

# o re_plan() en cada turno por reflejo, no por invalidacion
```

## Argumento de certificacion (criterios de aceptacion)

Cada item es verificable contra el reporte o el scratchpad; sin evidencia, no certifica.

- Presupuesto explicito declarado **antes** del mapeo (archivos / queries / minutos) y uso registrado <= limite en todos los ejes.
- Criterio de re-plan enunciado y aplicado: re-plan SOLO con `invalidates_hypothesis=true`; ningun re-plan disparado por un refinamiento (auditable en el log de decisiones).
- Las tres fases son distinguibles en el rastro: mapeo barato precede a cualquier lectura de cuerpo completo (cero `read` antes del primer `glob`/`regex`).
- Conexion con Kata 4 (subagentes para deep-dive paralelo) y Kata 18 (scratchpad como memoria persistente del plan y los findings) presente cuando aplica.
- Reporte compatible con `assets/adaptive-investigation-report-contract.json`, incluyendo seccion de pendientes si el budget se agoto.
- Reportes criticos validados con `scripts/check.sh` o `scripts/validate_adaptive_investigation_report.py` antes de cerrar; salida no-cero bloquea el cierre.

## Contrato deterministico

La skill usa `assets/` como contrato offline:

- `assets/exploration-budget-policy.json`: el presupuesto de archivos, queries y minutos se declara antes del mapeo; el uso nunca puede exceder el limite.
- `assets/replan-gate-policy.json`: un re-plan requiere un finding con `invalidates_hypothesis=true`; los refinamientos no disparan re-plan.
- `assets/evidence-policy.json`: cada claim lleva evidencia local y no requiere red, reloj ni random.
- `assets/scratchpad-policy.json`: topologia, plan, findings, budget y riesgos se persisten para handoff.

Cuando exista un reporte JSON de cierre, validarlo con:

```bash
bash skills/katas-adaptive-investigation/scripts/check.sh
```

## Modos de fallo (y deteccion)

- **Re-plan reflejo**: re_plan en cada turno. Sintoma: el plan rota sin que ningun finding marque `invalidates_hypothesis`. Causa: confundir refinar con invalidar. Detector: el gate `replan-gate-policy.json` debe rechazar.
- **Budget de mentira**: se declara presupuesto pero `deep_dive` lee sin decrementar. Sintoma: uso > limite o sin telemetria. Detector: `exploration-budget-policy.json` exige uso <= limite.
- **Mapeo caro disfrazado de barato**: leer cuerpos completos en Fase 1. Sintoma: `read` antes del primer plan. Mata el ahorro de contexto que justifica la kata.
- **Cierre optimista**: marcar completo ignorando pendientes tras agotar budget. Un cierre honesto reporta lo no explorado; verde no es exito.
- **Scratchpad de monologo**: volcar dudas/hipotesis sin confirmar en vez de conclusiones. Contamina el handoff (ver Kata 18).

## Cuando activar

- El dominio o repositorio es desconocido y no hay mapa previo confiable.
- El usuario pide investigar, mapear, auditar o entender una base de codigo o documento extenso.
- Hay riesgo de quemar contexto leyendo de mas si no se acota la exploracion.
- No activar cuando la tarea ya esta totalmente especificada y el plan es trivial y estable.

## Skills relacionadas

- `katas-subagent-parallelism`
- `katas-scratchpad-pattern`
- `katas-builtin-tool-selection`
- `katas-plan-mode-exploration`

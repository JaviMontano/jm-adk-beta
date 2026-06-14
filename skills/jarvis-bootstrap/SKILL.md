---
name: jarvis-bootstrap
version: 0.2.0
description: "Bootstrap del Jarvis OS: crea CLAUDE.md y MEMORY.md raiz y la estructura minima de niveles N0-N4 con proyectos semilla P00/P01/P02, sin sobrescribir ediciones locales."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - jarvis-bootstrap
  - bootstrap-jarvis
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Jarvis Bootstrap

Inicializa un Jarvis OS vacio o incompleto: deja un `CLAUDE.md` y un `MEMORY.md`
raiz coherentes y el esqueleto de niveles **N0-N4** con los proyectos semilla
**P00/P01/P02**. Es **idempotente y aditivo**: nunca pisa lo que ya existe.

## When to use / not use

- **USAR** cuando el directorio destino no tiene Jarvis OS, o le faltan piezas
  raiz (`CLAUDE.md`, `MEMORY.md`, niveles N0-N4, semillas P00-P02). {INFERENCIA}
- **USAR** para completar un OS parcial sin tocar ediciones locales (modo
  missing-only). {MEMORIA}
- **NO usar** para reescribir contenido ya curado, para generar entregables de
  cliente, ni para tareas ajenas al andamiaje del OS. {SUPUESTO}
- **NO usar** sin un directorio destino claro: ante ambiguedad, pregunta. {INFERENCIA}

## Inputs

- **Destino** (requerido): ruta raiz del Jarvis OS a crear o completar.
- **Modo**: `missing-only` (default, seguro) o `--force` (sobrescribe tras
  revisar diffs). {MEMORIA}
- **Contexto opcional**: nombre del operador, marca activa, objetivo del OS,
  para sembrar `MEMORY.md` con datos reales en vez de placeholders. {INFERENCIA}

## Outputs

- `CLAUDE.md` raiz: contrato de memoria del proyecto, enlaces a la red de
  orquestacion, reglas duras.
- `MEMORY.md` raiz: estado persistente inicial (identidad, marcas, indice).
- Estructura `N0-N4` minima con carpetas semilla `P00/P01/P02` y sus
  `CLAUDE.md` locales placeholder.
- **Reporte de bootstrap**: por cada artefacto, `creado` / `omitido (ya existe)`
  / `sobrescrito (--force)`, con la ruta absoluta. {INFERENCIA}

## Procedure

### 1. Discover (lee antes de escribir)
Resuelve la ruta destino. Inventaria que ya existe (`CLAUDE.md`, `MEMORY.md`,
niveles, semillas). **Read-before-write es obligatorio**: nunca escribas sobre
un archivo que no inspeccionaste primero. {MEMORIA}

### 2. Analyze
Calcula el delta = piezas faltantes. Elige el plan minimo: solo lo ausente. Si
`--force`, lista explicitamente que se sobrescribira y por que.

### 3. Execute
Crea solo el delta con las herramientas permitidas. Cada `Write` va precedido de
una comprobacion de existencia. Mantiene el cambio acotado al andamiaje; no
inyecta contenido de negocio inventado.

### 4. Validate (gate de aceptacion)
No marques completo sin pasar **todos** los criterios de abajo.

## Acceptance criteria (validation gate)

- [ ] `CLAUDE.md` y `MEMORY.md` raiz existen y son parseables. {INFERENCIA}
- [ ] Niveles `N0-N4` presentes; semillas `P00/P01/P02` con su `CLAUDE.md` local.
- [ ] Cero archivos preexistentes sobrescritos salvo `--force` explicito. {MEMORIA}
- [ ] El reporte de bootstrap enumera cada artefacto con su estado y ruta absoluta.
- [ ] Cada afirmacion no trivial del reporte lleva su tag de procedencia. {DOC}

## Edge cases

- **Sin destino**: detente y pide la ruta raiz — `{VACIO_CRITICO}`, no autocompletes. {DOC}
- **OS parcial**: completa solo lo ausente; reporta lo omitido, no lo silencies.
- **Conflicto missing-only vs --force**: gana la opcion segura (missing-only);
  exige confirmacion explicita para forzar. {INFERENCIA}
- **Ediciones locales / variantes `.local` / `user-context`**: preservalas
  intactas; los archivos de soporte generados son missing-only por defecto. {MEMORIA}
- **Permisos / ruta no escribible**: aborta antes de escritura parcial y reporta. {INFERENCIA}

## Anti-patterns (anti-scope)

- Regenerar un OS ya curado "para limpiarlo" — destruye memoria. {SUPUESTO}
- Sembrar `MEMORY.md` con datos de marca inventados o mezclar marcas. {DOC}
- Usar `--force` sin revisar diffs primero.
- Tratar este skill como generador de entregables; solo monta andamiaje.

## Self-correction triggers

- Vas a hacer `Write` sin haber leido el destino → para y lee primero. {INFERENCIA}
- El reporte dice "creado" pero el archivo ya existia → era omision, corrige el estado.
- Una afirmacion del reporte no es reproducible desde el contexto → etiquetala o eliminala. {DOC}

## Decisions & trade-offs

- **Missing-only como default** sobre force: prioriza no perder memoria del
  operador frente a la conveniencia de un OS "limpio"; el coste es dejar piezas
  parcialmente desactualizadas, asumible porque se reportan. {INFERENCIA}
- **Aditivo, no orquestador**: este skill no resuelve runtime ni rutea modelos
  (eso vive en `environment-protocol.md`); solo deja el andamiaje. Mantiene el
  skill pequeno y componible. {DOC}

## Example

`jarvis-bootstrap` sobre un directorio con `CLAUDE.md` ya editado:
→ omite `CLAUDE.md` (ya existe), crea `MEMORY.md`, niveles N1-N4 y semillas
P00-P02 faltantes; reporta 8 creados, 1 omitido, 0 sobrescritos. {INFERENCIA}

## Evidence requirements

- Familia de tags **Jarvis OS** (operador): `{MEMORIA}` `{EXTRAIDO_HILO}`
  `{SUPUESTO}` `{INFERENCIA}` `{AUTOCOMPLETADO}` `{POR_CONFIRMAR}`
  `{VACIO_CRITICO}`. No mezclar con la familia Alfa. Ver
  `references/verification-tags.md`. {DOC}
- Marca cada inferencia y supuesto; `{VACIO_CRITICO}` es terminal: detente y pregunta. {DOC}

## Assets

- Bundle de validacion en `assets/`: `assets/checklist.md` y
  `assets/quality-rubric.json` respaldan el gate del guardian (ver `assets/README.md`).

## Update-safety notes

- Archivos de soporte generados: **missing-only** por defecto.
- `--force` solo tras revisar diffs.

## Related skills

- `workspace-governance` · `workflow-forge` · `quality-guardian`

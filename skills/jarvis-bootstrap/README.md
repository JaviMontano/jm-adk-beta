# jarvis-bootstrap

Inicializa un **Jarvis OS** vacio o incompleto de forma **idempotente y aditiva**:
deja un `CLAUDE.md` y un `MEMORY.md` raiz coherentes y el esqueleto de niveles
**N0-N4** con los proyectos semilla **P00/P01/P02**, sin pisar ediciones locales.

## Que hace

- Resuelve la ruta destino y **inventaria** que ya existe (read-before-write).
- Calcula el **delta** (piezas faltantes) y crea solo lo ausente.
- Siembra `MEMORY.md` con contexto real del operador cuando se aporta; nunca
  inventa datos de marca ni mezcla marcas.
- Emite un **reporte de bootstrap**: por artefacto `creado` / `omitido (ya existe)`
  / `sobrescrito (--force)` con ruta absoluta y tag de procedencia.

## Cuando usarlo / cuando no

- **USAR** cuando el destino no tiene Jarvis OS o le faltan piezas raiz
  (`CLAUDE.md`, `MEMORY.md`, niveles N0-N4, semillas P00-P02).
- **USAR** para completar un OS parcial en modo `missing-only` sin tocar ediciones
  locales, variantes `.local` ni `user-context`.
- **NO usar** para reescribir contenido ya curado, generar entregables de cliente,
  ni rutear runtime/modelos (eso vive en `environment-protocol.md`).
- **NO usar** sin destino claro: `{VACIO_CRITICO}` es terminal, pregunta.

## Como rutea / ejecuta

1. **Discover** — resuelve ruta, inventaria existentes (Read/Bash).
2. **Analyze** — delta = faltantes; si `--force`, lista que se sobrescribe y por que.
3. **Execute** — Write solo del delta, cada uno precedido de check de existencia.
4. **Validate** — gate de aceptacion; no marca completo sin evidencia.

## Modos

- `missing-only` (default, seguro): solo crea lo ausente.
- `--force`: sobrescribe, **solo tras revisar diffs**; ante conflicto gana
  `missing-only`.

## Evidencia

Familia de tags **Jarvis OS** (no mezclar con la familia Alfa):
`{MEMORIA}` `{EXTRAIDO_HILO}` `{SUPUESTO}` `{INFERENCIA}` `{AUTOCOMPLETADO}`
`{POR_CONFIRMAR}` `{VACIO_CRITICO}`.

## Enlaces

- Contrato y procedimiento: [SKILL.md](SKILL.md)
- Conocimiento de dominio: [knowledge/body-of-knowledge.md](knowledge/body-of-knowledge.md)
- Grafo de conceptos: [knowledge/knowledge-graph.json](knowledge/knowledge-graph.json)
- Prompts: [prompts/primary.md](prompts/primary.md) ·
  [prompts/meta.md](prompts/meta.md) ·
  [quick](prompts/variations/quick.md) · [deep](prompts/variations/deep.md)
- Plantilla de salida (reporte): [templates/output.md](templates/output.md)
- Ejemplo: [examples/example-input.md](examples/example-input.md) →
  [examples/example-output.md](examples/example-output.md)
- Roles: [lead](agents/lead.md) · [specialist](agents/specialist.md) ·
  [support](agents/support.md) · [guardian](agents/guardian.md)
- Bundle de activos: [assets/](assets/README.md)

## Skills relacionados

`workspace-governance` · `workflow-forge` · `quality-guardian`

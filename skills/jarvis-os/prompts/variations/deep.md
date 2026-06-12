# Prompt — deep (jarvis-os)

Ruteo profundo. Para inputs ambiguos, multi-sector, o cuando hay que materializar estructura y validar guardrails a fondo.

## Fase 0 — Lectura de estado
Lee `docs/jarvis-os/` (playbook + runbook) y `user-context/context/routing-map.md`. Lista qué evidencia aportó cada uno. Prohibido inferir desde caché/historial.

## Fase 1 — Clarify
Captura el input con timestamp + intención. Si hay varios hilos, sepáralos: cada uno puede rutear a un sector distinto.

## Fase 2 — Organize (cascada completa)
Recorre los 5 pasos de la cascada documentando el resultado de cada uno:
1. prefijo explícito · 2. working dir · 3. presencia `02_Proyectos/`|`01_Estaciones/` · 4. keywords · 5. preguntar.
Asigna sector N0–N4 y la carpeta exacta. Si la cascada no converge → formula la pregunta de desambiguación.

## Fase 3 — Optimize (gate completo)
Verifica por evidencia: sectores/kebab-case, NOW≤3, rule-stacking, Rule-9 por capa, sin secretos, frontera `user-context/`, una sola familia de tags. Aplica autocorrección donde falle.

## Fase 4 — Liberate
Invoca el/los scaffolders o cadencias, o deriva a la skill concreta. Para R&D (N3) aplica Regla de 3; para automatización aplica los 14 días supervisados.

## Salida
Entregable completo por `templates/output.md`: ruteo razonado, estructura materializada (si aplica), gate verificado checkbox a checkbox con evidencia, y próximos pasos. Tags inline de una sola familia.

# Assets — jarvis-os

Bundle de activos deterministas que respaldan el acceptance gate y la evaluación de calidad del ruteo COOL.

| Asset | Tipo | Para qué | Usado por |
|---|---|---|---|
| `quality-rubric.json` | rubric | Evalúa un ruteo COOL contra 6 criterios ponderados (lectura de estado, ruteo resuelto, derivación, soberanía, reglas, familia de tags). | `SKILL.md` |
| `checklist.md` | checklist | Lista determinista que `guardian` recorre antes de marcar un ruteo completo. | `SKILL.md`, `agents/guardian.md` |

El manifiesto canónico es `manifest.json`. Toda entrada `used_by` apunta a un archivo existente del skill. Mantén el bundle lean: estos activos son operativos, no documentación duplicada.

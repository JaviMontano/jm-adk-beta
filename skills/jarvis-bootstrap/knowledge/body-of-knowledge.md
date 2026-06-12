# Body of Knowledge — jarvis-bootstrap

Conocimiento de dominio para inicializar un **Jarvis OS** de forma idempotente y
aditiva. Aplica la familia de evidencia Jarvis OS, no la familia Alfa.

## 1. Conceptos clave

### 1.1 Jarvis OS
Sistema de archivos-contrato que un operador usa como memoria persistente de
trabajo. Su raiz (N0) declara identidad, marca activa y la red de orquestacion;
sus niveles inferiores especializan el contexto.

### 1.2 Contrato de memoria raiz
- **`CLAUDE.md` raiz**: contrato de memoria del proyecto. Enlaza a la red de
  orquestacion y fija las reglas duras (evidencia obligatoria, read-before-write,
  single-brand, nunca precios).
- **`MEMORY.md` raiz**: estado persistente inicial — identidad del operador,
  marcas, indice. Es la pieza que mas memoria acumula; perderla es el peor fallo.

### 1.3 Niveles N0-N4
Capas de contexto de lo general a lo especifico. N0 = raiz; N1-N4 = subcontextos
progresivos. Cada nivel tiene su `CLAUDE.md` local. El bootstrap deja el
**esqueleto minimo** de los cinco niveles, no su contenido curado.

### 1.4 Semillas P00/P01/P02
Tres proyectos plantilla minimos. Cada uno con su `CLAUDE.md` local placeholder,
listo para que el operador lo cure. No se siembran con datos de negocio inventados.

### 1.5 Delta
Conjunto de piezas **ausentes** respecto al OS objetivo. El plan de ejecucion es
exactamente el delta — ni mas (no toca lo existente) ni menos (no deja huecos).

## 2. Estandares operativos

| Estandar | Regla |
|----------|-------|
| Read-before-write | Nunca escribir sobre un archivo no inspeccionado antes. |
| Idempotencia | Segunda corrida en `missing-only` ⇒ 0 creados. |
| Aditividad | Solo se anade el delta; lo existente queda intacto. |
| Single-brand | `MEMORY.md` jamas mezcla marcas; identificar marca primero. |
| Reporte trazable | Cada artefacto: estado + ruta absoluta + tag. |
| Abort seguro | Permisos/ruta no escribible ⇒ abortar antes de escritura parcial. |

## 3. Reglas de decision

1. **Modo por defecto** = `missing-only`. Ante conflicto con `--force`, gana la
   opcion segura; `--force` exige confirmacion explicita y revision de diffs.
2. **Destino ausente** ⇒ `{VACIO_CRITICO}`: terminal, detente y pregunta. No
   autocompletes la ruta.
3. **OS parcial** ⇒ completa solo lo ausente y reporta lo omitido; no lo silencies.
4. **Preservacion** ⇒ ediciones locales, variantes `.local` y `user-context`
   quedan intactas; los soportes generados son missing-only por defecto.
5. **Estado correcto** ⇒ "creado" solo si antes no existia; si existia, "omitido".

## 4. Taxonomia de evidencia (familia Jarvis OS)

| Tag | Significado |
|-----|-------------|
| `{MEMORIA}` | Proviene de memoria persistente del operador. |
| `{EXTRAIDO_HILO}` | Extraido del contexto de la conversacion. |
| `{SUPUESTO}` | Supuesto explicito, falsable. |
| `{INFERENCIA}` | Conclusion derivada por razonamiento. |
| `{AUTOCOMPLETADO}` | Estructura generada por defecto, sin dato real. |
| `{POR_CONFIRMAR}` | Pendiente de confirmacion del operador. |
| `{VACIO_CRITICO}` | Falta un dato terminal; detener y preguntar. |

No mezclar con la familia Alfa. `{VACIO_CRITICO}` es siempre terminal.

## 5. Criterios de calidad (gate)

- `CLAUDE.md`/`MEMORY.md` raiz existen y son parseables.
- N0-N4 presentes; P00/P01/P02 con `CLAUDE.md` local.
- Cero sobrescrituras salvo `--force` explicito.
- Reporte completo y trazable.
- Toda afirmacion no trivial etiquetada.

## 6. Anti-patrones

- Regenerar un OS curado "para limpiarlo" — destruye memoria.
- Sembrar `MEMORY.md` con datos de marca inventados o mezclar marcas.
- `--force` sin diffs revisados.
- Tratar el skill como generador de entregables (solo monta andamiaje).

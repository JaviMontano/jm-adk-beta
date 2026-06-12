# Auditoria de veracidad — <titulo o fuente del texto>

- **Familia usada**: <Jarvis OS | Alfa core>
- **Audiencia**: <operador | kit/repo>
- **Fecha**: <YYYY-MM-DD>
- **Estado**: <COMPLETO | BLOQUEADO por {VACIO_CRITICO}>

## 1. Texto auditado

> Reproduce aqui el texto original con **un (1)** tag inline por afirmacion no obvia.
> No reescribir el contenido. Ejemplo:
>
> "El endpoint responde en 40ms `{POR_CONFIRMAR}` y el equipo lo aprobo ayer `{EXTRAIDO_HILO}`."

## 2. Plan de verificacion

Una fila por cada `{SUPUESTO}` / `{POR_CONFIRMAR}`.

| # | Claim (extracto) | Tag | Paso de cierre concreto | Owner | Artefacto/comando |
|---|---|---|---|---|---|
| 1 | <claim> | `{POR_CONFIRMAR}` | <que leer / a quien preguntar / que correr> | <quien> | <ruta, link o `scripts/check.sh`> |
| 2 | <claim> | `{SUPUESTO}` | <accion de cierre> | <quien> | <artefacto> |

## 3. Resumen

- **Conteo por tag**:
  - `{MEMORIA}`: <n>
  - `{ADJUNTO}`: <n>
  - `{EXTRAIDO_HILO}`: <n>
  - `{WEB}`: <n>
  - `{CONOCIMIENTO}`: <n>
  - `{SUPUESTO}`: <n>
  - `{INFERENCIA}`: <n>
  - `{AUTOCOMPLETADO}`: <n>
  - `{POR_CONFIRMAR}`: <n>
  - `{VACIO_CRITICO}`: <n>
- **Familia**: <Jarvis OS | Alfa core> (una sola, ortografia consistente)
- **Bloqueos `{VACIO_CRITICO}`**: <lista o "ninguno">
- **Limites declarados**: <claims donde solo se marca el riesgo legal/medico/financiero/seguridad, sin decidir>

## 4. Gate (auto-chequeo)

- [ ] Un tag por afirmacion no obvia, una sola familia.
- [ ] Ningun `{WEB}` sin cita; ningun `{VACIO_CRITICO}` con dato fabricado.
- [ ] Cada `{SUPUESTO}`/`{POR_CONFIRMAR}` con paso concreto.
- [ ] Ortografia de tags consistente.
- [ ] Sin sobre-tageo; contenido no reescrito.

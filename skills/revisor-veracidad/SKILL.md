---
name: revisor-veracidad
version: 0.2.0
last_updated: 2026-06-11
description: "Audita un texto, etiqueta cada afirmacion no reproducible con un tag de veracidad y propone el siguiente paso concreto de verificacion."
owner: "JM Labs"
triggers:
  - revisor-veracidad
  - verificar-fuente
  - marcar-supuesto
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Revisor Veracidad

Audita un borrador o respuesta y devuelve el mismo texto con tags de procedencia inline, mas un plan de verificacion para todo lo que no sea verificable hoy. La fuente canonica de tags es `references/verification-tags.md`; este skill la aplica, no la redefine. [DOC]

## When to use / triggers

- Antes de entregar texto cuyas afirmaciones podrian ser falsas, derivadas o asumidas (informes, specs, mensajes a cliente). [INFERENCIA]
- Cuando el orquestador exige tags de evidencia y hay que homologar un borrador sin ellos. [SUPUESTO]
- Para convertir supuestos implicitos en `{POR_CONFIRMAR}` con accion de cierre.

**No usar para**: generar el contenido (eso es otro skill), validar codigo en ejecucion, ni reemplazar revision experta legal/medica/financiera/seguridad — ahi solo se marca el riesgo, no se decide. [SUPUESTO]

## Inputs

- El texto a auditar (pegado, archivo, o ruta). Sin texto -> `{VACIO_CRITICO}`: pedir el objetivo y parar. [DOC]
- Audiencia, para elegir familia de tags: salida a operador -> set Jarvis OS; salida a kit/repo -> set Alfa core. Nunca mezclar familias en un documento. [DOC]
- Fuentes disponibles (archivos, repo, hilo) para poder degradar `{WEB}` sin cita a `{CONOCIMIENTO}` o eliminar la afirmacion. [DOC]

## Outputs

- El texto original con un (1) tag por afirmacion no obvia.
- Lista de verificacion: cada `{SUPUESTO}`/`{POR_CONFIRMAR}` emparejado con un paso concreto y accionable (que leer, a quien preguntar, que comando correr).
- Resumen: conteo por tag, familia usada, y bloqueos `{VACIO_CRITICO}` si los hay.

## Tag set (Jarvis OS, operador)

`{MEMORIA}` `{ADJUNTO}` `{EXTRAIDO_HILO}` `{WEB}` `{CONOCIMIENTO}` `{SUPUESTO}` `{INFERENCIA}` `{AUTOCOMPLETADO}` `{POR_CONFIRMAR}` `{VACIO_CRITICO}`.

Alfa core (kit/repo): `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Homologar Jarvis -> Alfa, nunca al reves; ES y EN son alias, no tags distintos. Tabla y mapping completos en `references/verification-tags.md`. [DOC]

## Procedure

1. **Detectar familia y bloqueos.** Si no hay texto, emitir `{VACIO_CRITICO}` y parar. Elegir familia por audiencia. [DOC]
2. **Segmentar en afirmaciones.** Separar claims verificables de estructura/opinion. No etiquetar input del usuario re-citado ni la propia estructura del output. [DOC]
3. **Asignar el tag mas debil aplicable.** Si dos tags caben, elegir el menos cierto: un `{SUPUESTO}` disfrazado de `{MEMORIA}` es el fallo que importa. [DOC]
4. **Validar `{WEB}`.** Sin cita es invalido: degradar a `{CONOCIMIENTO}` o eliminar la afirmacion. [DOC]
5. **Generar plan de cierre.** Por cada `{SUPUESTO}`/`{POR_CONFIRMAR}`, escribir el paso que lo verifica.
6. **Auto-chequear** contra el gate de abajo antes de entregar.

## Validation gate (acceptance criteria)

- [ ] Cada afirmacion no obvia tiene exactamente un tag de una sola familia. [DOC]
- [ ] Ningun `{WEB}` sin cita; ningun `{VACIO_CRITICO}` seguido de dato fabricado. [DOC]
- [ ] Cada `{SUPUESTO}`/`{POR_CONFIRMAR}` lleva un paso de verificacion concreto.
- [ ] Ortografia de tags (ES vs EN) consistente en todo el documento.
- [ ] No se sobre-etiqueta: lo trivialmente auto-evidente queda sin tag. [INFERENCIA]

## Self-correction triggers

- Mas de un tag por claim -> colapsar al mas debil (paso 3).
- `{WEB}` huerfano de cita -> degradar o eliminar (paso 4).
- `{SUPUESTO}` sin paso de cierre -> volver al paso 5.
- Dos familias en el mismo documento -> rehacer eligiendo una por audiencia (paso 1).
- Casi todo etiquetado -> probable sobre-tagging; quitar los auto-evidentes.

## Edge cases

- **Texto sin afirmaciones factuales** (puro saludo/formato): devolver sin tags y decirlo. [INFERENCIA]
- **Requisitos en conflicto** ("etiqueta pero ignora la evidencia"): declarar el conflicto y elegir la interpretacion segura (mantener la evidencia). [DOC]
- **Cita presente pero inverificable** (link muerto, fuente privada): tratar como `{POR_CONFIRMAR}`, no como `{WEB}`.
- **Customizacion local**: preservar archivos locales; cambios solo aditivos; `--force` unicamente tras revisar diffs. [CONFIG]

## Anti-patterns

- Etiquetar todo para parecer riguroso: destruye la escaneabilidad y esconde los claims que importan. [DOC]
- Subir el tag a uno mas fuerte de lo justificado (ej. `{SUPUESTO}` -> `{MEMORIA}`). [DOC]
- Emitir `{POR_CONFIRMAR}` sin el paso que lo cierra: es ruido, no verificacion.
- Reescribir o "mejorar" el contenido en vez de solo auditarlo: fuera de alcance.

## Example (mini)

Entrada: "El endpoint responde en 40ms y el equipo lo aprobo ayer."
Salida: "El endpoint responde en 40ms `{POR_CONFIRMAR}` y el equipo lo aprobo ayer `{EXTRAIDO_HILO}`."
Plan: `{POR_CONFIRMAR}` -> correr `scripts/check.sh` o un benchmark contra el endpoint y registrar el p50 real.

## Scripts

Chequeos deterministas en `scripts/`: `scripts/check.sh` valida los fixtures bajo `scripts/fixtures/`. Contrato en `scripts/README.md`. [CONFIG]

## Assets

Rubrica de calidad y checklist del gate en `assets/` (ver `assets/README.md` y `assets/manifest.json`); el guardian los aplica antes de entregar. [CONFIG]

## Related skills

- `input-analysis` — antes, para entender el encargo.
- `frontload-prompt` — antes, para cargar contexto y fuentes.
- `cierre-conversacion` — despues, para arrastrar los `{POR_CONFIRMAR}` abiertos.

## Assumptions and limits

- No reemplaza revision experta en decisiones legales/medicas/financieras/seguridad; solo marca el riesgo. [DOC]
- Si la evidencia no existe, la afirmacion se marca `{SUPUESTO}` u open question — nunca se inventa el respaldo. [DOC]
- Archivos de soporte generados son missing-only por defecto. [CONFIG]

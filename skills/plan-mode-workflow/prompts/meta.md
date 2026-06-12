# Prompt — Meta (plan-mode-workflow)

Meta-prompt para **auto-evaluar y mejorar** un diseño de gate de dos modos antes
de declararlo aplicado. Úsalo después de generar el contrato del gate.

## Preguntas de verificación

1. **¿El modo es dato o prosa?** Localiza `mode` y `signed_plan_hash`. Si el control
   está en una frase ("ahora puedo escribir"), el gate no existe. [CÓDIGO]
2. **¿La blocklist es fail-closed?** ¿Hay allowlist de lectura + deny por defecto, o
   una whitelist de writes que deja pasar lo no enumerado? [CONFIG]
3. **¿La firma referencia el hash exacto?** ¿`approve_plan` toma un hash y lo compara,
   o aprueba "el plan" en abstracto? [CÓDIGO]
4. **¿El hook cubre Bash mutante?** ¿Bloquea `rm `, `sed -i`, redirecciones por patrón,
   no solo por nombre de tool? [CÓDIGO]
5. **¿Hash-mismatch revierte a `plan`?** ¿Un `plan.md` cambiado tras firmado fuerza
   re-aprobación? [CÓDIGO]
6. **¿`bypassPermissions` y entrada vacía se rechazan?** [CONFIG]
7. **¿Hay rastro de evidencia?** ¿Plan firmado + diff final quedan registrados? [DOC]

## Auto-correcciones

- Si alguna respuesta es "no", **re-abre el diseño** en ese punto antes de cerrar.
- Marca cada hallazgo con su tag de evidencia y devuelve el control al lead.
- Nunca declares la skill aplicada en verde-por-defecto: exige verde-con-evidencia.

## Disciplina

Sin precios. Sin PII de cliente. Single-brand (JM Labs). Si la tarea no escribe a
repo, degrada a no-activación en lugar de forzar el gate.

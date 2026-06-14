# Prompt — Deep (wbr-weekly-review)

WBR profundo para semanas densas, alcances con varios items arrastrados o cuando
el estancamiento empieza a volverse cronico. Anade analisis de causa raiz y
tendencia multi-semana sobre el flujo base.

## Entrada ampliada
- Semana ISO + alcance unico + fecha de corte.
- Compromisos previos con evidencia de cumplimiento.
- Senales completas con artefacto verificable por item.
- WBR de las 2-4 semanas previas para tendencia de arrastres y friccion recurrente.

Si falta periodo o alcance → `{VACIO_CRITICO}`, pregunta y detente.

## Pasos
1. **Recolectar** todo + leer los WBR previos para reconstruir la serie de arrastres.
2. **Clasificar** cada item en un lente; justifica los casos limite con `{INFERENCIA}`.
3. **Diagnosticar causa raiz** de cada estancado: antiguedad, causa (dependencia /
   decision / capacidad / alcance), dueno y proximo paso fechado. Distingue causa
   de sintoma explicitamente.
4. **Tendencia.** Para cada arrastre, cuenta semanas abiertas; ≥3 semanas →
   `{POR_CONFIRMAR}` + escalada a bloqueo. Para cada friccion, verifica si reaparece
   ≥2 semanas → recurrente, escalar a accion estructural.
5. **Comprometer** 3-5 acciones desde estancado+friccion, cada una con criterio de
   hecho y dueno; prioriza desbloquear lo cronico antes que abrir frentes nuevos.
6. **Validar** con el gate completo (ver `prompts/meta.md`).

## Salida
Acta WBR completa segun `templates/output.md` mas un bloque corto de **tendencia**:
antiguedad de arrastres y friccion recurrente con su escalada. Una sola familia de
tags `{...}`; never green-as-success. {DOC}

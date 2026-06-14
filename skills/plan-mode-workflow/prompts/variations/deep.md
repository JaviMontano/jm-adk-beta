# Prompt — Deep (plan-mode-workflow)

Variación profunda: diseña el gate de dos modos **completo y auditable** para un
repo de alto blast radius (pagos, producción, workspace compartido), con todos los
edge cases y la rúbrica de aceptación.

## Contexto a recabar

- Repo objetivo, blast radius, dependencias críticas, trabajo no commiteado de otros.
- Aprobador(es) y política de re-firma.
- Requisitos de compliance: ¿la aprobación debe ser auditable (hash + aprobador + timestamp)?

## Diseño exhaustivo

1. **Máquina de estados** completa: `plan → execute` por `approve_plan(hash)`;
   `execute → plan` por hash-mismatch; deny que mantiene `plan`. [CÓDIGO]
2. **Write-blocklist exhaustiva:** todas las write-tools + MCP de mutación +
   patrones Bash (`rm `, `sed -i`, `mv `, `git commit`, `git push`, `>`, `>>`).
   Justifica fail-closed sobre fail-open. [CONFIG]
3. **`plan.md` detallado:** objetivo, archivos a tocar, orden de cambios, criterio
   de aceptación, riesgos y plan de rollback. [DOC]
4. **Evento de firma criptográfico:** hash del contenido del plan, `approved_by`,
   `plan_signed_at`. Persistencia y no-repudio. [CÓDIGO]
5. **Hook `PreToolUse`** con: chequeo de hash-mismatch primero, deny de write-tools,
   deny de Bash mutante por patrón, motivo explícito en cada deny. [CÓDIGO]
6. **Edge cases:** Bash mutante disfrazado de inspección; firma con hash viejo;
   `bypassPermissions`; entrada vacía; upgrade idempotente sin tocar otras skills. [CÓDIGO]
7. **Gate de aceptación:** corre los 6 criterios de `assets/quality-rubric.json`;
   ningún caso bloqueado pasa en verde. [DOC]
8. **Cierre:** plan firmado + diff final como rastro de qué se autorizó vs. ejecutó. [DOC]

## Disciplina

Cada afirmación con tag. Sin precios. Sin PII de cliente. Single-brand (JM Labs).
Verde-con-evidencia, nunca verde-por-defecto.

# Deep Variation — frontload-prompt

Para inputs largos, multi-objetivo, o que dependen de un codebase/documento. Pase
exhaustivo con inspección de fuentes.

## Prompt
1. **Discover a fondo.** Lee el input completo. Inspecciona con Read/Grep/Glob
   cada archivo/repo/documento referenciado **antes** de inferir. Cita lo
   encontrado con `{ADJUNTO}` / `{EXTRAIDO_HILO}` / `{MEMORIA}`.
2. **Detecta multi-objetivo.** Si hay más de una intención, separa: un SPEC por
   objetivo, o un Purpose con sub-objetivos numerados. Nunca los fundas.
3. **Analyze cada hueco con la regla de oro.** ¿Puede el ejecutor arrancar sin
   esto? → clasifica en `{INFERENCIA}` / `{AUTOCOMPLETADO}` / `{VACIO_CRITICO}`.
4. **Structure** el/los bloque(s) SPEC con tags inline y defaults declarados.
5. **Validate** contra el gate completo (5 criterios) y emite veredicto.

## Salida esperada
Uno o varios bloques SPEC (según objetivos) usando `templates/output.md`, cada
uno con su veredicto **READY**/**BLOCKED**.

## Profundidad extra
- Para cada `{VACIO_CRITICO}`, da la pregunta exacta que lo desbloquea.
- Para cada conflicto de requisitos, nombra la interpretación elegida y márcala
  `{SUPUESTO}`.
- Reporta qué fuentes inspeccionaste y qué no encontraste (evidencia negativa
  cuenta).

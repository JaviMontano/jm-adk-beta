# Quick Variation — pristino-calibration

For `bypass`, `solo_*`, or `full+trivial` modes where ceremony must stay minimal.

## Instruction

1. Read the block; resolve `MODE`.
2. Apply the smallest correct shape:
   - `bypass` → plain answer only.
   - `solo_prompt` → only the prompt optimizado.
   - `solo_respuesta` → only the respuesta.
   - `full+trivial` → persona line (line 1) + a tight respuesta, no Canvas.
3. Keep precedence Veracidad > Seguridad > Objetivo > Formato > Estilo.
4. One tag family; tag only genuinely non-obvious claims; declare confidence.
5. No Canvas, no section 1/2 unless the mode demands it. No mode bleed.

## Stop conditions
- Empty input or fabrication-only intent → refuse.
- A `VACIO_CRITICO` appears → stop and ask, do not auto-fill.

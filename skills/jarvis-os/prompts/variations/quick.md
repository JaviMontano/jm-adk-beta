# Prompt — quick (jarvis-os)

Ruteo rápido. Para inputs donde el sector es casi evidente y solo falta confirmar la skill objetivo.

## Pasos
1. **Clarify** breve: ¿qué llegó y con qué intención?
2. **Organize**: corre la cascada de ruteo solo hasta el primer match (prefijo → working dir → presencia de carpeta → keywords). Asigna sector N0–N4.
3. **Liberate**: nombra el scaffolder/cadencia objetivo.

## Reglas mínimas no negociables
- Si el usuario ya nombró la skill → delega, no re-enrutes.
- Sector dudoso → **pregunta**, no autoasignes.
- Tags inline de una sola familia.

## Salida (una línea por campo)
- Sector: `<I–V / N0–N4>`
- Ubicación: `<carpeta>`
- Ruta: `<scaffolder|cadencia|skill>`
- Tag: `[DOC]` / `[INFERENCIA]` / `[SUPUESTO]`

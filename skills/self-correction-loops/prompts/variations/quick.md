# Variacion quick — self-correction-loops

Bucle de verificacion en una sola pasada, para un unico agregado.

## Uso

Dame `field`, `declared`, los componentes crudos y `data_type`. Yo:

1. Recomputo `computed` desde los crudos (suma de lineas / debe - haber / conteo).
2. Fijo `epsilon` (0 para enteros, 0.005 moneda, 1e-6 float) segun
   `assets/epsilon-policy.json`.
3. Emito `{ field, declared, computed, delta, mismatch }` con
   `delta = declared - computed` y `mismatch = abs(delta) > epsilon`.
4. Si `mismatch=true`: `action="escalate_to_human"`, campo declarado intacto.

## Reglas no negociables (incluso en modo rapido)

- Nunca reusar el declarado como calculado.
- Nunca sobreescribir el campo.
- Ambos valores visibles.

Salida: una linea de registro tipado por campo. Sin precios, single-brand.

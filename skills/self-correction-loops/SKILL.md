---
name: self-correction-loops
version: 1.1.0
description: "Construir verificacion cruzada declarado-vs-calculado con mismatch flag tipado y escalada a humano; recomputo independiente, epsilon justificado, nunca corregir numeros en silencio."
owner: "JM Labs"
triggers:
  - self-correction loops
  - cross-check verification
  - mismatch flag
  - numeric validation
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Self Correction Loops

## Capacidad

Construir un bucle de verificacion cruzada que compara el valor **declarado** (lo que la fuente afirma) contra el valor **calculado** (lo que recomputas de forma independiente desde los datos crudos). Cuando difieren mas alla de un `epsilon` justificado, el sistema emite `mismatch=true` con ambos valores y escala a un humano. La invariante dura: **nunca corregir un numero en silencio** [DOC]. Un mismatch no es un error a parchear; es la senal de que la fuente, el calculo o los datos estan en conflicto, y esa decision pertenece a una persona [INFERENCIA].

Esto convierte la auto-correccion en un control de integridad auditable, no en un "arreglo" opaco que oculta la discrepancia y propaga un dato falso con apariencia de validado [INFERENCIA].

## Cuando usarla

Activa cuando se cumplen las dos condiciones (declarado + recomputo independiente disponibles):

- Hay campos numericos que llegan ya agregados (totales, subtotales, balances, conteos) y ademas tienes los componentes para recomputarlos [DOC].
- El costo de un numero silenciosamente equivocado es alto: finanzas, facturacion, inventario, reporting regulatorio [DOC].
- Quieres distinguir "lo recompute y coincide" de "lo recompute y NO coincide" en lugar de confiar ciegamente en lo declarado [DOC].
- Necesitas rastro de auditoria: cada total verificado debe poder mostrar declarado vs calculado [DOC].

## Cuando NO usarla (anti-scope)

- **Sin recomputo independiente**: el agregado llega solo (total sin lineas ni componentes). No hay nada contra que cruzar; degrada a `[POR_CONFIRMAR]` humano, no inventes un calculado [INFERENCIA]. Caso `unverifiable_aggregate_degradation` [CONFIG].
- **Validacion de formato/parsing** (el JSON parsea, el campo existe, el tipo es correcto): eso es `validation-retry-design`, no este skill [DOC]. Caso `format_validation_not_numeric` espera `expected_activation:false` [CONFIG].
- **"Arregla los numeros para que cuadren"**: peticion de correccion silenciosa. Se rechaza, no se ejecuta; este skill bloquea exactamente ese patron [DOC]. Casos `conflicting_silent_fix` y `false_positive_generic_fix` -> no activar [CONFIG].
- Input vacio o tarea no numerica (redactar correo, etc.): no activar [CONFIG].

## Inputs / Outputs

**Inputs** [INFERENCIA]: por cada campo verificable -> `field` (nombre), `declared` (valor de la fuente), una **formula de recomputo** desde componentes crudos, `data_type` (entero | moneda | float) y el destino de escalada.

**Output**: registro tipado por campo -> `{ field, declared, computed, delta, mismatch }`; ante mismatch se anade `action="escalate_to_human"` y el campo declarado **permanece intacto** [CODE]. El reporte debe cumplir `assets/self-correction-loops-contract.json` [CONFIG].

## Como construir

1. **Identifica los campos numericos verificables.** Cada uno necesita dos caminos: el declarado y una formula de recomputo desde datos mas primitivos (suma de lineas, balance = debe - haber, conteo de items) [DOC].
2. **Justifica el epsilon por tipo de dato.** Cero para enteros (conteos, cantidades). Tolerancia pequena para moneda y floats por redondeo (`1e-6` o el centavo segun la unidad). Documenta el porque; un epsilon arbitrario invalida el control [DOC]. Las tolerancias permitidas viven en `assets/epsilon-policy.json` [CONFIG].
3. **Recomputa de forma independiente.** No reuses el agregado declarado; deriva el calculado desde los componentes crudos. Reusar el declarado convierte el check en un no-op que siempre pasa [INFERENCIA].
4. **Compara y emite estado tipado.** Si `abs(declared - computed) <= epsilon` -> `match`. Si no -> `mismatch=true` con `declared`, `computed`, `delta` y `field` [CODE].
5. **Escala, no corrijas.** Ante mismatch, NO sobreescribas el campo. Adjunta el flag al output y deriva a revision humana con ambos valores visibles. Politica en `assets/mismatch-policy.json` y `assets/escalation-policy.json` [CONFIG].
6. **Cubre con un test estructural.** Un caso con mismatch inyectado debe producir `mismatch=true`; jamas un `total=computed` silencioso [CODE].

### Decisiones y trade-offs

- **`>` estricto para el flag**, no `>=`: una diferencia exactamente igual al epsilon se considera dentro de tolerancia (match). Es deliberado para que `epsilon=0` en enteros marque solo diferencias reales, no el caso `delta==0` [INFERENCIA].
- **`delta = declared - computed`** (signo conservado): el signo dice si la fuente sobre- o sub-declara; perderlo con `abs()` en el registro reduce el valor de auditoria [INFERENCIA].
- **Recomputo > confianza**: cuesta CPU recalcular, pero el costo de un total falso "validado" en finanzas es mayor [SUPUESTO].

## Patron correcto

```python
from dataclasses import dataclass

@dataclass
class CrossCheck:
    field: str
    declared: float
    computed: float
    epsilon: float

    @property
    def mismatch(self) -> bool:
        return abs(self.declared - self.computed) > self.epsilon

    def to_record(self) -> dict:
        return {
            "field": self.field,
            "declared": self.declared,
            "computed": self.computed,
            "delta": self.declared - self.computed,
            "mismatch": self.mismatch,
        }

def verify_total(invoice: dict) -> dict:
    computed = sum(line["amount"] for line in invoice["lines"])  # recomputo independiente
    check = CrossCheck(
        field="total",
        declared=invoice["total"],          # lo que la fuente afirma
        computed=computed,                  # lo que recalculamos
        epsilon=0.005,                      # medio centavo, justificado por redondeo
    )
    record = check.to_record()
    if check.mismatch:
        record["action"] = "escalate_to_human"   # NO se reescribe el total
    return record
```

## Anti-patrones

```python
# ANTI 1: confiar en lo declarado, o "corregir" en silencio.
def verify_total_bad(invoice: dict) -> dict:
    computed = sum(line["amount"] for line in invoice["lines"])
    invoice["total"] = computed   # sobreescribe sin avisar: oculta el conflicto
    return invoice                # el humano nunca ve que la fuente estaba mal

# ANTI 2: recomputo no-independiente (siempre pasa).
def verify_total_noop(invoice: dict) -> dict:
    declared = invoice["total"]
    computed = invoice["total"]   # mismo agregado: el check nunca puede fallar
    return {"mismatch": abs(declared - computed) > 0.005}

# ANTI 3: epsilon arbitrario sin justificacion -> oculta errores reales bajo "tolerancia".
```

## Disparadores de auto-correccion (self-check)

Si detectas cualquiera de estos en tu propia salida, corrige antes de entregar [INFERENCIA]:

- El `computed` deriva del mismo agregado que `declared` -> recomputa desde crudos (ANTI 2).
- Hay un `mismatch=true` y el campo fue sobreescrito -> revierte y escala (ANTI 1).
- Un epsilon de moneda aplicado a enteros, o un epsilon sin nota de justificacion -> ajusta a `epsilon-policy.json`.
- El reporte oculta `declared` o `computed` en un mismatch -> ambos deben ser visibles.

## Checklist de validacion (gate de aceptacion)

PASA solo si **todos** marcan:

- [ ] Campos numericos verificables identificados, cada uno con recomputo **independiente** de los datos crudos.
- [ ] `epsilon` justificado por tipo de dato: cero para enteros, tolerancia pequena documentada para moneda/floats.
- [ ] El valor calculado se deriva de componentes crudos, no del agregado declarado.
- [ ] Ante discrepancia se emite `mismatch=true` con `declared` y `computed` ambos visibles y `delta` con signo.
- [ ] Un mismatch escala a humano; el campo declarado NO se sobreescribe.
- [ ] Agregados sin recomputo posible se degradan a revision humana, no a un calculado inventado.
- [ ] Test estructural: caso con mismatch inyectado produce el flag; nunca un `total=computed` silencioso.
- [ ] El reporte cumple `assets/self-correction-loops-contract.json` y pasa `scripts/check.sh` con fixtures validas e invalidas.

## Upgrade safety y scope

- Al completar archivos faltantes del skill, **no sobreescribas ediciones locales**: anade lo ausente, respeta lo presente [DOC]. Caso `upgrade_safety_case` exige este comportamiento [CONFIG].
- Manten el alcance en el bucle de verificacion numerica; no expandas a formato, retry ni orquestacion (esos son skills hermanas) [INFERENCIA].

## Assets y validacion offline

- `assets/self-correction-loops-contract.json` define los campos obligatorios del reporte JSON [CONFIG].
- `assets/epsilon-policy.json` fija tolerancias permitidas por tipo de dato [CONFIG].
- `assets/mismatch-policy.json` y `assets/escalation-policy.json` obligan a mostrar ambos valores y escalar sin sobreescribir [CONFIG].
- `assets/structural-test-policy.json` declara las pruebas estructurales que deben quedar en `true` [CONFIG].
- `scripts/validate_self_correction_loops.py` valida reportes offline y `scripts/check.sh` ejecuta fixtures deterministicas positivas y negativas [CODE].
- `assets/` incluye ademas `assets/README.md`, `assets/quality-rubric.json` (8 criterios de aceptacion) y `assets/checklist.md` (gate operativo); ver `assets/manifest.json` [CONFIG].

## Katas y skills relacionadas

- Kata: `katas-critical-self-correction`
- Relacionada: `validation-retry-design` (formato/parsing, no numerico)
- Relacionada: `human-escalation-design` (a donde va el mismatch)
- Relacionada: `provenance-engineering` (rastro de auditoria del declarado)

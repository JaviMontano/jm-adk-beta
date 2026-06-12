# Ejemplo — Input

## Encargo

Pipeline de onboarding KYC. Para cada entidad extraemos tres atributos desde tres documentos distintos. El output va a un analista que **firma la apertura de la cuenta**. Diseña el pipeline con provenance tipada y dime que pasa cuando dos documentos discrepan.

## Inventario de fuentes

| source_id | documento | version | as_of |
|-----------|-----------|---------|-------|
| `coi-2024` | Certificate of Incorporation | rev A | 2024-03-02 |
| `aoa-2023` | Articles of Association | rev 2 | 2023-11-18 |
| `util-2025` | Comprobante de domicilio (utility bill) | — | 2025-01-09 |

## Atributos y locators

| atributo | source_id | locator |
|----------|-----------|---------|
| `legal_name` | `coi-2024` | pagina 1, encabezado |
| `legal_name` | `aoa-2023` | pagina 1, clausula 1 |
| `incorporation_date` | `coi-2024` | pagina 1, sello |
| `registered_address` | `aoa-2023` | pagina 2, clausula 3 |
| `registered_address` | `util-2025` | bloque de direccion |

## Datos crudos observados

- `legal_name`: "Acme Holdings Ltd." (`coi-2024`) y "ACME HOLDINGS LTD" (`aoa-2023`).
- `incorporation_date`: "02 Mar 2024" (`coi-2024`), solo una fuente.
- `registered_address`: "12 King St, London" (`aoa-2023`) y "48 Queen Rd, London" (`util-2025`).

## Consumidor / consecuencia

Analista de cumplimiento; firma la apertura de la cuenta. Necesita auditar el origen de cada dato antes de aprobar.

# Ejemplo de salida — prompt-chaining-design

Diseño de cadena para la auditoría de 80 archivos Python (ver `example-input.md`).

## 1. Contexto y decisión chaining vs single-pass

- **Tarea**: auditar 80 archivos Python y producir un reporte único.
- **Volumen del lote**: 80 unidades.
- **Decisión**: [x] chaining
- **Justificación**: 80 archivos crudos saturan una sola ventana de atención; el pase
  local es paralelizable y se exige aislar el fallo de parseo por archivo. [INFERENCIA]

## 2. Unidad atómica

- **Una unidad es**: un archivo `.py`.
- **Independencia**: confirmada — cada archivo se analiza sin necesitar el crudo de
  otro. [DOC]
- **Enumeración**: `glob("**/*.py")` sobre la raíz del repo.

## 3. Schema del pase local

| Campo | Tipo | Obligatorio | Notas |
|-------|------|-------------|-------|
| `unit_id` | str | sí | ruta relativa del archivo |
| `status` | `ok` \| `error` | sí | `error` si falla el parseo |
| `error_detail` | str \| null | si error | mensaje del `SyntaxError` |
| `findings` | list[str] | sí (si ok) | hallazgos de calidad del archivo |
| `loc` | int | sí (si ok) | líneas de código, para ranking de deuda |
| `severity_max` | `low`\|`med`\|`high` | sí (si ok) | peor severidad del archivo |

Modos de fallo cubiertos: `SyntaxError` de parseo, archivo vacío. [DOC]

## 4. Schema de transición

- **Contrato**: `list[FileSummary]`.
- **Invariante**: el código crudo NO viaja al pase 2; solo los resúmenes. [DOC]

## 5. Pase local (map)

```python
def local_pass(path: str) -> FileSummary:
    try:
        tree = ast.parse(read(path))
        findings, sev = analyze(tree)
        return FileSummary(unit_id=path, status="ok",
                           findings=findings, loc=count_loc(tree), severity_max=sev)
    except SyntaxError as exc:
        return FileSummary(unit_id=path, status="error", error_detail=str(exc))

summaries = [local_pass(p) for p in py_files]  # paralelizable, idempotente
```

## 6. Pase de integración (reduce)

```python
def integration_pass(summaries: list[FileSummary]) -> RepoReport:
    ok = [s for s in summaries if s.status == "ok"]
    failed = [s for s in summaries if s.status == "error"]
    top5 = sorted(ok, key=debt_score, reverse=True)[:5]  # solo resúmenes
    return RepoReport(per_file=ok, top_debts=top5, parse_failures=failed)
```

- Tolerancia: los archivos en `error` se listan en `parse_failures`; no abortan la
  auditoría ni contaminan el ranking.

## 7. Resultado de gates (Guardian)

| Gate | Veredicto | Evidencia |
|------|-----------|-----------|
| Pase 2 sin crudos | pass | el reduce solo lee `FileSummary` [CÓDIGO] |
| Schema por pase | pass | `FileSummary` + `RepoReport` tipados [CÓDIGO] |
| Error tipado por unidad | pass | `status="error"` + `error_detail` [CÓDIGO] |
| Pase local de una unidad | pass | `local_pass` recibe un solo `path` [CÓDIGO] |
| Schema de transición presente | pass | `list[FileSummary]` explícito [DOC] |
| Chaining justificado | pass | volumen + paralelismo + aislamiento [INFERENCIA] |

Todos los gates en verde con evidencia adjunta: diseño apto para entrega.

## 8. Anexo de costo

- Chaining: 80 análisis lineales + un reduce que lee 80 resúmenes acotados.
- Mega-prompt: concatenar 80 archivos crudos → atención saturada y costo cuadrático.

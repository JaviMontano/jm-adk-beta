# Ejemplo de entrada — self-correction-loops

Lote de dos facturas y un conteo de inventario que entran al ERP. Se pide verificar
cada agregado declarado contra su recomputo independiente antes de cargarlo, y
escalar a finanzas cualquier discrepancia. No corregir nada en silencio.

```json
{
  "destino_escalada": "finanzas-control@interno",
  "facturas": [
    {
      "id": "F-1001",
      "total_declarado": 100.00,
      "data_type": "moneda",
      "lineas": [
        { "concepto": "servicio A", "amount": 40.00 },
        { "concepto": "servicio B", "amount": 35.00 },
        { "concepto": "servicio C", "amount": 25.00 }
      ]
    },
    {
      "id": "F-1002",
      "total_declarado": 250.00,
      "data_type": "moneda",
      "lineas": [
        { "concepto": "licencia", "amount": 120.00 },
        { "concepto": "soporte", "amount": 90.00 },
        { "concepto": "implementacion", "amount": 30.00 }
      ]
    }
  ],
  "inventario": {
    "almacen": "BOG-01",
    "conteo_declarado": 12,
    "data_type": "entero",
    "items": ["sku-1", "sku-2", "sku-3", "sku-4", "sku-5",
              "sku-6", "sku-7", "sku-8", "sku-9", "sku-10"]
  }
}
```

Notas:
- `F-1001`: la suma de lineas (40 + 35 + 25 = 100) deberia coincidir con el total
  declarado.
- `F-1002`: la suma de lineas (120 + 90 + 30 = 240) NO coincide con el total
  declarado (250) -> mismatch esperado.
- `inventario`: el conteo declarado (12) frente al conteo real de items (10) ->
  mismatch esperado con `epsilon=0` por ser entero.

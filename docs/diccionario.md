# 📖 Diccionario de Datos (Esquema Canónico)

## Esquema Canónico

| Campo   | Descripción                               | Tipo de dato   | Ejemplo       |
|---------|-------------------------------------------|----------------|---------------|
| date    | Fecha del registro en formato ISO (YYYY-MM-DD) | `date`        | 2025-01-15    |
| partner | Nombre del socio/cliente/proveedor         | `string`       | "ACME Corp"   |
| amount  | Importe monetario en euros (EUR)           | `float`        | 1250.75       |

---

## Mapeos de Origen → Canónico

| Origen (CSV campo) | Canónico  | Ejemplo origen        | Ejemplo normalizado   |
|--------------------|-----------|-----------------------|-----------------------|
| `fecha`            | date      | `15/01/2025`          | `2025-01-15`          |
| `client_name`      | partner   | `"Acme co."`          | `"ACME CO"`           |
| `importe_total`    | amount    | `1.250,75`            | `1250.75`             |
| `transactionDate`  | date      | `"2025/01/15"`        | `2025-01-15`          |
| `partner_id`       | partner   | `"ID123-XYZ"`         | `"ID123-XYZ"`         |
| `valueEUR`         | amount    | `"1250.75 EUR"`       | `1250.75`             |

📌 *Nota: siempre que existan múltiples campos de origen, deben normalizarse al esquema canónico antes de la carga en la capa Silver.*

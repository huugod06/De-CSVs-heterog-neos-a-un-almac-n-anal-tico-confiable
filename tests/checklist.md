# ✅ Checklist de verificación (antes de entregar)

> Archivo: `tests/checklist.md`

## 1) Despliegue y acceso
- [x] **URL de Streamlit funcional** (pública y accesible).
  - URL: `https://...`
  - [ ] La app carga sin errores.
  - [ ] Se pueden subir CSV y ver resultados.

## 2) Artefactos de datos
- [x] **`bronze.csv`** generado y subido a **`/data/bronze/bronze.csv`**.
- [x] **`silver.csv`** generado y subido a **`/data/silver/silver.csv`**.
- [ ] Columnas canónicas presentes en Bronze: `date, partner, amount, source_file, ingested_at`.
- [ ] Silver agregado por `month × partner` con `amount` sumado.

## 3) Documentación del proyecto
- [ ] **README** con decisiones **justificadas** (relaciona las **5V** de Big Data → **elecciones** tecnológicas/arquitectónicas).
  - [ ] Arquitectura del pipeline (ingesta → validación → normalización → Bronze/Silver → KPIs).
  - [ ] Razones de librerías y formato de datos.
- [ ] **Capturas** de la app y flujo en `docs/` (mín. 2: carga de archivos y KPIs/gráfico).

## 4) Gobierno y semántica
- [ ] **`docs/diccionario.md`** completo (esquema canónico + mapeos origen→canónico).
- [ ] **`docs/gobernanza.md`** completo (origen/linaje, validaciones mínimas, mínimos privilegios, trazabilidad, roles).

## 5) Calidad y validaciones
- [ ] Las validaciones **pasan** (sin `NaT` en `date`, sin `amount` negativos, columnas presentes).
- [ ] Limpieza aplicada: normalización de `amount`, `partner` y fechas.
- [ ] Logs/linaje visibles (`source_file`, `ingested_at`).

## 6) Reproducibilidad
- [ ] `requirements.txt` en la raíz con dependencias mínimas.
- [ ] Estructura de carpetas conforme al README.
- [ ] `streamlit_app.py` como entrypoint principal.

# De CSVs heterogéneos a un almacén analítico confiable  
**Repositorio:** `bigdata-storage-lab-<dedios>`

---

## 1. Objetivo

Diseñar y desplegar un flujo completo de datos que permita transformar **CSVs heterogéneos** en un **almacén analítico confiable**, siguiendo las etapas:

1. **Ingesta** de archivos CSV de distintas fuentes.  
2. **Validación** de esquemas, tipos de datos y reglas de calidad.  
3. **Normalización** y limpieza para unificar formatos y estructuras.  
4. Creación de capas **Bronze / Silver** dentro del flujo de almacenamiento.  
   - **Bronze:** datos crudos validados.  
   - **Silver:** datos limpios y estandarizados.  
5. Generación de **KPIs** clave en una aplicación interactiva (Streamlit).  

El objetivo es demostrar la capacidad de implementar un pipeline reproducible, trazable y documentado, desde datos crudos hasta visualizaciones útiles.

---

## 2. Entregables

- 📂 **Repositorio GitHub público** (`bigdata-storage-lab-<dedios>`) que incluya:  
  - Scripts de ingesta, validación y normalización.  
  - Estructura de carpetas (bronze, silver).  
  - Notebook(s) de prueba y ejemplos de ejecución.  
  - Documentación clara en Markdown.  

- 🖥️ **Aplicación Streamlit**:  
  - Lectura de datos desde la capa *Silver*.  
  - Cálculo de al menos **3 KPIs relevantes**.  
  - Visualización interactiva (tablas, gráficos, filtros).  

---

## 3. Criterios de Evaluación

1. **Diseño y justificación técnica**  
   - Claridad en la arquitectura del pipeline.  
   - Razonamiento detrás de elecciones tecnológicas y de modelado.  

2. **Calidad de datos**  
   - Reglas de validación implementadas.  
   - Manejo de valores nulos, duplicados, inconsistencias.  

3. **Trazabilidad y diseño del Data Warehouse**  
   - Evidencia clara de transición entre capas (Bronze → Silver).  
   - Organización modular y reproducible.  

4. **Documentación**  
   - README inicial completo.  
   - Guías de ejecución reproducibles.  
   - Comentarios adecuados en el código.  

---

## 4. Qué NO subir

🚫 **No incluir datos sensibles o privados**.  
- Usa datos sintéticos, abiertos o anonimizados.  
- No exponer credenciales, tokens ni configuraciones locales de seguridad.  

---

## 5. Tiempo estimado por fase

| Fase                          | Tiempo estimado |
|-------------------------------|-----------------|
| Ingesta de CSVs               | 2 h             |
| Validación de datos           | 3 h             |
| Normalización y limpieza      | 4 h             |
| Definición Bronze / Silver    | 3 h             |
| Desarrollo KPIs (Streamlit)   | 4 h             |
| Documentación y README final  | 2 h             |
| **Total**                     | **18 h aprox.** |

## 6. Decisiones de diseño (5V)

- **Volumen**: Los CSV son medianos → se procesan con pandas; se usan capas Bronze/Silver para manejar escalabilidad.
- **Velocidad**: Procesamiento batch en memoria; Streamlit da resultados inmediatos.
- **Variedad**: Los CSV traen columnas distintas → se usa un mapeo origen→canónico y normalización de fechas/amount.
- **Veracidad**: Validaciones implementadas (`basic_checks`), linaje (`source_file`, `ingested_at`).
- **Valor**: Agregación en Silver (partner × mes), KPIs y gráfico → insights claros.


📌 **Recomendación:** trabajar por ramas (`feature/ingesta`, `feature/streamlit`, etc.) y hacer *pull requests* revisables.  


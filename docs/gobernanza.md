
# 🛡️ Gobernanza de Datos

## 1. Origen y linaje
- **Raw Layer**: archivos CSV heterogéneos (distintas fuentes).  
- **Bronze Layer**: ingesta de datos validados sin transformar.  
- **Silver Layer**: datos limpios y normalizados al esquema canónico.  
- **Gold Layer**: datos listos para análisis avanzado y KPIs.  

El **linaje** debe estar documentado en los *logs de ingesta y transformación*, trazando cada campo desde su origen hasta el modelo canónico.

---

## 2. Validaciones mínimas
- Formato de fechas en `YYYY-MM-DD`.
- `partner` no nulo, cadena normalizada (upper/lower case coherente).
- `amount` debe ser numérico y mayor o igual a 0.
- Registros duplicados deben eliminarse o marcarse.
- Archivo CSV con delimitador consistente (`;` o `,`) y codificación `UTF-8`.

---

## 3. Política de mínimos privilegios
- **Lectura/escritura**: solo el equipo de ingesta y procesamiento.  
- **Lectura analítica**: usuarios de negocio acceden únicamente a la capa **Gold**.  
- **Administración**: acceso restringido a responsables de plataforma.  
- **Credenciales**: nunca almacenadas en código, siempre mediante *vaults* o variables de entorno.  

---

## 4. Trazabilidad
- Cada job de ingesta/transformación debe generar un **log con timestamp**.  
- Todo dataset debe tener metadatos:  
  - Fecha de creación  
  - Fuente  
  - Script/proceso de transformación aplicado  
- Cambios de esquema deben documentarse en `docs/diccionario.md`.

---

## 5. Roles
- **Data Engineer**: diseña pipelines, valida calidad, mantiene linaje.  
- **Data Steward**: asegura cumplimiento de gobernanza y diccionario.  
- **Data Analyst**: consume datos de la capa Gold para generar KPIs.  
- **Administrador de Plataforma**: gestiona accesos y seguridad.  

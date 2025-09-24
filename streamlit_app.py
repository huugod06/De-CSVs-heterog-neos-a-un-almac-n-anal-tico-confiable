# streamlit_app.py
# ------------------------------------------------------------
# Big Data Storage Lab - <dedios>
# App Streamlit para:
# - Subida de múltiples CSV
# - Normalización a esquema canónico (date, partner, amount)
# - Trazabilidad (source_file, ingested_at)
# - Validaciones básicas
# - Derivación a capa Silver (partner x mes)
# - KPIs y visualización
# - Descarga de bronze.csv y silver.csv
# ------------------------------------------------------------

from __future__ import annotations

import io
from typing import Dict, List

import pandas as pd
import streamlit as st

# Importa tus utilidades del repo (asegúrate de que `src` es un paquete/módulo accesible)
from src.transform import normalize_columns, to_silver
from src.validate import basic_checks
from src.ingest import tag_lineage, concat_bronze


# ------------------------------
# Utilidades de lectura
# ------------------------------
def read_csv_with_fallback(file) -> pd.DataFrame:
    """
    Intenta leer CSV con UTF-8 y hace fallback a latin-1 si falla.
    Delimitador por defecto: auto (pandas intenta inferir).
    """
    try:
        return pd.read_csv(file)
    except UnicodeDecodeError:
        file.seek(0)  # reinicia puntero
        return pd.read_csv(file, encoding="latin-1")


def build_mapping(date_col: str, partner_col: str, amount_col: str) -> Dict[str, str]:
    """
    Construye el mapeo origen -> canónico.
    """
    mapping: Dict[str, str] = {}
    if date_col:
        mapping[date_col] = "date"
    if partner_col:
        mapping[partner_col] = "partner"
    if amount_col:
        mapping[amount_col] = "amount"
    return mapping


# ------------------------------
# UI
# ------------------------------
st.set_page_config(
    page_title="Big Data Storage Lab - <dedios>",
    layout="wide",
)

st.title("Big Data Storage Lab - <dedios>")
st.caption("De CSVs heterogéneos a un almacén analítico confiable")

with st.sidebar:
    st.header("⚙️ Configuración de columnas origen")
    st.markdown("Indica los **nombres de columna** en tus CSVs que corresponden al esquema canónico.")
    date_col = st.text_input("Columna origen → date (YYYY-MM-DD)", value="date")
    partner_col = st.text_input("Columna origen → partner (string)", value="partner")
    amount_col = st.text_input("Columna origen → amount (float EUR)", value="amount")

    st.divider()
    st.header("📤 Subida de archivos")
    uploaded_files = st.file_uploader(
        "Selecciona uno o varios CSV",
        type=["csv"],
        accept_multiple_files=True,
    )

st.markdown("### 1) Ingesta y normalización (Bronze)")

bronze_frames: List[pd.DataFrame] = []

if uploaded_files:
    mapping = build_mapping(date_col.strip(), partner_col.strip(), amount_col.strip())

    for up in uploaded_files:
        st.subheader(f"Archivo: `{up.name}`")

        # Leer CSV con fallback de encoding
        df_raw = read_csv_with_fallback(up)
        st.write("Vista previa (raw):")
        st.dataframe(df_raw.head(10), use_container_width=True)

        # Normalizar a columnas canónicas
        df_norm = normalize_columns(df_raw, mapping)

        # Trazabilidad
        df_tag = tag_lineage(df_norm, source_name=up.name)

        # Muestra resultado intermedio
        st.write("Normalizado + linaje:")
        st.dataframe(df_tag.head(10), use_container_width=True)

        bronze_frames.append(df_tag)

    # Unificar Bronze
    bronze = concat_bronze(bronze_frames)
    st.markdown("#### Bronze unificado")
    st.dataframe(bronze, use_container_width=True)

    # Validaciones
    st.markdown("### 2) Validaciones básicas")
    errors = basic_checks(bronze[["date", "partner", "amount"]]) if not bronze.empty else ["Dataset vacío"]

    if errors:
        st.error("Se encontraron problemas en las validaciones:")
        for e in errors:
            st.markdown(f"- {e}")
        st.info("Corrige las columnas origen, revisa los archivos o limpia los datos y vuelve a intentar.")
    else:
        st.success("Validaciones OK ✅")

        # ------------------------------
        # Silver derivado
        # ------------------------------
        st.markdown("### 3) Derivación a Silver (partner × mes)")
        silver = to_silver(bronze[["date", "partner", "amount"]])

        # KPIs simples
        st.markdown("#### KPIs")
        total_amount = float(silver["amount"].sum()) if not silver.empty else 0.0
        n_partners = bronze["partner"].nunique(dropna=True) if "partner" in bronze.columns else 0
        n_months = silver["month"].nunique(dropna=True) if not silver.empty else 0

        kpi_cols = st.columns(3)
        kpi_cols[0].metric("Importe total (EUR)", f"{total_amount:,.2f}")
        kpi_cols[1].metric("Partners únicos", f"{n_partners}")
        kpi_cols[2].metric("Meses cubiertos", f"{n_months}")

        st.markdown("#### Silver (agregado)")
        st.dataframe(silver, use_container_width=True)

        # ------------------------------
        # Visualización (bar chart mes vs amount)
        # ------------------------------
        st.markdown("#### Gráfico: Importe por mes")
        # Agrega por mes (independiente de partner) para el gráfico de barras
        by_month = (
            silver.groupby("month", as_index=False)["amount"].sum(min_count=1)
            if not silver.empty
            else pd.DataFrame(columns=["month", "amount"])
        )

        # Streamlit maneja el chart sin estilos personalizados
        # Asegura que month sea interpretable
        if not by_month.empty:
            # Convertir a string ISO YYYY-MM para un eje más claro
            by_month_display = by_month.copy()
            by_month_display["month"] = by_month_display["month"].dt.strftime("%Y-%m")
            st.bar_chart(by_month_display, x="month", y="amount", use_container_width=True)
        else:
            st.info("No hay datos suficientes para graficar.")

        # ------------------------------
        # Descargas
        # ------------------------------
        st.markdown("### 4) Descargas")
        bronze_csv = bronze.to_csv(index=False).encode("utf-8")
        silver_csv = silver.to_csv(index=False).encode("utf-8")

        dl_cols = st.columns(2)
        with dl_cols[0]:
            st.download_button(
                label="⬇️ Descargar bronze.csv",
                data=bronze_csv,
                file_name="bronze.csv",
                mime="text/csv",
            )
        with dl_cols[1]:
            st.download_button(
                label="⬇️ Descargar silver.csv",
                data=silver_csv,
                file_name="silver.csv",
                mime="text/csv",
            )

else:
    st.info("Sube uno o varios CSV desde la barra lateral para comenzar.")


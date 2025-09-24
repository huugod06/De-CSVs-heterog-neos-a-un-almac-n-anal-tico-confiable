from __future__ import annotations

from typing import Dict
import pandas as pd


def _parse_amount_series(s: pd.Series) -> pd.Series:
    """
    Normaliza importes:
    - Quita símbolos de moneda (€, EUR).
    - Maneja miles/punto y coma europea (1.234,56 -> 1234.56).
    - Convierte a float.
    """
    s = (
        s.astype(str)
        .str.replace(r"\s+", "", regex=True)  # quita espacios (incl. no-break)
        .str.replace("€", "", regex=False)
        .str.replace("EUR", "", case=False, regex=True)
    )

    # Caso mixto con . y ,: asumimos formato europeo (coma decimal)
    both_mask = s.str.contains(r"[.,]") & s.str.contains(r"\.") & s.str.contains(r",")
    s_both = s.where(~both_mask, s.str.replace(r"\.", "", regex=True).str.replace(",", ".", regex=False))

    # Solo comas: asume coma decimal
    only_comma = s_both.str.contains(",") & ~s_both.str.contains(r"\.")
    s_comma = s_both.where(~only_comma, s_both.str.replace(",", ".", regex=False))

    # Miles con apóstrofo u otros separadores exóticos
    s_clean = s_comma.str.replace("'", "", regex=False)

    # Vacíos a NaN
    s_clean = s_clean.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    return pd.to_numeric(s_clean, errors="coerce")


def normalize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Renombra columnas según `mapping` (origen -> 'date'|'partner'|'amount'),
    parsea fechas a datetime (ISO), normaliza `amount`, y limpia `partner`.

    Args:
        df: DataFrame de entrada (bronze).
        mapping: diccionario {col_origen: col_canonica}.

    Returns:
        DataFrame con columnas canónicas: ['date','partner','amount'] normalizadas.
    """
    # Renombrar columnas
    df = df.rename(columns=mapping).copy()

    # Fechas -> datetime (utc-naive, ISO al serializar)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=False).dt.tz_localize(None)

    # Partner -> limpiar espacios y normalizar espacios múltiples
    if "partner" in df.columns:
        df["partner"] = (
            df["partner"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    # Amount -> float normalizado
    if "amount" in df.columns:
        df["amount"] = _parse_amount_series(df["amount"])

    # Conservar solo las canónicas si existen
    keep = [c for c in ["date", "partner", "amount"] if c in df.columns]
    return df[keep]


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega 'amount' por 'partner' y mes.
    - Crea columna 'month' (primer día del mes, 00:00:00).
    - Devuelve DataFrame con columnas ['month','partner','amount'].
    """
    required = {"date", "partner", "amount"}
    missing = required - set(bronze.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas en bronze: {sorted(missing)}")

    df = bronze.copy()

    # Asegurar datetime aunque venga como string desde CSV
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.tz_localize(None)

    # month como primer día del mes (seguro en todas las versiones de pandas)
    df["month"] = df["date"].dt.to_period("M").dt.start_time

    # Agregación
    silver = (
        df.groupby(["month", "partner"], dropna=False, as_index=False)["amount"]
        .sum(min_count=1)  # si todos NaN, resultado NaN
    )
    return silver


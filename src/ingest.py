from __future__ import annotations

from typing import Iterable, List
import pandas as pd


def tag_lineage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Añade metadatos de linaje:
    - 'source_file': nombre/identificador de la fuente.
    - 'ingested_at': timestamp UTC en ISO 8601 (string).

    Args:
        df: DataFrame de entrada (post-ingesta).
        source_name: nombre del archivo/fuente original.

    Returns:
        DataFrame con columnas adicionales de linaje.
    """
    tagged = df.copy()
    tagged["source_file"] = source_name
    tagged["ingested_at"] = pd.Timestamp.now(tz="UTC").isoformat()
    return tagged


def concat_bronze(frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatena múltiples DataFrames al esquema estándar de bronze:
    ['date', 'partner', 'amount', 'source_file', 'ingested_at']

    - Reindexa/ordena columnas.
    - Mantiene tipos razonables: date datetime64, amount float, metadatos string.

    Args:
        frames: iterable de DataFrames compatibles.

    Returns:
        DataFrame concatenado con el esquema definido.
    """
    cols = ["date", "partner", "amount", "source_file", "ingested_at"]
    cast_order: List[pd.DataFrame] = []

    for frame in frames:
        if frame is None or frame.empty:
            continue
        f = frame.copy()

        # Asegurar columnas faltantes como NaN
        for c in cols:
            if c not in f.columns:
                f[c] = pd.NA

        # Tipos recomendados
        f["date"] = pd.to_datetime(f["date"], errors="coerce").dt.tz_localize(None)
        f["amount"] = pd.to_numeric(f["amount"], errors="coerce")
        f["partner"] = f["partner"].astype("string")
        f["source_file"] = f["source_file"].astype("string")
        # ingested_at es ISO string (UTC)
        f["ingested_at"] = f["ingested_at"].astype("string")

        cast_order.append(f[cols])

    if not cast_order:
        # Devuelve DataFrame vacío con el esquema esperado
        return pd.DataFrame(columns=cols)

    bronze = pd.concat(cast_order, ignore_index=True)
    return bronze

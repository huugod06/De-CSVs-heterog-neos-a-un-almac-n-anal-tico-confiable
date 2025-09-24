from __future__ import annotations

from typing import List
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_numeric_dtype


def basic_checks(df: pd.DataFrame) -> List[str]:
    """
    Valida requisitos mínimos sobre el esquema canónico.

    Reglas:
    - Columnas 'date','partner','amount' presentes.
    - 'date' en dtype datetime (sin NaT).
    - 'amount' numérico y >= 0 (sin NaN negativos).

    Returns:
        Lista de mensajes de error (vacía si todo OK).
    """
    errors: List[str] = []

    # 1) Columnas presentes
    required = ["date", "partner", "amount"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        errors.append(f"Faltan columnas requeridas: {missing}")
        # Si faltan columnas base, el resto de validaciones puede fallar
        return errors

    # 2) date es datetime y sin NaT
    if not is_datetime(df["date"]):
        errors.append("Columna 'date' no es datetime.")
    else:
        if df["date"].isna().any():
            errors.append("Existen valores NaT/NaN en 'date'.")

    # 3) amount numérico y >= 0 (permitimos NaN; sólo reportamos negativos o no numéricos)
    if not is_numeric_dtype(df["amount"]):
        errors.append("Columna 'amount' no es numérica.")
    else:
        if (df["amount"].dropna() < 0).any():
            errors.append("Existen valores negativos en 'amount'.")

    return errors


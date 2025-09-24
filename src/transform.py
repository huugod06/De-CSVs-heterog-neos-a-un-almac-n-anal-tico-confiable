def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega 'amount' por 'partner' y mes.
    - Crea columna 'month' (primer día del mes, 00:00:00).
    - Devuelve ['month','partner','amount'].
    """
    required = {"date", "partner", "amount"}
    missing = required - set(bronze.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas en bronze: {sorted(missing)}")

    df = bronze.copy()

    # Asegurar datetime aunque venga como string desde CSV
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.tz_localize(None)

    # month = inicio del mes (seguro en todas las versiones de pandas)
    df["month"] = df["date"].dt.to_period("M").dt.start_time

    silver = (
        df.groupby(["month", "partner"], dropna=False, as_index=False)["amount"]
        .sum(min_count=1)
    )
    return silver


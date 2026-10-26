"""Cálculos financieros exactos: el LLM nunca calcula números."""


def cuota_credito(monto: float, tasa_anual: float, meses: int) -> float:
    """Cuota mensual fija (sistema francés). tasa_anual en % (ej. 12 = 12%)."""
    if monto <= 0 or meses <= 0:
        raise ValueError("monto y meses deben ser positivos")
    i = tasa_anual / 100 / 12
    if i == 0:
        return round(monto / meses, 2)
    return round(monto * i / (1 - (1 + i) ** -meses), 2)


def total_e_intereses(monto: float, tasa_anual: float, meses: int) -> tuple[float, float]:
    """(total pagado, intereses) de un crédito con cuota fija."""
    total = round(cuota_credito(monto, tasa_anual, meses) * meses, 2)
    return total, round(total - monto, 2)


def ahorro_mensual(meta: float, meses: int) -> float:
    """Ahorro mensual necesario para alcanzar una meta, sin interés."""
    if meta <= 0 or meses <= 0:
        raise ValueError("meta y meses deben ser positivos")
    return round(meta / meses, 2)


def interes_compuesto(capital: float, tasa_anual: float, anios: float, n: int = 12) -> float:
    """Monto final con capitalización n veces al año."""
    if capital <= 0 or anios <= 0 or n <= 0:
        raise ValueError("capital, años y n deben ser positivos")
    return round(capital * (1 + tasa_anual / 100 / n) ** (n * anios), 2)

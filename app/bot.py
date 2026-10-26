"""Detecta la intención con reglas; el LLM (opcional) solo atiende preguntas abiertas."""
import os
import re

from app import finanzas

GLOSARIO = {
    "uf": "La UF (Unidad de Fomento) es una unidad de cuenta chilena reajustable según la inflación.",
    "cae": "El CAE (Carga Anual Equivalente) expresa el costo total anual de un crédito, incluyendo gastos.",
    "apv": "El APV (Ahorro Previsional Voluntario) es un ahorro adicional para la jubilación con beneficios tributarios.",
    "inflación": "La inflación es el aumento sostenido de los precios, que reduce el poder adquisitivo.",
    "fondo mutuo": "Un fondo mutuo agrupa dinero de muchos inversionistas para invertir en instrumentos diversificados.",
}

NUM = r"(\d+(?:[.,]\d+)?)"


def _n(s: str) -> float:
    return float(s.replace(",", "."))


def _numeros(texto: str) -> list[float]:
    return [_n(x) for x in re.findall(NUM, texto)]


def _llm(mensaje: str) -> str | None:
    clave = os.getenv("OPENAI_API_KEY")
    if not clave:
        return None
    try:
        import httpx

        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {clave}"},
            json={
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "messages": [
                    {"role": "system", "content": "Eres Finbot, asistente de finanzas personales. Responde breve y sin inventar cifras."},
                    {"role": "user", "content": mensaje},
                ],
            },
            timeout=20,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


def responder(mensaje: str) -> dict:
    t = mensaje.lower().strip()
    nums = _numeros(t)

    if "cuota" in t or "crédito" in t or "credito" in t:
        if len(nums) >= 3:
            monto, tasa, meses = nums[0], nums[1], int(nums[2])
            try:
                c = finanzas.cuota_credito(monto, tasa, meses)
                total, intereses = finanzas.total_e_intereses(monto, tasa, meses)
                return {"respuesta": f"La cuota mensual es {c:,.2f} (monto {monto:,.0f}, tasa {tasa}% anual, {meses} meses). Total pagado: {total:,.2f}, de los cuales {intereses:,.2f} son intereses.", "fuente": "reglas"}
            except ValueError as e:
                return {"respuesta": f"Datos inválidos: {e}.", "fuente": "reglas"}
        return {"respuesta": "Para calcular la cuota indícame: monto, tasa anual (%) y meses. Ej: cuota crédito 1000000 12 24", "fuente": "reglas"}

    if "ahorr" in t and nums:
        if len(nums) >= 2:
            try:
                a = finanzas.ahorro_mensual(nums[0], int(nums[1]))
                return {"respuesta": f"Debes ahorrar {a:,.2f} al mes para llegar a {nums[0]:,.0f} en {int(nums[1])} meses.", "fuente": "reglas"}
            except ValueError as e:
                return {"respuesta": f"Datos inválidos: {e}.", "fuente": "reglas"}
        return {"respuesta": "Indícame la meta y los meses. Ej: ahorro 600000 12", "fuente": "reglas"}

    if "interés" in t or "interes" in t:
        if len(nums) >= 3:
            try:
                m = finanzas.interes_compuesto(nums[0], nums[1], nums[2])
                return {"respuesta": f"Con interés compuesto, {nums[0]:,.0f} a {nums[1]}% anual por {nums[2]:g} años llegan a {m:,.2f}.", "fuente": "reglas"}
            except ValueError as e:
                return {"respuesta": f"Datos inválidos: {e}.", "fuente": "reglas"}
        return {"respuesta": "Indícame capital, tasa anual (%) y años. Ej: interés compuesto 1000000 5 10", "fuente": "reglas"}

    for termino, definicion in GLOSARIO.items():
        if termino in t:
            return {"respuesta": definicion, "fuente": "glosario"}

    r = _llm(mensaje)
    if r:
        return {"respuesta": r, "fuente": "llm"}
    return {"respuesta": "No entendí. Prueba: 'cuota crédito 1000000 12 24', 'ahorro 600000 12', 'interés compuesto 1000000 5 10' o pregunta qué es la UF, CAE, APV, inflación o fondo mutuo.", "fuente": "reglas"}

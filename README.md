# Finbot

Asistente de educación financiera para Chile, hecho con FastAPI.
Los números (cuotas, ahorro, interés) los calculan funciones exactas; el LLM solo responde preguntas abiertas y solo si hay `OPENAI_API_KEY`.

## Ejecutar

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --port 8000
```

Abre http://localhost:8000 para el chat.

## Endpoints

- `GET /health` → `{"status": "ok"}`
- `POST /chat` con `{"mensaje": "..."}` → `{"respuesta": "...", "fuente": "reglas|glosario|llm"}`
- `GET /` → chat HTML mínimo

## Ejemplos

- `cuota crédito 1000000 12 24` (monto, tasa anual %, meses)
- `ahorro 600000 12` (meta, meses)
- `interés compuesto 1000000 5 10` (capital, tasa anual %, años)
- `qué es la UF` (también CAE, APV, inflación, fondo mutuo)

## LLM opcional

Copia `.env.example` a `.env`, define `OPENAI_API_KEY` y expórtala (`export $(cat .env)`) antes de iniciar.

## Pruebas y Docker

```bash
.venv/bin/pytest
docker build -t finbot . && docker run --rm -p 8080:8080 finbot
```

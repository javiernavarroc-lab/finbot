from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator

from app.bot import responder

app = FastAPI(title="Finbot")


class Mensaje(BaseModel):
    mensaje: str

    @field_validator("mensaje")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("el mensaje no puede estar vacío")
        return v


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
@app.get("/chat", response_class=HTMLResponse)
def pagina():
    return """<!doctype html><meta charset=utf-8><title>Finbot</title>
<body style="font-family:sans-serif;max-width:640px;margin:2rem auto">
<h2>Finbot</h2><div id=log style="min-height:200px;border:1px solid #ccc;padding:8px;margin-bottom:8px"></div>
<form id=f><input id=m style="width:80%" placeholder="cuota crédito 1000000 12 24" autofocus><button>Enviar</button></form>
<script>
f.onsubmit=async e=>{e.preventDefault();const t=m.value;m.value='';
log.innerHTML+='<p><b>Tú:</b> '+t.replace(/</g,'&lt;')+'</p>';
const r=await (await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mensaje:t})})).json();
log.innerHTML+='<p><b>Finbot</b> <i>('+r.fuente+')</i>: '+r.respuesta.replace(/</g,'&lt;')+'</p>'}
</script></body>"""


@app.post("/chat")
def chat(m: Mensaje):
    return responder(m.mensaje)

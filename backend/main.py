from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from downloader import link_downloader

app = FastAPI(
    title="CS-Music Downloader API",
    description="Backend para procesamiento de descarga de musica por python",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str

@app.get("/")
def raiz():
    return {"Servidor en FastAPI funcionando"}

@app.post("/descargar")
def descargas_audio(request: DownloadRequest):
    result = link_downloader(request.url)

    if result["state"] == "error":
        raise HTTPException(status_code=400, detail=result["details"])

    return {
        "state": "ok",
        "result": result,
    }
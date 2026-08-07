from fastapi import FastAPI

from panel_api.routes.ingestion import router as ingestion_router

app = FastAPI(title="Panel API", version="0.1.0")
app.include_router(ingestion_router)


@app.get("/healthz", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

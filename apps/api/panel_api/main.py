from fastapi import FastAPI

app = FastAPI(title="Panel API", version="0.1.0")


@app.get("/healthz", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


from fastapi import FastAPI

app = FastAPI(title="Enterprise SSO Integration")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

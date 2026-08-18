from fastapi import FastAPI

app = FastAPI(title="OTT Situation Picker API")


@app.get("/health")
def health_check():
    return {"status": "ok"}

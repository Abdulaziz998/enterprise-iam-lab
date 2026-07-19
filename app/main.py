from fastapi import FastAPI

app = FastAPI(
    title="Enterprise IAM Lifecycle Lab",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Enterprise IAM Lifecycle Lab API",
        "status": "running",
    }

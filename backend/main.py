from fastapi import FastAPI, HTTPException
from routes import router

app = FastAPI(
    title="JWT Analyzer API",
    version="1.0.0"
)

app.include_router(router)

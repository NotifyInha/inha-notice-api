from fastapi import FastAPI
import uvicorn
from V1 import router as v1_router

app = FastAPI(
    title="Notify Inha",
    description="인하알리미의 openapi 문서입니다",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.include_router(v1_router, prefix="/api/v1")


@app.get("/api")
async def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from V1 import router as v1_router


origins = [
    "*"
]


app = FastAPI(
    title="Notify Inha",
    description="인하알리미의 openapi 문서입니다",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router, prefix="/api/v1")


@app.get("/api")
async def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

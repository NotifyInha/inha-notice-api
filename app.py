from fastapi import FastAPI
import uvicorn
from V1 import router as v1_router

app = FastAPI()
app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

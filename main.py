from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(
    title="Sample FastAPI Service",
    version="1.0.0",
    description="A simple FastAPI application with health check endpoint.",
)

@app.get("/", tags=["Root"])
async def read_root():
    return JSONResponse(
        status_code=200,
        content={"message": "Hello, FastAPI!"},
    )

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "ok"},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

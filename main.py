from fastapi import FastAPI
from fastapi.responses import JSONResponse
from openai import OpenAI
import uvicorn
import os

app = FastAPI(
    title="Sample FastAPI Service",
    version="1.0.0",
    description="A simple FastAPI application with OpenAI test endpoint.",
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


@app.get("/openai-test", tags=["OpenAI"])
async def openai_test():
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Say hello from OpenAI API",
                }
            ],
            max_tokens=20,
        )

        return JSONResponse(
            status_code=200,
            content={
                "response": response.choices[0].message.content
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

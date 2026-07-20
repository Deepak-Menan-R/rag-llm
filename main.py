from fastapi import FastAPI
from fastapi.responses import JSONResponse
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic
import uvicorn
import os

app = FastAPI(
    title="Sample FastAPI Services",
    version="1.0.0",
    description="FastAPI app with OpenAI, Gemini, and Claude test endpoints.",
)

# -----------------------------
# OpenAI Client
# -----------------------------
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------
# Gemini Client
# -----------------------------
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# Claude Client
# -----------------------------
claude_client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/", tags=["Root"])
async def read_root():
    return JSONResponse(
        status_code=200,
        content={"message": "Hello, FastAPI!"},
    )


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "ok"},
    )


# -----------------------------
# OpenAI Test Endpoint
# -----------------------------
@app.get("/openai-test", tags=["OpenAI"])
async def openai_test():
    try:
        response = openai_client.chat.completions.create(
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
                "provider": "openai",
                "response": response.choices[0].message.content,
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )


# -----------------------------
# Gemini Test Endpoint
# -----------------------------
@app.get("/gemini-test", tags=["Gemini"])
async def gemini_test():
    try:
        response = gemini_model.generate_content(
            "Say hello from Gemini API"
        )

        return JSONResponse(
            status_code=200,
            content={
                "provider": "gemini",
                "response": response.text,
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )


# -----------------------------
# Claude Test Endpoint
# -----------------------------
@app.get("/claude-test", tags=["Claude"])
async def claude_test():
    try:
        response = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=20,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello from Claude API",
                }
            ],
        )

        return JSONResponse(
            status_code=200,
            content={
                "provider": "claude",
                "response": response.content[0].text,
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

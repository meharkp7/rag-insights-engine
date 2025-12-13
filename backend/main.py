# backend/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes import upload, rag, evaluate

os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/embeddings", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting RAG Pipeline MVP...")
    print("📁 Data directories ready")
    yield
    print("🛑 Shutting down...")


app = FastAPI(
    title="RAG Pipeline MVP API",
    description="Testing and optimization platform for RAG systems",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://rag-insights-engine.*\.vercel\.app|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(rag.router, prefix="/api", tags=["RAG"])
app.include_router(evaluate.router, prefix="/api", tags=["Evaluate"])


@app.get("/")
def root():
    return {
        "message": "RAG Pipeline MVP API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /api/upload-docs",
            "list_docs": "GET /api/docs",
            "run_rag": "POST /api/run-rag",
            "evaluate": "POST /api/evaluate",
        },
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Use string import for reload
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from backend.db import engine, Base
from backend.models.document import Document
from backend.routes import upload, rag, evaluate

os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/embeddings", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting RAG Pipeline MVP...")
    yield
    print("🛑 Shutting down...")

app = FastAPI(
    title="RAG Pipeline MVP API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(rag.router, prefix="/api", tags=["RAG"])
app.include_router(evaluate.router, prefix="/api", tags=["Evaluate"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

# 🔥 FRONTEND SERVE (LAST LINE)
app.mount("/", StaticFiles(directory="dist", html=True), name="frontend")
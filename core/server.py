import os

# =========================================================================
# VERCEL FIX: MUST BE AT THE ABSOLUTE TOP BEFORE ANY OTHER APP IMPORTS
# =========================================================================
if os.environ.get("VERCEL") == "1":
    os.environ["TIKTOKEN_CACHE_DIR"] = "/tmp/tiktoken"
    os.makedirs("/tmp/tiktoken", exist_ok=True)

    os.environ["HF_HOME"] = "/tmp/huggingface"
    os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"
    os.environ["SENTENCE_TRANSFORMERS_HOME"] = "/tmp/sentence_transformers"  # ADD THIS
    os.environ["XDG_CACHE_HOME"] = "/tmp/xdg_cache"                          # ADD THIS
    os.makedirs("/tmp/huggingface", exist_ok=True)
    os.makedirs("/tmp/sentence_transformers", exist_ok=True)
    os.makedirs("/tmp/xdg_cache", exist_ok=True)

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["OMP_NUM_THREADS"] = "1"
# =========================================================================

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from core.logging_config import setup_logging
from api.routes.ingestion import router as ingestion_router
from api.routes.rag import router as rag_router
from dotenv import load_dotenv

load_dotenv()
setup_logging()

app = FastAPI(title="Multi-Tenant RAG")

app.include_router(ingestion_router)
app.include_router(rag_router)

static_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def home():
    return FileResponse(static_path / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}
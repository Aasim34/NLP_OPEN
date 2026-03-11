"""
Indian Code-Mixed Language Converter — FastAPI Backend
======================================================
Entry point for the application.

Run with:
    uvicorn main:app --reload
"""

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the project root is on sys.path so relative imports work
# when running via `uvicorn main:app` from inside the project folder.
_PROJECT_ROOT = str(Path(__file__).resolve().parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from routes.convert import router as convert_router  # noqa: E402

# ---------------------------------------------------------------------------
# Application setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Indian Code-Mixed Language Converter",
    description=(
        "Converts Hinglish (Hindi + English mixed) sentences into "
        "pure Hindi (Devanagari), Finglish (Roman Hindi), and English. "
        "Runs entirely offline — no external APIs required."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS Configuration - Allow frontend to connect
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default dev server
        "http://localhost:3000",  # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the /convert route
app.include_router(convert_router)


# Health-check endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": "Indian Code-Mixed Language Converter is running."}

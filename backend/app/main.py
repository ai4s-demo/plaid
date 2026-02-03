"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import chat, file, layout

app = FastAPI(
    title=settings.app_name,
    description="AI-powered microplate layout designer",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(file.router, prefix="/api/file", tags=["file"])
app.include_router(layout.router, prefix="/api/layout", tags=["layout"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.app_name}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

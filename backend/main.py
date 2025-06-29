from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.database import engine, Base
from app.api import brain_dump, emotion_detection, summary_generation

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="NeuroDesk API",
    description="AI-Powered Productivity & Mental Wellness API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(brain_dump.router, prefix="/api/v1", tags=["brain-dump"])
app.include_router(emotion_detection.router, prefix="/api/v1", tags=["emotion"])
app.include_router(summary_generation.router, prefix="/api/v1", tags=["summary"])

@app.get("/")
async def root():
    return {
        "message": "NeuroDesk API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 
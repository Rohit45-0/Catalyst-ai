from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, projects, uploads, jobs, assets
from app.db.session import get_engine, Base
from app.db import models  # Import models to register them with Base

app = FastAPI(
    title="Catalyst AI Backend",
    version="0.1.0",
    description="Agent-orchestrated marketing intelligence platform"
)

# Add CORS middleware to fix Swagger OAuth2 "Failed to fetch" error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    # Create database tables
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not connect to database: {e}")
        print("The application will start but database operations may fail.")

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(uploads.router)
app.include_router(jobs.router)
app.include_router(assets.router)

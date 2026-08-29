from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.prediction import router as prediction_router
from backend.app.api.job_fit import router as job_fit_router
from backend.app.api.analyze import router as analyze_router
from backend.app.api.upload import router as upload_router


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="ResumeLens AI",
    description="AI-powered resume analysis and job-fit platform.",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(prediction_router)
app.include_router(job_fit_router)
app.include_router(analyze_router)
app.include_router(upload_router)


# ============================================================
# HEALTH
# ============================================================

@app.get("/")
def root():
    return {
        "message": "ResumeLens AI API is running.",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ResumeLens AI",
    }
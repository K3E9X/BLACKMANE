"""
BLACKMANE Backend - Main Application Entry Point

Security by Design Architecture Analysis Tool
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# API routers imports
from api.v1 import projects
# Other routers (to be implemented during MVP development)
# from api.v1 import architectures, analyses, recommendations, maturity, roadmap
from database.connection import init_db

app = FastAPI(
    title="BLACKMANE API",
    description="Security by Design Architecture Analysis API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Security: Only allow localhost
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "::1"]
)

# CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": "BLACKMANE API",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Health check for monitoring"""
    return {"status": "healthy"}


# Include API routers
app.include_router(projects.router, prefix="/api/v1", tags=["Projects"])

# Other routers (to be implemented)
# app.include_router(architectures.router, prefix="/api/v1", tags=["architectures"])
# app.include_router(analyses.router, prefix="/api/v1", tags=["analyses"])
# app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])
# app.include_router(maturity.router, prefix="/api/v1", tags=["maturity"])
# app.include_router(roadmap.router, prefix="/api/v1", tags=["roadmap"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

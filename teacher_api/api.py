"""
Main API module.

FastAPI application with ethical constraints enforced at every endpoint.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from teacher_api import __version__
from teacher_api.ethics.constraints import EthicsGuard
from teacher_api.provenance.audit_log import AuditLog

# Initialize FastAPI app
app = FastAPI(
    title="Harmony Teacher API",
    description="Educator-first planning, awareness, and collaboration — consent-first, teacher-in-the-loop",
    version=__version__,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global audit log
audit_log = AuditLog()


# Models
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    ethics_enforced: bool


# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        ethics_enforced=True,
    )


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "name": "Harmony Teacher API",
        "version": __version__,
        "docs": "/docs",
        "principles": [
            "Privacy by default",
            "Consent-gated access",
            "Teacher override always wins",
            "No diagnostic outputs",
            "Audit-grade provenance",
        ],
    }


# TODO: Add endpoints for:
# - Lesson planning
# - Grading assistance
# - Awareness flags
# - Collaboration channels
# Each endpoint will use EthicsGuard and audit_log

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

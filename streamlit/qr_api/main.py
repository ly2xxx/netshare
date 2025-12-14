#!/usr/bin/env python3
"""
FastAPI application for QR code generation service
Designed to run embedded within Streamlit app
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import API_VERSION, API_PREFIX
from .routers import health, qr, greeting

# Create FastAPI app
app = FastAPI(
    title="QR Code Generation API",
    description="Embedded API for QR code and greeting operations",
    version=API_VERSION,
    docs_url=f"{API_PREFIX}/docs",
    redoc_url=f"{API_PREFIX}/redoc",
    openapi_url=f"{API_PREFIX}/openapi.json"
)

# CORS middleware (allow Streamlit to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Localhost only in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=API_PREFIX)
app.include_router(qr.router, prefix=API_PREFIX)
app.include_router(greeting.router, prefix=API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "QR Code Generation API",
        "version": API_VERSION,
        "docs": f"{API_PREFIX}/docs"
    }


# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    """Called when API starts"""
    print(f"[QR API] Starting on port 8000")
    print(f"[QR API] Documentation: http://127.0.0.1:8000{API_PREFIX}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Called when API stops"""
    print("[QR API] Shutting down")

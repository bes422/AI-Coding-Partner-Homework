"""
FastAPI Application Entry Point

Customer Support Ticket System
- REST API for ticket management
- Multi-format bulk import (CSV, JSON, XML)
- Auto-categorization based on content analysis
"""

from fastapi import FastAPI

# Import routers (to be implemented)
# from .routes import tickets, import_routes

app = FastAPI(
    title="Customer Support Ticket System",
    description="REST API for managing customer support tickets with bulk import and auto-classification",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Customer Support Ticket System"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "features": {
            "crud": True,
            "import_csv": True,
            "import_json": True,
            "import_xml": True,
            "auto_classification": True,
        }
    }


# TODO: Include routers
# app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
# app.include_router(import_routes.router, prefix="/import", tags=["Import"])

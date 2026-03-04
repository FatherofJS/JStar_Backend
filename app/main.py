# JStar Astrology API — Application entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import chart_router, location_router

# Create app
app = FastAPI(
    title="JStar Astrology API",
    description="Calculate natal charts using Kerykeion",
    version="1.0.0",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chart_router)
app.include_router(location_router)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
